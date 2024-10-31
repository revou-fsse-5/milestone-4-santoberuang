from flask import Blueprint, jsonify, redirect, request, session, url_for
from flask_login import login_required, login_user, logout_user
from models.user_model import User
from connectors.db import Session
import datetime
from flask_jwt_extended import create_access_token, current_user, unset_jwt_cookies

userBp =Blueprint('user', __name__) 

@userBp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        return redirect(url_for('user.register', error='Please fill all fields'))
    
    try:
        with Session() as session:
            user = User(username=username, email=email)
            user.set_password(password)

            session.add(user)
            session.commit()

            login_user(user)
            expires = datetime.timedelta(days=1)
            create_access_token(identity={'id': user.id, 'username': user.username, 'email': user.email}, expires_delta=expires)

            return 'User successfully created!',200
    except Exception as e:
        print(e)
        return 'Error creating user. Please try again later.', 500

    
    
@userBp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return redirect(url_for('user.login', error='Please fill all fields'))

    try:
        with Session() as session:
            user = session.query(User).filter(User.email == email).first()
            isCorrectUser = user and user.check_password(password)
            

            if isCorrectUser:
                login_user(user)
                expires = datetime.timedelta(days=1)
                create_access_token(identity={'id': user.id, 'username': user.username, 'email': user.email}, expires_delta=expires)
                return 'Login successful', 200
            else:
                return 'Invalid email or password', 401
    except Exception as e:
        print(e)
        return 'Error logging in. Please try again later.', 500
    
@userBp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        response = 'Logout successful', 200
        logout_user()
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        print(e)
    return 'Error logging out. Please try again later.', 500

@userBp.route('/user/me', methods=['GET'])
@login_required
def user_me():
    try:
        user = User.query.get(current_user.id)
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200
    except Exception as e:
        print(e)
        return 'Error fetching user. Please try again later.', 500
    
@userBp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(id):
    try:
        user = User.query.get(id)
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200
    except Exception as e:
        print(e)
        return 'Error fetching user. Please try again later.', 500

@userBp.route('/user/update', methods=['PUT'])
@login_required
def update_user():
    try:
        user = User.query.get(current_user.id)
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        session.commit()
        return 'User updated successfully', 200
    except Exception as e:
        print(e)
        return 'Error updating user. Please try again later.', 500