from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, get_user_friends, change_email

#User DTO variables
api = UserDto.api
_user = UserDto.user

#User list resource
@api.route('/')
class UserList(Resource):

    #List of all users
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    #New user creation
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)

#Individual user class
@api.route('/<username>')
@api.param('username', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):

    #Getting user by username
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, username):
        """get a user given its identifier"""
        user = get_a_user(username)
        if not user:
            api.abort(404)
        else:
            return user

#Change email route
@api.route('/<username>/change_email')
@api.param('username', 'The User identifier')
@api.response(404, 'User not found.')
class UserChangeEmail(Resource):

    #changing user email
    @api.doc('get a user')
    def post(self, username):
        data = request.json

        if data:
            return change_email(username,data['email'])
        else:
            response_object = {
                'status': 'fail',
                'message': 'no email provided'
            }
            return response_object, 404

#User friends class
@api.route('/<username>/friends')
@api.param('username', 'The User identifier')
@api.response(404, 'User not found.')
class UserFriends(Resource):

    #Getting list of user friends
    @api.doc('get user friends')
    @api.marshal_with(_user)
    def get(self, username):
        """get a user given its identifier"""
        friends = get_user_friends(username)
        if not friends:
            api.abort(404)
        else:
            return friends
