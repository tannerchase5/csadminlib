from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient import errors
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from os.path import exists

def get_Service(OAuth_Creds_path:str, scopes:str, token_path:str, API:str, API_Version:str):
    assert exists(OAuth_Creds_path), "Ensure that OAuth (json) Creds path exists!"

    token = None
    if exists(token_path):
        token = Credentials.from_authorized_user_file(token_path, scopes)

    if (not token) or (not token.valid):
        if token and token.expired and token.refresh_token:
            token.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(OAuth_Creds_path, scopes)
            token = flow.run_console()
        with open(token_path, 'w') as token_file:
            token_file.write(token.to_json())

    try:
        service = build(API, API_Version, credentials=token)
        return service
    except errors.HttpError as error:
        print(error.content)

def sendmail(subject:str, toAdd:str, body:str, log_path:str=None, creds_dir_path:str='creds'):
    message = MIMEMultipart()
    message['to'] = toAdd
    message['subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    message = {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    API = 'gmail'
    API_VERSION = 'v1'
    OAUTH_CREDS = creds_dir_path + '/oauth.json'
    TOKEN = creds_dir_path + '/token.json'
    service = get_Service(OAUTH_CREDS, SCOPES, TOKEN, API, API_VERSION)

    try:
        send = service.users().messages().send(userId='me', body=message).execute()
        print('Message Id: %s' % send['id'])
        if log_path:
            with open(log_path, 'a+') as log:
                log.write("To: %s\nSubject: %s\nBody: %s\n\n" % (toAdd, subject, body))
    except errors.HttpError as error:
        print('An error occurred: %s' % error)