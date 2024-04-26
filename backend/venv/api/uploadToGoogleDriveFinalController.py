from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from werkzeug.utils import secure_filename
import os
from services.uploadToGoogleDriveService import upload_file_to_drive
from app import api2
from services.translation_service import update_output_drive_path
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
        # Ensure directory exists for temporary file storage
        file_path = os.path.join('C:\\tmp', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        try:
            folder_id = '1-KnlSu6nLfhfmAO8LQUuEtbErH3OgzuH'  # Your Google Drive folder ID
            file_id = upload_file_to_drive(filename, file_path, folder_id)  # Upload file to Google Drive

            # Construct the output drive path using the file ID from Google Drive
            output_drive_path = file_id
            translation_id = request.form.get('translation_id', type=int)  # Assuming translation_id is sent as form data

            if not translation_id:
                raise ValueError("Translation ID is required")

            # Update the output drive path for the existing translation record
            success = update_output_drive_path(translation_id, output_drive_path)

            os.remove(file_path)  # Clean up the local file system
            if success:
                return {'message': 'File uploaded and output path updated successfully', 'file_id': file_id, 'drive_path': output_drive_path, 'translation_id': translation_id}, 200
            else:
                return {'error': 'Failed to update the output drive path'}, 400
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)  # Ensure cleanup even if an error occurs
            return {'error': str(e)}, 500