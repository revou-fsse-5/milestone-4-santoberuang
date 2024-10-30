from extensions import db


class Transaction(db.Model):

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(255), db.Enum('deposit', 'transfer', 'withdrawal'), nullable=False)
    desciption = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    account = db.relationship('Account', back_populates='transactions')

class Account(db.Model):

    __tablename__ = 'accounts'
    transaction = db.relationship('Transaction', back_populates='accounts')

    def __repr__(self):
        return f'<Transaction(id={self.id}, from_account_id={self.from_account_id}, to_account_id={self.to_account_id}, amount={self.amount}, type={self.type}, description={self.description})>'
    