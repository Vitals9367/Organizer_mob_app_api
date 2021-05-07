import uuid
import datetime

from flask_mail import Message

from app.main import db, mail
from app.main.model.user import User
from typing import Dict, Tuple

from sqlalchemy import or_

#Creating new user
def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:

    #Checking if email exists
    user = User.query.filter(
        or_(User.email == data['email'], User.username==data['username'])).first()

    #If not creating new user
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        #Saving user
        save_changes(new_user)

        msg = Message(new_user.username + ", your account has been created!",
        sender="vitalijus.alsauskas@gmail.com",
        recipients=[new_user.email])

        #mail.send(msg)

        #Generating Auth token
        return generate_token(new_user)

    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


#Getting all users
def get_all_users():
    return User.query.all()


#Getting user by username
def get_a_user(username):
    return User.query.filter_by(username=username).first()

#Getting user friends
#Returns list of friends
def get_user_friends(username):
    friends = User.query.filter_by(username=username).first().friends
    if friends.count == 0:
        response_object = {
            'status': 'fail',
            'message': 'No friends found',
        }
        return response_object, 404
    else:
        return friends

#Friend adding
#Returns response object
def add_user_friend(username,friend_usr):

    user = User.query.filter_by(username=username).first()
    friend = User.query.filter_by(username=friend_usr).first()

    #Appending both because both are each other friends after
    user.friends.append(friend)
    friend.friends.append(user)

    response_object = {
        'status': 'success',
        'message': user.username + ' and ' + friend.username + ' are friends now.'
    }
    return response_object, 200

#Authentication token generation
#Returns response object
def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:

        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

#Saving changes to database
def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()
