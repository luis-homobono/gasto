from flask import Flask

from gasto.config import Config
from gasto.models import User
from gasto.extensions import db, migrate, login_manager


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
    from gasto.blueprints.users.views import users
    from gasto.blueprints.error_pages.views import error_pages

    app.register_blueprint(users)
    app.register_blueprint(error_pages)
    app.register_blueprint(core, url_prefix="/")


def install_extensions(app: Flask):
    """Install extensions for third-party

    Args:
        app (Flask): Flask app
    """
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app=app)
    login_manager.login_view = "blueprints.users.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
