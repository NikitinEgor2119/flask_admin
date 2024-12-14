from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Добавьте импорт Migrate
from celery import Celery
import os

db = SQLAlchemy()
migrate = Migrate()  # Инициализируем Flask-Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

    db.init_app(app)
    migrate.init_app(app, db)  # Инициализируем миграции

    from .routes import bp
    app.register_blueprint(bp)

    # Celery setup
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    return app
