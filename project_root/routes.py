from flask import request, jsonify
from . import app, db
from .models import User, Transaction

@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    commission = amount * user.commission_rate
    transaction = Transaction(amount=amount, commission=commission, user_id=user_id)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction created", "id": transaction.id}), 201


@app.route('/cancel_transaction', methods=['POST'])
def cancel_transaction():
    data = request.json
    transaction_id = data.get('transaction_id')
    transaction = Transaction.query.get(transaction_id)

    if not transaction or transaction.status != 'waiting':
        return jsonify({"error": "Transaction cannot be cancelled"}), 400

    transaction.status = 'cancelled'
    db.session.commit()

    return jsonify({"message": "Transaction cancelled"})


@app.route('/check_transaction', methods=['GET'])
def check_transaction():
    transaction_id = request.args.get('transaction_id')
    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify({"id": transaction.id, "status": transaction.status})