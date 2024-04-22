# controllers/translationController.py
from flask import request
from flask_restx import Resource, Namespace, fields
from services.updateTranslationService import update_translation_service
from app import api2

update_translation_model = api2.model('UpdateTranslation', {
    'input_drive_path': fields.String(description='New Input Google Drive Path'),
    'output_drive_path': fields.String(description='New Output Google Drive Path')
})

@api2.route('/translation/<int:translation_id>/update')
class UpdateTranslationResource(Resource):
    @api2.expect(update_translation_model)
    def put(self, translation_id):
        """Update the Google Drive paths for an existing translation"""
        data = request.json
        return update_translation_service(translation_id, **data)
