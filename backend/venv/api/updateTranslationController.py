# controllers/translationController.py
from flask import request
from flask_restx import Resource, Namespace, fields
from services.updateTranslationService import update_output_path_service
from app import api2




# Define the expected payload structure
update_output_path_model = api2.model('UpdateOutputPath', {
    'output_drive_path': fields.String(required=True, description='New Output Google Drive Path')
})

@api2.route('/translation/<int:translation_id>')
class UpdateOutputPathResource(Resource):
    @api2.expect(update_output_path_model)
    def put(self, translation_id):
        """Update the output Google Drive path for an existing translation"""
        data = request.json
        return update_output_path_service(translation_id, data['output_drive_path'])

