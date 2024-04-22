# services/createTranslationService.py
from sqlalchemy.sql import text
from config.exts import db

def create_translation_service(data):
    try:
        # Start the transaction
        db.session.begin()

        # Insert the new audio translation
        insert_query = text("""
            INSERT INTO audio_translations (user_id, input_drive_path, output_drive_path, source_language, target_language)
            VALUES (:user_id, :input_drive_path, :output_drive_path, :source_language, :target_language);
        """)
        db.session.execute(insert_query, {
            'user_id': data['user_id'],
            'input_drive_path': data['input_drive_path'],
            'output_drive_path': data['output_drive_path'],
            'source_language': data['source_language'],
            'target_language': data['target_language']
        })

        # Fetch the last inserted ID
        last_id_query = text("SELECT LAST_INSERT_ID();")
        result = db.session.execute(last_id_query)
        translation_id = result.fetchone()[0]

        db.session.commit()
        return {"message": "Translation created successfully", "translation_id": translation_id}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
