from importlib import import_module

from flask import Flask

from src.blueprint import all_blueprints
import src.configuration as config
from src.core.filters import ALL_FILTERS
from src.extensions import init_extensions


def create_app():
    """Create an instance of the app."""
    app = Flask(__name__)

    # Load the app configuration
    app.config.update(config.get_app_config("default"))
    app.config.update(config.get_app_config(app.config["ENV"]))

    # Put the app secret key into the expected key
    app.config["SECRET_KEY"] = app.config["SECRET_KEY_ADMIN"]
    del app.config["SECRET_KEY_ADMIN"]

    # Load the extensions
    init_extensions(app)

    # Load any injection/special app handler methods
    with app.app_context():
        import_module("src.middleware")

    # Register all of the blueprints
    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)

    # Register the filters
    for name, method in ALL_FILTERS.items():
        app.add_template_filter(method, name=name)

    return app
