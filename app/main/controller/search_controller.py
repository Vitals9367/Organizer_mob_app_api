from flask import request
from flask_restx import Resource

from ..util.dto import SearchDto
from ..service.search_service import get_all_users

api = SearchDto.api
_search = SearchDto.user

#Search class
@api.route('/<name>')
@api.param('name', 'The User identifier')
@api.response(404, 'User not found.')
class SearchList(Resource):

    #Gets searched items by string
    @api.doc('list_of_searched_items')
    @api.marshal_list_with(_search, envelope='data')
    def get(self,name):

        """List all items found"""
        #Currently finds all users by name
        return get_all_users(name)
