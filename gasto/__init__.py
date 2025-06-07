from flask import Flask
from gasto.config import Config


def create_app() -> Flask:
    """Create Flask App

    Returns:
        Flask: Instance of Flask app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    register_blueprints(app=app)

    return app


def register_blueprints(app: Flask):
    """Register Blueprints

    Args:
        app (Flask): Flask app
    """
    from gasto.blueprints.core.views import core

    app.register_blueprint(core, url_prefix="/")
