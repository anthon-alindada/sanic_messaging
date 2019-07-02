# -*- coding: utf-8
# Core
from datetime import datetime
from . import db


class Channel(db.Model):
    """
    Channel model
    """

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    is_channel = db.Column(db.Boolean, default=True)
    timestamp = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    edited_timestamp = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    __tablename__ = 'channels'

    def __repr__(self):
        return '<Channel: %r>' % (self.name)


class ChannelUser(db.Model):
    """
    Channel User model
    Many to Many relation
    """

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))

    __tablename__ = 'channel_users'

    def __repr__(self):
        return '<ChannelUser: %r %r>' % (self.user_id, self.channel_id)


class Message(db.Model):
    """
    Message model
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    timestamp = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    edited_timestamp = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    __tablename__ = 'messages'

    def __repr__(self):
        return '<Message: %r>' % (self.id)
