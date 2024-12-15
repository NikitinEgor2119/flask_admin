from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0)
    commission_rate = db.Column(db.Float, default=0.0)
    webhook_url = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), default='user')
    usdt_wallet = db.Column(db.String(255), nullable=True)  # поле USDT-кошелька

    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def calculate_commission(self, amount):
        return amount * self.commission_rate

    def is_admin(self):
        return self.role == 'admin'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='waiting')  # waiting, confirmed, cancelled, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
