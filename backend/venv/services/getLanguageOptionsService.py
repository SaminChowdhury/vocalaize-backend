from config.exts import db
from sqlalchemy.sql import text

def getLanguageOptionsService():
    query = text(
        "SELECT language_name, nlp_code FROM Language"
    )
    language_options = db.session.execute(query).fetchall()
    return language_options
