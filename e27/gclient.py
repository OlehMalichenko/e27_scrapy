import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from pprint import pprint

class Gclient(object):

    def __init__(self):
        self.client = self.create_client()


    def create_client(self):
        scope = ['https://spreadsheets.google.com/feeds']
        path = os.getcwd() + '\client_secret.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        return gspread.authorize(creds)


    def get_sheet_url(self):
        return self.client.open_by_key('1GdnOjWJEdnNuAgvRihkVDKSky9ZyQawif3l4hAQ4OoQ').get_worksheet(1)


    def get_sheet_result(self):
        return self.client.open_by_key('1GdnOjWJEdnNuAgvRihkVDKSky9ZyQawif3l4hAQ4OoQ').get_worksheet(2)