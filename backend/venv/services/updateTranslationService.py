# services/updateTranslationService.py
from sqlalchemy.sql import text
from config.exts import db

def update_translation_service(translation_id, input_drive_path=None, output_drive_path=None):
    try:
        # Prepare the query to update the translation paths
        update_fields = []
        params = {'translation_id': translation_id}
        
        if input_drive_path is not None:
            update_fields.append("input_drive_path = :input_drive_path")
            params['input_drive_path'] = input_drive_path

        if output_drive_path is not None:
            update_fields.append("output_drive_path = :output_drive_path")
            params['output_drive_path'] = output_drive_path

        if not update_fields:
            return {"message": "No update parameters provided."}, 400

        update_query = text("""
            UPDATE audio_translations
            SET {}
            WHERE translation_id = :translation_id;
        """.format(", ".join(update_fields)))

        db.session.execute(update_query, params)
        db.session.commit()
        return {"message": "Translation updated successfully."}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
