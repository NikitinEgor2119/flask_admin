from flask import Flask
from flask_migrate import Migrate
from project_root import create_app, db, migrate  # Импортируем Migrate из __init__.py
from flask.cli import FlaskGroup

app = create_app()  # создаём приложение
migrate.init_app(app, db)  # Инициализируем миграцию с приложением и базой данных

cli = FlaskGroup(create_app=create_app)  # создаём объект CLI

@cli.command("create-admin")
def create_admin():
    # код для создания админа
    print("Admin created successfully.")

if __name__ == "__main__":
    cli()
