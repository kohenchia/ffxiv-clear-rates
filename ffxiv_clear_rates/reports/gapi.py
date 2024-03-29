from google.oauth2 import service_account
from googleapiclient.discovery import build

# Scopes required to access Google Sheets API
_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleAPI:
    def __init__(self):
        self.initialized = False
        self.GSHEETS = None
        self.GDRIVE = None

    @property
    def sheets(self):
        if not self.initialized:
            raise RuntimeError(
                "Google API is not initialized yet. Please call initialize()."
            )
        return self.GSHEETS

    @property
    def drive(self):
        if not self.initialized:
            raise RuntimeError(
                "Google API is not initialized yet. Please call initialize()."
            )
        return self.GDRIVE

    def initialize(self, creds_file: str):
        # Authenticate with Google Sheets and Drive APIs
        creds = service_account.Credentials.from_service_account_file(
            creds_file, scopes=_SCOPES
        )
        self.GSHEETS = build("sheets", "v4", credentials=creds)
        self.GDRIVE = build("drive", "v3", credentials=creds)
        self.initialized = True


GAPI = GoogleAPI()
