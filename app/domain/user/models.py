# -*- coding: utf-8
# Core
from datetime import datetime
from . import db, bcrypt


class User(db.Model):
    """
    User model
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=False)
    date_joined = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    password = db.Column(db.String(128))

    __tablename__ = 'users'

    def __repr__(self):
        return '<User: %r>' % (self.email)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        if self.password is None:
            return False

        return bcrypt.check_password_hash(self.password, password)
