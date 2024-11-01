from flask import Blueprint, jsonify, redirect, request, session, url_for
from flask_login import login_required, login_user, logout_user
from models.user_model import User
from connectors.db import Session
import datetime
from flask_jwt_extended import create_access_token, current_user, get_jwt_identity, jwt_required, unset_jwt_cookies
from services.user_service import role_required
from extensions import db

userBp =Blueprint('user', __name__) 

@userBp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Please fill all fields'}), 400
    
    try:
        with Session() as session:
            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            
            return jsonify({'message': 'User successfully created!'}),200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': 'Error creating user. Please try again later.'}), 500

    
    
@userBp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'Please fill all fields'}), 400

    try:
        with Session() as session:
            user = session.query(User).filter(User.email == email).first()
            isCorrectUser = user and user.check_password(password)
            

            if isCorrectUser:
                login_user(user)
                expires = datetime.timedelta(days=1)
                access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'email': user.email}, expires_delta=expires)
                return jsonify({'Login successful'}), 200
            else:
                return jsonify({'Invalid email or password'}), 401
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'Error logging in. Please try again later.'}), 500
    
@userBp.route('/logout', methods=['POST'])
@login_required
@jwt_required()
def logout():
    try:
        response = 'Logout successful', 200
        logout_user()
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify({'Error logging out. Please try again later.'}), 500

@userBp.route('/users/me', methods=['GET'])
@login_required
@jwt_required()
def user_me():
    current_user = get_jwt_identity
    try:
        data = request.get_json()
        user = User.query.get(current_user.id)
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'Error fetching user. Please try again later.'}), 500

@userBp.route('/users', methods=['GET'])
@login_required
@jwt_required()
# @role_required('admin')
def get_users():
    try:
        data = request.get_json()
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users]), 200
    except Exception as e:
        print(e)
        return jsonify({'Error fetching users. Please try again later.'}), 500

@userBp.route('/users/update', methods=['PUT'])
@login_required
@jwt_required()
def update_user():
    current_user = get_jwt_identity
    try:
        data = request.get_json()
        user = User.query.get(current_user.id)
        user.username = data.get('username')
        user.email = data.get('email')
        db.session.commit()
        return jsonify({'User updated successfully'}), 200
    except Exception as e:
        print(e)
        db.session.rollback
        return jsonify({'Error updating user. Please try again later.'}), 500