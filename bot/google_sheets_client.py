import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsClient:
    def _create_api(credentials_file_path: str):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file_path,
            [
                'https://www.googleapis.com/auth/spreadsheets',
            ],
        )

        httpAuth = credentials.authorize(httplib2.Http())
        return apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    def __init__(self, credentials_file_path: str, spreadsheet_id: str)
        self._api = _create_api(credentials_file_path)
        self._spreadsheet_id = spreadsheet_id

        # try read to check access rights

