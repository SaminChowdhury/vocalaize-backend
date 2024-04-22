# controllers/translationController.py
from flask_restx import Resource, Namespace
from services.getTranslationInfoService import get_translation_info
from app import api2




@api2.route('/translation/<int:translation_id>')
class TranslationResource(Resource):
    def get(self, translation_id):
        """Retrieve details for a specific translation ID"""
        translation_info = get_translation_info(translation_id)
        if translation_info:
            return translation_info
        else:
            api2.abort(404, "Translation not found")
