from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from werkzeug.utils import secure_filename
import os
from services.uploadToGoogleDriveService import upload_file_to_drive
from app import api2

# Assuming 'api2' is a valid Namespace object already defined somewhere in your application.

@api2.route('/upload-audio-final')
class UploadAudio(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        filename = secure_filename(file.filename)
        # Using Windows compatible path and ensuring the directory exists
        file_path = os.path.join('C:\\tmp', filename)  # Ensure this directory exists or create it
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create the directory if it doesn't exist
        file.save(file_path)

        try:
            folder_id = '1-KnlSu6nLfhfmAO8LQUuEtbErH3OgzuH'  # Your Google Drive folder ID
            file_id = upload_file_to_drive(filename, file_path, folder_id)  # Upload file to Google Drive

            # Building the drive path with file_id instead of filename
            output_drive_path = f"{folder_id}/{file_id}"  # Construct the path with folder_id and file_id

            translation_data = {
                'user_id': request.form.get('user_id', type=int),  # Fetch user_id, assuming it's sent as form data
                'output_drive_path': output_drive_path
            }
            # Here you can further process translation_data as needed

            os.remove(file_path)  # Remove the file after uploading to Google Drive
            return {'message': 'File uploaded', 'file_id': file_id, 'drive_path': output_drive_path}, 200
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)  # Safely remove file only if it exists
            return {'error': str(e)}, 500
