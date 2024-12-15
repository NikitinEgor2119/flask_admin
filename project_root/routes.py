# project_root/routes.py
from flask import Blueprint, render_template, request, jsonify
from .models import User, Transaction
from . import db

bp = Blueprint('main', __name__)

# Маршрут для страницы дашборда
@bp.route('/dashboard')
def dashboard():
    user_count = User.query.count()
    transaction_count = Transaction.query.count()
    total_transactions = db.session.query(db.func.sum(Transaction.amount)).scalar() or 0
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', user_count=user_count, transaction_count=transaction_count,
                           total_transactions=total_transactions, recent_transactions=recent_transactions)

# Маршрут для страницы пользователей
@bp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Маршрут для страницы транзакций
@bp.route('/transactions')
def transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)

# API метод для создания транзакции
@bp.route('/create_transaction', methods=['POST'])
def create_transaction():
    # Проверка, что запрос содержит JSON-данные
    if not request.is_json:
        return jsonify({"error": "Invalid content type, application/json required"}), 400

    # Извлекаем данные из тела запроса
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')

    # Проверка наличия обязательных полей
    if not user_id or not amount:
        return jsonify({"error": "user_id and amount are required"}), 400

    # Найти пользователя
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Расчет комиссии через метод calculate_commission
    commission = user.calculate_commission(amount)

    # Создание транзакции
    transaction = Transaction(amount=amount, commission=commission, user_id=user_id)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction created", "id": transaction.id}), 201


# API метод для отмены транзакции
@bp.route('/cancel_transaction', methods=['POST'])
def cancel_transaction():
    data = request.json
    transaction_id = data.get('transaction_id')
    transaction = Transaction.query.get(transaction_id)

    if not transaction or transaction.status != 'waiting':
        return jsonify({"error": "Transaction cannot be cancelled"}), 400

    transaction.status = 'cancelled'
    db.session.commit()

    return jsonify({"message": "Transaction cancelled"})

# API метод для проверки статуса транзакции
@bp.route('/check_transaction', methods=['GET'])
def check_transaction():
    transaction_id = request.args.get('transaction_id')
    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify({"id": transaction.id, "status": transaction.status})




