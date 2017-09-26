from flask import Flask
from views import mod


def create_app(config, app_name):
    app = Flask(app_name)
    app.config.from_object(config)
    app.register_blueprint(mod)
    return app
