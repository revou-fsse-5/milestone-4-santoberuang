# from sqlalchemy import Enu
from extensions import db


class Account(db.Model):

    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False)
    account_type = db.Column(db.String(255), db.Enum('checking', 'savings'), nullable=False)
    account_number = db.Column(db.String(255), unique=True, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    update_at = db.Column(db.DateTime(timezone=True), nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('User', back_populates='accounts')

class User(db.Model):

    __tablename__ = 'users'
    account = db.relationship('Account', back_populates='users')

    def __repr__(self):
        return f'<Account(id={self.id}, balance={self.balance}, account_type={self.account_type}, account_number={self.account_number})>'