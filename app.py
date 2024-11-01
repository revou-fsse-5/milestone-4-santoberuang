from flask import Flask, session
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_login import LoginManager
from flask_migrate import Migrate
from extensions import db
from models.user_model import User
from models.account_model import Account
from models.transaction_model import Transaction
import os
from controllers.user_controller import userBp
from controllers.account_controller import accountBp
from controllers.transaction_controller import transactionBp

# Base.metadata.create_all(connection)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://milestone4santo_togetheras:aea57cc0af2e83cd579446184cd7bc1d82c3aa21@cpu2s.h.filess.io:3307/milestone4santo_togetheras' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)

login_manager = LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(userBp)
app.register_blueprint(accountBp)
app.register_blueprint(transactionBp)


@login_manager.request_loader
def load_user(request):
    try:
            verify_jwt_in_request(request)
            user = get_jwt_identity()
            return session.query(User).get(user.id)
    except Exception as e:
        print(e)
        return None

@app.route('/')
def index():
    return "Hello, World!"