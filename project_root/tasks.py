# project_root/tasks.py
from celery import Celery
from datetime import datetime, timedelta
from . import db
from .models import Transaction
import requests

celery = Celery('tasks', broker='redis://localhost:6379/0')


@celery.task
def check_expired_transactions():
    expiration_time = datetime.utcnow() - timedelta(minutes=15)
    transactions = Transaction.query.filter(Transaction.status == 'waiting',
                                            Transaction.created_at < expiration_time).all()

    for transaction in transactions:
        transaction.status = 'expired'
        db.session.commit()

        # Отправить webhook
        if transaction.user.webhook_url:
            requests.post(transaction.user.webhook_url, json={"transaction_id": transaction.id, "status": "expired"})
