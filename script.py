import gspread
from oauth2client.service_account import ServiceAccountCredentials

def conectar_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1f2zruI_aJ7i9dgjdvekgBSgLlOaIRHN4kdO7tlYMEVY").sheet1
    return sheet