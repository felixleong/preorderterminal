import httplib2
import os
import logging

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


_logger = logging.getLogger('preorder.googlesheets')


class GoogleSheets(object):
    """Google Sheets API handler class."""

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-{app_id}.json
    _SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    _CLIENT_SECRET_FILE = 'client_secret.json'

    def __init__(self, app_id, app_name, spreadsheet_id):
        self.app_id = app_id
        self.app_name = app_name
        self.spreadsheet_id = spreadsheet_id

        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                         'version=v4')
        self.service = discovery.build(
            'sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    def _get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        :returns: Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(
            credential_dir,
            'sheets.googleapis.com-{}.json'.format(self.app_id))

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self._CLIENT_SECRET_FILE, self._SCOPES)
            flow.user_agent = self.app_name
            credentials = tools.run_flow(flow, store)
            _logger.info('Storing credentials to {}'.format(credential_path))
        return credentials

    def write_rows(self, sheet_range, values=[]):
        """Write rows in the Google Sheet.

        :param str sheet_range: A1 notation of the sheet range.
        :param list values: A list of rows, which a row is a list of raw data.
        """
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_range,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body).execute()
        return result


if __name__ == '__main__':
    """
    A simple script to set up the Google Sheet API credentials.
    """
    import sys

    app_id = sys.argv.pop()
    sheet = GoogleSheets(
        app_id, 'Google Sheets API Quickstart',
        '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms')
