from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json, requests 

#ランキングを取得する
url = requests.get("https://anime.dmkt-sp.jp/animestore/rest/WS000103?rankingType=01")
text = url.text #ランキングのデータをテキストとして取得
data = json.loads(text) #テキストをJSONに変換

array = [] #ランキングを格納する配列を生成
array.clear()

for i in range(0, 300): #ランキング（タイトル名のみ）を配列に格納する
  title = data["data"]['workList'][i]['workInfo']['workTitle']
  array.append(title)

#スプレッドシートにデータを移す

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'スプレッドシートID'
RANGE_NAME = 'Sheet1!B3' #出力するセル

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

#スプレッドシートに書き込む情報・形式
values = [array]
body = {
    'values': values,
    'majorDimension' : 'COLUMNS', #縦方向に出力する
    }

#スプレッドシートに書き込む
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=RANGE_NAME,
    valueInputOption = 'USER_ENTERED',
     body=body).execute()

#print('success')

