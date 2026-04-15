import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets authentication
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(credentials)

# Change this if your sheet name is different
SHEET_NAME = "fidlefolio_assignment2"


def connect_sheet():
    """Connect to the Google Sheet."""
    sheet = client.open(SHEET_NAME).sheet1
    return sheet


def read_pending_rows():
    """
    Read rows where status is empty or Pending.
    """
    sheet = connect_sheet()
    rows = sheet.get_all_records()

    rows_to_process = []

    for i, row in enumerate(rows, start=2):  # start=2 because row 1 is header

        status = str(row.get("Status", "")).strip()

        if status == "" or status.lower() == "pending":
            row["sheet_row"] = i
            rows_to_process.append(row)

    return rows_to_process


def update_status(row_number, status):
    """Update Status column."""
    sheet = connect_sheet()
    sheet.update_cell(row_number, 6, status)


def update_compliance_flag(row_number, flag):
    """Update Compliance_flag column."""
    sheet = connect_sheet()
    sheet.update_cell(row_number, 7, flag)