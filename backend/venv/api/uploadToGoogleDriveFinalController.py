from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from werkzeug.utils import secure_filename
import os
from services.uploadToGoogleDriveService import upload_file_to_drive
from services.createTranslationService import create_translation_service
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
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)

        try:
            folder_id = '1-KnlSu6nLfhfmAO8LQUuEtbErH3OgzuH'
            file_id = upload_file_to_drive(filename, file_path, folder_id)

            translation_data = {
                'user_id': request.form.get('user_id'),
                'output_drive_path': request.form.get('output_drive_path')
            }
            try:
                os.remove(file_path)
            except:
                print("No Path")
            return {'message': 'File uploaded'}, 200
        except Exception as e:
            os.remove(file_path)
            return {'error': str(e)}, 500

