from flask import Flask
from flask_migrate import Migrate
from extensions import db
from models.users_model import User
from models.accounts_model import Account
from models.transaction_model import Transaction
# from connectors.db import Base
# from connectors.db import connection

# Base.metadata.create_all(connection)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://milestone4santo_togetheras:aea57cc0af2e83cd579446184cd7bc1d82c3aa21@cpu2s.h.filess.io:3307/milestone4santo_togetheras' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/')
def index():
    return "Hello, World!"