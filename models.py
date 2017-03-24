import os
import datetime
from app import app, db
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# pylint: disable=F403, E1101, C0301, E0001

class Users(db.Model):
    """model class for table user"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(120), nullable=False)
    bucketlists = db.relationship('BucketList', backref='users', lazy='dynamic')

    def __repr__(self):
        return '<name %s %s>' % (self.first_name, self.last_name)

    def hash_password(self, password):
        """ hashes the password"""

        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        """ decodes the password"""

        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=10000):
        """ generate the auth token """

        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """ token verification"""

        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = Users.query.get(data['id'])
        return user



class BucketList(db.Model):
    """model class for table bucketlist """

    __tablename__ = "bucketlist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('BucketListItem', backref='bucketlist', passive_deletes=True)

class BucketListItem(db.Model):
    """ model for bucketlist item """

    __tablename__ = "bucketlistitems"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id", ondelete='CASCADE'), nullable=False)
    bucketlist_item_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    done = db.Column(db.Boolean, default=False)

