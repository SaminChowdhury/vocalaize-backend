from googleapiclient.http import MediaIoBaseDownload
import io
from sqlalchemy.sql import text

# Assuming you've set this up as described in previous messages
def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh
from google.oauth2 import service_account
from googleapiclient.discovery import build

def authenticate_drive():
    SERVICE_ACCOUNT_FILE = 'config/service.json'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Load the service account credentials from the JSON file
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Build the service object for the Drive API
    service = build('drive', 'v3', credentials=credentials)
    return service
def find_and_download_file_by_name(service, folder_id, file_name):
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        return None
    file_id = items[0]['id']
    return download_file(service, file_id)
from config.exts import db
from sqlalchemy.sql import text



from sqlalchemy.sql import text
from config.exts import db

def get_file_info(user_id, translation_id):
    query = text("""
        SELECT output_drive_path FROM audio_translations
        WHERE user_id = :user_id AND translation_id = :translation_id AND output_drive_path IS NOT NULL
        ORDER BY created_at DESC LIMIT 1;
    """)
    result = db.session.execute(query, {'user_id': user_id, 'translation_id': translation_id}).fetchone()
    
    # Handle the response properly by checking if a result exists
    if result:
        # Convert result which is a RowProxy to a dictionary if you're expecting a dictionary access
        return {'output_drive_path': result[0]}  # Access by index as result is likely a tuple
    else:
        return None  # Or an appropriate response indicating no data found


def download_file(service, file_id):
    """Download a file from Google Drive given its file ID."""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}% complete.")
    fh.seek(0)
    return fh
def download_file_by_id(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh