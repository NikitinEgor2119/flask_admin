# app.py или __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

# Инициализация объектов
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Создание объекта приложения Flask
    app = Flask(__name__)

    # Настройки приложения
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Указание на Redis

    # Инициализация расширений
    db.init_app(app)  # Инициализируем базу данных
    migrate.init_app(app, db)  # Инициализируем миграции

    # Регистрация Blueprint
    from .routes import bp
    app.register_blueprint(bp)

    # Настройка Celery
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])  # Создаем экземпляр Celery
    celery.conf.update(app.config)  # Обновляем конфигурацию Celery с конфигурацией Flask

    return app
