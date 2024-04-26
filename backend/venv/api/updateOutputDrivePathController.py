from flask import request, jsonify
from flask_restx import Resource
from services.translation_service import update_output_drive_path
from app import api2

@api2.route('/update-output-path/<int:translation_id>')
class UpdateOutputPath(Resource):
    def put(self, translation_id):
        # Parse the new output drive path from the request body
        data = request.get_json()
        output_drive_path = data.get('output_drive_path')

        if not output_drive_path:
            return {'error': 'No output drive path provided'}, 400

        # Call the service function to update the output drive path in the database
        try:
            success = update_output_drive_path(translation_id, output_drive_path)
            if success:
                return {'message': 'Output drive path updated successfully'}, 200
            else:
                return {'error': 'Failed to update output drive path'}, 404
        except Exception as e:
            return {'error': str(e)}, 500