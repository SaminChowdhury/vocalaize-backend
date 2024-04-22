# services/getTranslationInfoService.py
from sqlalchemy.sql import text
from config.exts import db

def get_translation_info(translation_id):
    try:
        query = text("""
            SELECT 
                translation_id, user_id, input_drive_path, output_drive_path, 
                source_language, target_language, created_at, updated_at 
            FROM 
                audio_translations 
            WHERE 
                translation_id = :translation_id;
        """)
        result = db.session.execute(query, {'translation_id': translation_id})
        translation_info = result.fetchone()

        if translation_info:
            # Create a dictionary with the correct indices if required
            translation_dict = {
                'translation_id': translation_info[0],
                'user_id': translation_info[1],
                'input_drive_path': translation_info[2],
                'output_drive_path': translation_info[3],
                'source_language': translation_info[4],
                'target_language': translation_info[5],
                'created_at': translation_info[6].isoformat() if translation_info[6] else None,
                'updated_at': translation_info[7].isoformat() if translation_info[7] else None,
            }
            return translation_dict
        else:
            return None
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}
