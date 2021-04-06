from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.event_controller import api as event_ns
from .main.controller.search_controller import api as search_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus (restx) web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(search_ns, path='/search')
api.add_namespace(event_ns, path='/event')
api.add_namespace(auth_ns)
