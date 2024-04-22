# services/updateTranslationService.py
from sqlalchemy.sql import text
from config.exts import db

def update_output_path_service(translation_id, output_drive_path):
    try:
        update_query = text("""
            UPDATE audio_translations
            SET output_drive_path = :output_drive_path
            WHERE translation_id = :translation_id;
        """)
        db.session.execute(update_query, {
            'translation_id': translation_id,
            'output_drive_path': output_drive_path
        })
        db.session.commit()
        return {"message": "Output drive path updated successfully."}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
