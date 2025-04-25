from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# Instancia global de SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Crear la instancia de la app Flask
    app = Flask(
        __name__,
        template_folder='templates',  # Ruta explícita a los templates
        static_folder='static'        # Carpeta para archivos estáticos
    )

    # Configuraciones esenciales
    app.config['SECRET_KEY'] = 'clave-secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quadra.db'
    app.config['SESSION_TYPE'] = 'filesystem'

    # Inicializar extensiones
    Session(app)
    db.init_app(app)

    # Importar y registrar blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
