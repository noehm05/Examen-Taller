
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app.models import modelos

with app.app_context():
    appbuilder = AppBuilder(app, db.session)

    from app.views import vistas
    from app.views import reportes
    from app.views import asistente
