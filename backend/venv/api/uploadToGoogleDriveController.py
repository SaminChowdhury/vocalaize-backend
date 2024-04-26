from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from werkzeug.utils import secure_filename
import os
from services.uploadToGoogleDriveService import upload_file_to_drive
from services.createTranslationService import create_translation_service
from app import api2

# Assuming 'api2' is a valid Namespace object already defined somewhere in your application.

@api2.route('/upload-audio')
class UploadAudio(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        filename = secure_filename(file.filename)
        # Use a directory that exists on Windows, ensure C:\tmp is created or use another valid path
        file_path = os.path.join('C:\\tmp', filename)
        # Make sure the directory exists, if not, create it
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        try:
            folder_id = '1a6q5sEvEBMz7zNSsKRqfolaTlq9L2bvv'
            file_id = upload_file_to_drive(filename, file_path, folder_id)

            translation_data = {
                'user_id': request.form.get('user_id', None),
                'input_drive_path': filename,  # Use file_id as input path for clarity in data
                'output_drive_path': None,
                'source_language': request.form.get('source_language'),
                'target_language': request.form.get('target_language')
            }
            translation_result = create_translation_service(translation_data)
            translation_id = translation_result.get('translation_id')

            os.remove(file_path)

            return {'message': 'File uploaded and translation created', 'translation_id': translation_id}, 200
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return {'error': str(e)}, 500

