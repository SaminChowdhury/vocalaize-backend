from app import api2
from flask_restx import Resource, fields
from flask import request
from services.getLanguageOptionsService import getLanguageOptionsService

language_model = api2.model(
    "Languages",
    {
        "language_name": fields.String,
        "nlp_code": fields.String
    }
)

@api2.route('/languages')
class LanguageOptionsResource(Resource):
    @api2.marshal_list_with(language_model)
    def get(self):
        """Get all Language Options"""
        languages = getLanguageOptionsService()
        return languages
