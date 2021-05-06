import uuid
import datetime

from flask.helpers import send_file

from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple

#Returning user image by username

def get_user_image(username):
    user = User.query.filter(username=username).first()

    if user:
        return send_file(user.image_name, mimetype='image/gif')

    else:
        response_object = {
            'status': 'fail',
            'message': 'User not found',
        }
        return response_object, 404
