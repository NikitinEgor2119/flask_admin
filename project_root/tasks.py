from datetime import datetime
import requests
from . import celery, db
from .models import Transaction

@celery.task
def check_transactions():
    now = datetime.utcnow()
    transactions = Transaction.query.filter_by(status="waiting").all()
    for transaction in transactions:
        if (now - transaction.created_at).seconds > 900:  # 15 minutes
            transaction.status = "expired"
            db.session.commit()
            if transaction.user.webhook_url:
                requests.post(transaction.user.webhook_url, json={"id": transaction.id, "status": "expired"})