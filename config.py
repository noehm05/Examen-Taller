
import os
from dotenv import load_dotenv
from flask_appbuilder.security.manager import AUTH_DB

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "jehiely-clave-desarrollo-2026")

    # Configuración de la base de datos MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASSWORD', '')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'jehiely_db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Autenticación mediante base de datos
    AUTH_TYPE = AUTH_DB
