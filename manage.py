from app import app, db
from flask.cli import FlaskGroup
from app.models import User

cli = FlaskGroup(app)

@cli.command("create-admin")
def create_admin():
    admin = User(balance=0, commission_rate=0.0, webhook_url=None, role="admin")
    db.session.add(admin)
    db.session.commit()
    print("Admin created successfully.")

if __name__ == "__main__":
    cli()