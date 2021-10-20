from __future__ import print_function
from os import system
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = json.load(open('sheetID.json'))['ID']
RANGE_NAME = 'Feuille 1!A2:B10'

def getValues():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    global service
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    return values

def writeValues(rowID, content):
    body = {
        'values': content
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=f'Feuille 1!C{rowID}:C{rowID}',
        valueInputOption="RAW", body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    getValues()