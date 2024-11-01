from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import current_user, get_jwt_identity, jwt_required
from flask_login import login_required
from models.account_model import Account
# from connectors.db import Session
from services.user_service import role_required
from extensions import db

accountBp = Blueprint('account', __name__)


@accountBp.route('/accounts', methods=['GET'])
@login_required
@jwt_required()
@role_required('admin')
def get_accounts():
    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        accounts = Account.query.all()
        return jsonify([{'id': account.id, 'balance': account.balance, 'account_type': account.account_type, 'account_number': account.account_number} for account in accounts]), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'Error fetching accounts. Please try again later.'}), 500
    
@accountBp.route('/accounts/<int:account_id>', methods=['GET'])
@login_required
@jwt_required()
# @role_required('admin')
def get_account(id):
    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        account = Account.query.get(id)
        return jsonify({'id': account.id, 'balance': account.balance, 'account_type': account.account_type, 'account_number': account.account_number}), 200
    except Exception as e:
        print(e)
        return jsonify({'Error fetching account. Please try again later.'}), 500


@accountBp.route('/accounts/create', methods=['POST'])
@login_required
@jwt_required()
# @role_required('admin')
def crerate_account():
    current_user = get_jwt_identity()
    data = request.get_json()

    balance = data.get('balance')
    account_type = data.get('account_type')
    account_number = data.get('account_number')

    try:
        # with Session() as session:
            account = Account(balance=balance, account_type=account_type, account_number=account_number)
            db.session.add(account)
            db.session.commit()
            return jsonify({ 'Account successfully created!'}),200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'Error creating account. Please try again later.'}), 500

@accountBp.route('/accounts/update', methods=['PUT'])
@login_required
@jwt_required()
# @role_required('admin')
def update_account():
    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        account = Account.query.get(current_user.id)
        account.balance = data.get('balance')
        account.account_type = data.get('account_type')
        account.account_number = data.get('account_number')
        db.session.commit()
        return jsonify({'Account updated successfully'}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'Error updating account. Please try again later.'}), 500
    
@accountBp.route('/accounts/delete', methods=['DELETE'])
@login_required
@jwt_required()
# @role_required('admin')
def delete_account():
    current_user = get_jwt_identity()
    data = request.get_json()

    try:
        # with Session() as session:
            account = Account.query.get(current_user.id)
            db.session.delete(account)
            db.session.commit()
            return jsonify({'Account deleted successfully'}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'Error deleting account. Please try again later.'}), 500
