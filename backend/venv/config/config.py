from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)

class DevConfig(Config):
    DB_USER = 'admin'
    DB_PASSWORD = 'mypassword'
    DB_HOST = 'vocal.czo0uksuylah.us-east-2.rds.amazonaws.com'
    DB_NAME = 'vocal'  # Replace 'your_database_name' with your actual database name

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_ECHO = True
    DEBUG = True

class ProdConfig(Config):
    # You can set up production configuration here
    pass

class TestConfig(Config):
    # You can set up testing configuration here
    pass
