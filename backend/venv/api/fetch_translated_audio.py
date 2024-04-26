from flask import send_file
from googleapiclient.http import MediaIoBaseDownload
import io
from flask_restx import Resource, Api, Namespace
from services.drive_service import authenticate_drive, get_file_info, download_file_by_id
from app import api2

@api2.route('/download-file/<int:user_id>/<int:translation_id>')
class FileDownload(Resource):
    def get(self, user_id, translation_id):
        service = authenticate_drive()
        
        # Fetch the file information
        file_info = get_file_info(user_id, translation_id)
        if not file_info:
            return {'error': 'File information not found'}, 404

        # Download the file using Google Drive API
        file_stream = download_file_by_id(service, file_info['output_drive_path'])
        if file_stream:
            file_stream.seek(0)
            return send_file(
                file_stream,
                as_attachment=True,
                download_name=f"{file_info['output_drive_path']}.wav",  # Correct usage of the filename parameter
                mimetype='audio/wav'  # Adjust MIME type according to file type
            )
        else:
            return {'error': 'File not found'}, 404
