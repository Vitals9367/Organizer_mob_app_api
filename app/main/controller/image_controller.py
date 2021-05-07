from app.main.util.decorator import token_required
from app.main.service.image_service import get_user_image, upload_user_image
from flask import request
from flask_restx import Resource

from ..util.dto import ImageDto
from typing import Dict, Tuple

api = ImageDto.api

#Image class

@api.route('/<username>')
class Image(Resource):

    #decorators for getting user_id
    #method_decorators = [token_required]

    #gets user image by username
    @api.doc('user_image')
    def get(self, username):
        """user image"""
        return get_user_image(username)

    #uploads user image
    @api.doc('user_image')
    def post(self, username):
        """user image"""
        return upload_user_image(username,request)

