from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import current_user
from flask_login import login_required
from models.account_model import Account
from connectors.db import Session
from services.user_service import role_required
accountBp = Blueprint('account', __name__)

@accountBp.route('/account', methods=['GET'])
@login_required
@role_required('admin')
def get_accounts():
    try:
        accounts = Account.query.all()
        return jsonify([{'id': account.id, 'balance': account.balance, 'account_type': account.account_type, 'account_number': account.account_number} for account in accounts]), 200
    except Exception as e:
        print(e)
        return 'Error fetching accounts. Please try again later.', 500
    
@accountBp.route('/account/<int:account_id>', methods=['GET'])
@login_required
# @role_required('admin')
def get_account(id):
    try:
        account = Account.query.get(id)
        return jsonify({'id': account.id, 'balance': account.balance, 'account_type': account.account_type, 'account_number': account.account_number}), 200
    except Exception as e:
        print(e)
        return 'Error fetching account. Please try again later.', 500

# @accountBp.route('/account/:id', methods=['GET'])
# @login_required
# def get_account_by_id(id):
#     try:
#         account = Account.query.get(id)
#         return jsonify({'id': account.id, 'balance': account.balance, 'account_type': account.account_type, 'account_number': account.account_number}), 200
#     except Exception as e:
#         print(e)
#         return 'Error fetching account. Please try again later.', 500

@accountBp.route('/account/create', methods=['POST'])
@login_required
@role_required('admin')
def crerate_account():
    balance = request.form.get('balance')
    account_type = request.form.get('account_type')
    account_number = request.form.get('account_number')

    try:
        with Session() as session:
            account = Account(balance=balance, account_type=account_type, account_number=account_number)
            session.add(account)
            session.commit()
            return 'Account successfully created!',200
    except Exception as e:
        print(e)
        return 'Error creating account. Please try again later.', 500

@accountBp.route('/account/update', methods=['PUT'])
@login_required
@role_required('admin')
def update_account():
    try:
        account = Account.query.get(current_user.id)
        account.balance = request.form.get('balance')
        account.account_type = request.form.get('account_type')
        account.account_number = request.form.get('account_number')
        session.commit()
        return 'Account updated successfully', 200
    except Exception as e:
        print(e)
        return 'Error updating account. Please try again later.', 500
    
@accountBp.route('/account/delete', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_account():
    try:
        with Session() as session:
            account = Account.query.get(current_user.id)
            session.delete(account)
            session.commit()
            return 'Account deleted successfully', 200
    except Exception as e:
        print(e)
        return 'Error deleting account. Please try again later.', 500
