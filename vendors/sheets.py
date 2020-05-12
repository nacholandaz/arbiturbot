from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

spread_url = os.getenv('SPREAD_URL')

KEYS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_headers():
    sheet = client.open_by_url(spread_url)
    try:
        values = sheet.values_get('Sheet1!1:999')['values'][0]
        if values[0] == '': values = []
    except:
        values = []
    return values

def update_headers(new_keys):
    current_headers = get_headers()
    new_keys = list(set(new_keys) - set(current_headers))
    sheet = client.open_by_url(spread_url)
    sheet.values_update(
        'Sheet1!' +KEYS[len(current_headers)]+'1',
        params = {'valueInputOption': 'USER_ENTERED'},
        body = {
            'values':[new_keys]
        }
    )
    return True

def get_sheet_size(sheet):
    try:
        return len(worksheet.get_all_values())
    except:
        return 1

def insert_row(context):
    headers = get_headers()
    print(headers)
    if len(set(list(context.keys()))-set(headers))>0:
        update_headers(context.keys())
        headers=get_headers()
    output = []
    for key in headers:
        if key in context:
            output.append(str(context[key]))
        else:
            output.append('N/A')
    sheet = client.open_by_url(spread_url)
    worksheet = sheet.worksheet('Sheet1')
    worksheet.insert_row(output, get_sheet_size(worksheet)+1)
    return True
