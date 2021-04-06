from functools import wraps
from flask import request

from app.main.service.auth_helper import Auth
from app.main.model.user import User

#Authorization token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        #Gets user from token
        """
        response_object = {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'email': user.email,
                'admin': user.admin,
                'registered_on': str(user.registered_on)
            }
        """
        data, status = Auth.get_logged_in_user(request)

        #Gets user data
        token = data.get('data')

        #if token fails
        if not token:
            return data, status

        #Finds current user
        current_user = User.query.filter_by(id=token.get('user_id')).first()
        
        #Returns decorator with current user
        return f(current_user,*args, **kwargs)

    return decorated


#Authorization token decorator for admin user
def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        #Gets user from token
        """
        response_object = {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'email': user.email,
                'admin': user.admin,
                'registered_on': str(user.registered_on)
            }
        """
        data, status = Auth.get_logged_in_user(request)

        #Gets user data
        token = data.get('data')

        #if token fails
        if not token:
            return data, status

        #checks if admin
        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        #Finds current user
        current_user = User.query.filter_by(id=token.get('user_id')).first()
        
        #Returns decorator with current user
        return f(current_user,*args, **kwargs)

    return decorated
