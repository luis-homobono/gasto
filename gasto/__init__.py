from flask import Flask
from gasto.config import Config
from gasto.extensions import db


def create_app() -> Flask:
    """Create Flask App

    Returns:
        Flask: Instance of Flask app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    register_blueprints(app=app)
    install_extensions(app=app)

    return app


def register_blueprints(app: Flask):
    """Register Blueprints

    Args:
        app (Flask): Flask app
    """
    from gasto.blueprints.core.views import core
    from gasto.blueprints.error_pages.views import error_pages

    app.register_blueprint(error_pages)
    app.register_blueprint(core, url_prefix="/")


def install_extensions(app: Flask):
    """Install extensions for third-party

    Args:
        app (Flask): Flask app
    """
    db.init_app(app=app)

    with app.app_context():
        db.create_all()
