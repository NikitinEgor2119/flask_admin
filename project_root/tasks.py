from datetime import datetime, timedelta
from . import db, create_app
from .models import Transaction

app = create_app()

@app.celery.task
def expire_transactions():
    with app.app_context():
        # Время, после которого транзакции истекают
        expiration_time = datetime.utcnow() - timedelta(minutes=10)

        # Поиск транзакций со статусом 'waiting' и временем создания более старым
        transactions = Transaction.query.filter(
            Transaction.status == 'waiting',
            Transaction.created_at < expiration_time
        ).all()

        for transaction in transactions:
            transaction.status = 'expired'
            db.session.add(transaction)

        db.session.commit()
