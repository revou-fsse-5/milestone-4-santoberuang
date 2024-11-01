from decimal import Decimal
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import login_required
from models.transaction_model import Transaction
from models.account_model import Account
from services.user_service import role_required
from extensions import db
# from connectors.db import Session


transactionBp = Blueprint('transactions', __name__)

@transactionBp.route('/transactions', methods=['GET'])
@login_required
@jwt_required()
@role_required('admin')
def get_transactions():
    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        transaction = Transaction.query.all()
        return jsonify({'message': 'Transactions fetched successfully', 'transactions': transaction}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'Error fetching transactions. Please try again later.'}), 500
        
@transactionBp.route('/transactions/create', methods=['POST'])
@login_required
@jwt_required()
def create_transaction():
    current_user = get_jwt_identity()
    data = request.get_json()

    from_account = Account.query.get(data.get('from_account_id'))
    to_account = Account.query.get(data.get('to_account_id'))
    description = data.get('description')

    if not from_account or not to_account:
        return jsonify({'error': 'account is not found'}), 400

    amount = Decimal(data.get('amount'))

    if from_account.balance < amount:
        return jsonify({'error': 'Insufficient balance'}), 400
    

    try:
        # with Session() as session:
            transaction = Transaction(from_account_id=from_account.id, to_account_id=to_account.id, amount=amount, type=data['type'], description=description)
            
            from_account.balance -= amount
            to_account.balance += amount
            
            db.session.add(transaction)
            db.session.commit()
            return jsonify({'message': 'Transaction successfully created!'}),200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': 'Error creating transaction. Please try again later.'}), 500
    
@transactionBp.route('/transactions/<int:transaction_id>', methods=['GET'])
@login_required
@jwt_required()
def get_transaction(id):
    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        transaction = Transaction.query.get(id)
        return jsonify({'message': 'Transaction fetched successfully', 'transaction': transaction}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'Error fetching transaction. Please try again later.'}), 500