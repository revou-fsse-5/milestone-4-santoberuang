from bcrypt import gensalt, hashpw
from extensions import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    update_at = db.Column(db.DateTime(timezone=True), nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt.decode('utf-8'))

    def check_password(self, password):
        return self.password == hashpw(password.encode('utf-8'), self.password.encode('utf-8'))
    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, email={self.email})>'
