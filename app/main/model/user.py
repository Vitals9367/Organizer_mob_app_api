from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt
from typing import Union

#User friends table
friends = db.Table('friends',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
                   )

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    events = db.relationship('Event', backref='user',uselist=True, lazy='dynamic')

    friends = db.relationship('User',  # defining the relationship, User is left side entity
                              secondary=friends,
                              primaryjoin=(friends.c.user_id == id),
                              secondaryjoin=(friends.c.friend_id == id),
                              lazy='dynamic'
                              )

    #Password property for write only
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    #Sets password to hashed string
    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    #Checks password hash
    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    #Authorization token encoding function
    @staticmethod
    def encode_auth_token(user_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            #Payload creation
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            #Encoding
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    #Authorization token decoding function
    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            #Decoding into payload
            """
                payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            """
            payload = jwt.decode(auth_token, key)

            #Checking if token is blacklisted
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)

            #If token invalid returns string
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'

                #If token valid returns user_id
            else:
                return payload['sub']

        #If token expired
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'

        #If token invalid
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)
