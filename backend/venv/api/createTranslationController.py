# controllers/createTranslationController.py
from flask_restx import Resource, fields, Namespace
from services.createTranslationService import create_translation_service
from app import api2


translation_model = api2.model('AudioTranslation', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'input_drive_path': fields.String(required=True, description='Input Drive Path'),
    'output_drive_path': fields.String(required=True, description='Output Drive Path'),
    'source_language': fields.String(required=True, description='Source Language'),
    'target_language': fields.String(required=True, description='Target Language')
})

@api2.route('/create/translation')
class CreateTranslationResource(Resource):
    @api2.expect(translation_model)
    def post(self):
        """Create a new translation record"""
        data = api2.payload
        return create_translation_service(data)
