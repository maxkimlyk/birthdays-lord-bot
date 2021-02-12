import enum
import logging
import os
from typing import Mapping, Any, List

import httplib2  # type: ignore
import apiclient.discovery  # type: ignore
import oauth2client.service_account  # type: ignore
import googleapiclient.errors  # type: ignore


class CheckFailed(BaseException):
    pass


class SpreadsheetCheckResult(enum.Enum):
    OK = 0
    NO_ACCESS = 1
    NOT_FOUND = 2


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
        self._api = self._create_api(cred_file_path)

    def get_data(
            self, spreadsheet_id: str, ranges: List[str],
    ) -> List[List[str]]:
        results = (
            self._api.spreadsheets()
            .values()
            .batchGet(
                spreadsheetId=spreadsheet_id,
                ranges=ranges,
                valueRenderOption='FORMATTED_VALUE',
                dateTimeRenderOption='FORMATTED_STRING',
            )
            .execute()
        )
        rows = results['valueRanges'][0]['values']

        return rows

    def check_spreadsheet(self, spreadsheet_id: str) -> SpreadsheetCheckResult:
        ranges = ['birthdays']
        try:
            self.get_data(spreadsheet_id, ranges)
        except googleapiclient.errors.HttpError as e:
            if e.resp.status == 403:
                logging.info(
                    'No permission to given spreadsheet with id: %s',
                    spreadsheet_id,
                )
                return SpreadsheetCheckResult.NO_ACCESS
            if e.resp.status == 404:
                logging.info(
                    'Not found given spreadsheet with id: %s', spreadsheet_id,
                )
                return SpreadsheetCheckResult.NOT_FOUND
            logging.exception(
                'Failed to check spreadsheet with id %s due to unknown reason',
                spreadsheet_id,
            )
            raise

        logging.info(
            'Check passed for spreadsheet with id: %s', spreadsheet_id,
        )
        return SpreadsheetCheckResult.OK
