from flask import Flask

from config import Config

from .errors import register_error_handlers
from .models import db
from .routes import main_bp


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    app.register_blueprint(main_bp)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
