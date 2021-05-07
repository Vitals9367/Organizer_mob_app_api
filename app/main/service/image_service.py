from flask.helpers import send_file
from flask import request
import os
from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple

from werkzeug import secure_filename

#Checking allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Returning user image by username

def get_user_image(username):

    user = User.query.filter_by(username=username).first();

    if user:
        if user.image_name:
            return send_file("images\\"+user.image_name, mimetype='image/gif')

        return send_file("images\\person.png", mimetype='image/gif')

    else:
        response = {
            'status': 'fail',
            'message':'User not found',
        }
        return response, 404

#Uploading user image
def upload_user_image(username, request):

    user = User.query.filter_by(username=username).first()

    if not user:
        response = {
            'status': 'fail',
            'message': 'User not found',
        }
        return response, 404

    if 'file' not in request.files:
        response = {
            'status': 'fail',
            'message': 'No file part',
        }
        return response, 404

    file = request.files['file']
    name = secure_filename(file.filename)

    if not allowed_file(name):
        response = {
        'status': 'fail',
        'message': 'Wrong file format',
        }
        return response, 404

    if user.image_name or os.path.isfile("app\\main\\images\\"+user.image_name):
       os.remove("app\\main\\images\\"+user.image_name)

    user.image_name = name;

    file.save("app\\main\\images\\"+name)

    db.session.commit()

    response = {
        'status': 'success',
        'message': 'Image uploaded',
    }
    return response, 200
