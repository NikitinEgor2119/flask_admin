from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from celery import Celery
from flask_swagger_ui import get_swaggerui_blueprint

from .routes import api

db = SQLAlchemy()
migrate = Migrate()
celery = Celery()

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    celery.conf.update(app.config)

    # Admin setup
    admin = Admin(app, name="Admin Panel", template_mode="bootstrap4")

    # Swagger setup
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Import and register blueprints
    from .routes import api
    app.register_blueprint(api)

    return app
