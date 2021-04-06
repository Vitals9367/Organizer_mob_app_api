import uuid
import datetime

from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple

#Searching user list by string
def get_all_users(name):
    users = User.query.filter(User.username.contains(name)).all()
    if users:
        return users
    else:
        response_object = {
            'status': 'fail',
            'message': 'No items found',
        }
        return response_object, 404


