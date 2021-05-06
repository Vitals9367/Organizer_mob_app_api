from app.main.model.user import User
from ..service.blacklist_service import save_token

#Authentication class
class Auth:

    #User login functions
    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                #If function succeeds
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode(),
                        'User':{
                            'username':user.username,
                            'email':user.email,
                        }
                    }
                    return response_object, 200

            #If fails
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    #User logout function
    @staticmethod
    def logout_user(data):

        #If token is provided
        if data:
            try:
                auth_token = data.split(" ")[0]

            except Exception as e:
                
                response_object = {
                    'status': 'fail',
                    'message': e.args
                }
                return response_object, 500

        else:
            auth_token = ''

        #If token is splited correctly
        if auth_token:

            #Decoding token
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):

                # mark the token as blacklisted
                return save_token(token=auth_token)

            # if decoded returns wrong parameters    
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401

        #If token is invalid
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403


    #Getting user information from token
    @staticmethod
    def get_logged_in_user(new_request):

        # get the auth token
        auth_token = new_request.headers.get('Authorization')

        if auth_token:

            #Decoding token
            #returns user_id
            resp = User.decode_auth_token(auth_token)
            
            #if decoded token is good
            if not isinstance(resp, str):

                user = User.query.filter_by(id=resp).first()

                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200

            #if decoding failed
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401

        #if token is invalid
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
