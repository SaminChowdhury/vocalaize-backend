from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from config.exts import db
from config.config import DevConfig

app=Flask(__name__)
CORS(app)
app.config.from_object(DevConfig)
db.init_app(app)
api2=Api(app,doc='/docs')
def createApp():
    app=Flask(__name__)
    app.app_context().push()
    CORS(app)
    app.config.from_object(DevConfig)
    db.init_app(app)
    api2=Api(app,doc='/docs')
import api