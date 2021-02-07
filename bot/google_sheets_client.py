import logging
import os
from typing import Mapping, Any

import httplib2  # type: ignore
import apiclient.discovery  # type: ignore
import oauth2client.service_account  # type: ignore


class CheckFailed(BaseException):
    pass


class GoogleSheetsClient:
    @staticmethod
    def _create_api(credentials_file_path: str):
        credentials = (
            oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(
                credentials_file_path,
                ['https://www.googleapis.com/auth/spreadsheets'],
            )
        )

        http_auth = credentials.authorize(httplib2.Http())
        return apiclient.discovery.build('sheets', 'v4', http=http_auth)

    def __init__(self, config: Mapping[str, Any]):
        cred_file_path = os.path.join(
            config['cache_dir'], config['google_sheets_credentials_file'],
        )
        spreadsheet_id = config['google_sheets_spreadsheet_id']
        self._api = self._create_api(cred_file_path)
        self._spreadsheet_id = spreadsheet_id

        self._check_get_data()

    def get_data(self, ranges):
        results = (
            self._api.spreadsheets()
            .values()
            .batchGet(
                spreadsheetId=self._spreadsheet_id,
                ranges=ranges,
                valueRenderOption='FORMATTED_VALUE',
                dateTimeRenderOption='FORMATTED_STRING',
            )
            .execute()
        )
        rows = results['valueRanges'][0]['values']

        return rows

    def _check_get_data(self):
        ranges = 'birthdays'
        try:
            self.get_data(ranges)
        except BaseException as e:
            logging.exception('Failed to check google sheets client')
            raise CheckFailed() from e

        logging.info('Google sheets client check passed')
