from flask_restx import Namespace, fields

#User DTO
class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

#Search DTO
class SearchDto:
    api = Namespace('search', description='search related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
    })

#Auth DTO
class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

#Event DTO
class EventDto:
    api = Namespace('event', description='event related operations')
    event = api.model('event', {
        'title': fields.String(required=True, description='The title'),
        'created_by_id': fields.Integer(description='The user id'),
        'date': fields.DateTime(required=True, description='The date ')
    })
