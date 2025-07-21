import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config import spreadsheet_backend_id,url_base_range


class SheetsIntegration:

    def __init__(self, gsheet_id, gsheet_range):
        self.SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        self.USE_ENV_CREDS = False  # Set to True if you're using environment-based auth (e.g. on GCP)
        self.spreadsheet_id = gsheet_id
        self.spreadsheet_range = gsheet_range


    def add_job_entry(self, job_entry):
        try:
            creds = self.backend_authentication();
            service = build("sheets", "v4", credentials=creds)

            # 2D array: one row, two columns
            row = [[job_entry.company, job_entry.req_id, job_entry.title, job_entry.date_posted, job_entry.apply_url, job_entry.description, "Nuh uh"]]

            # Append the row
            result = service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=self.spreadsheet_range,
                valueInputOption="RAW",
                body={"values": row}
            ).execute()

            updates = result.get("updates", {})
            print(f"Added row to {updates.get('updatedRange')}")
            return True

        except HttpError as error:
            print(f"Google Sheets API error: {error}")
            return []


    def delete_completed_application(self, row_index):
        try:
            creds = self.backend_authentication();
            service = build("sheets", "v4", credentials=creds)

            body = {
                "requests": [
                    {
                        "deleteDimension": {
                            "range": {
                                "sheetId": self.spreadsheet_id,
                                "dimension": "ROWS",
                                "startIndex": row_index,
                                "endIndex": row_index + 1
                            }
                        }
                    }
                ]
            }

            response = service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()

            print(f"Deleted row at index {row_index}.")
            return response

        except HttpError as error:
            print(f"Google Sheets API error: {error}")
            return []


    def add_endpoint_to_sheet(self, new_organization, new_json_url):
        try:
            # Choose auth method
            creds = self.backend_authentication()

            service = build("sheets", "v4", credentials=creds)

            row = [[new_organization, new_json_url]]  # 2D array: one row, two columns
            # Append the row
            result = service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=self.spreadsheet_range,
                valueInputOption="RAW",
                body={"values": row}
            ).execute()

            updates = result.get("updates", {})
            #print(f"Added row to {updates.get('updatedRange')}")
            return True

        except HttpError as error:
            print(f"Google Sheets API error: {error}")
            return []


    def backend_authentication(self):
        if self.USE_ENV_CREDS:
            creds, _ = google.auth.default()
        else:
            creds = None
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                    creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
        return creds


    def get_endpoints_from_sheet(self):
        try:
            # Choose auth method
            creds = self.backend_authentication()

            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.spreadsheet_range).execute()
            values = result.get("values", [])

            if not values:
                print("No Job Website Endpoints Found.")
                return []

            # Expecting format: [company, url]
            endpoints = []
            for row in values:
                if len(row) >= 2:
                    endpoints.append({"company": row[0], "url": row[1]})
            print(f"{len(endpoints)} Job Website Endpoints Retrieved.")
            return endpoints

        except HttpError as error:
            print(f"Google Sheets API error: {error}")
            return []

############ EXAMPLE USAGES ##################
#gsheet = SheetsIntegration(spreadsheet_backend_id, url_base_range)

# ADD a website endpoint to the google sheet
# endpoints = gsheet.add_endpoint_to_sheet("Broadcom", "https://broadcom.wd1.myworkdayjobs.com/wday/cxs/broadcom/External_Career/jobs")

# GET all the website endpoints from the sheet
# endpoints = gsheet.get_endpoints_from_sheet()
# for ep in endpoints:
#    print(f"{ep['company']}: {ep['url']}")



