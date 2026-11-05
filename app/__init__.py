
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder

from config import Config


# CREAR APLICACION
app = Flask(__name__)
app.config.from_object(Config)


# CONECTAR BASE DE DATOS
db = SQLAlchemy(app)


# IMPORTAR MODELOS
from app.models import modelos


# INICIALIZAR FLASK-APPBUILDER
with app.app_context():

    appbuilder = AppBuilder(app, db.session)

    # IMPORTAR VISTAS CRUD
    from app.views import vistas

    # IMPORTAR REPORTES
    from app.views import reportes
