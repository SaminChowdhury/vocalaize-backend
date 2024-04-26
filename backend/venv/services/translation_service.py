from config.exts import db
from sqlalchemy.sql import text

def update_output_drive_path(translation_id, output_drive_path):
    update_query = text("UPDATE audio_translations SET output_drive_path=:output_drive_path WHERE translation_id=:translation_id")
    result = db.session.execute(update_query, {'output_drive_path': output_drive_path, 'translation_id': translation_id})
    db.session.commit()
    return result.rowcount > 0  # True if the update affected at least one row
