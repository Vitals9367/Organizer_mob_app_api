from app.main.util.decorator import token_required
from app.main.service.event_service import get_a_event, get_all_user_events, save_new_event
from flask import request
from flask_restx import Resource

from ..util.dto import EventDto
from typing import Dict, Tuple

api = EventDto.api
_event = EventDto.event

#Event class
@api.route('/')
class EventList(Resource):

    #decorators for getting user_id
    method_decorators = [token_required]

    #Gets all user events of current user
    @api.doc('list_of_user_events')
    @api.marshal_list_with(_event, envelope='data')
    def get(self, current_user):
        """List all user events"""
        return get_all_user_events(current_user.id)

    #User new event creation
    @api.response(201, 'User event successfully created.')
    @api.doc('create a new user event')
    @api.expect(_event, validate=True)
    def post(self, current_user):
        """Creates a new user event """
        #Adding user id
        data = request.json
        info = {
            'title': data.get('title'),
            'date': data.get('date'),
            'created_by': current_user.id,
        }
        return save_new_event(data=info), 200

#Individual event class
@api.route('/<event_id>')
@api.param('event_id', 'The event identifier')
@api.response(404, 'Event not found.')
class Event(Resource):

    #Gets event by id
    @api.doc('get an event')
    @api.marshal_with(_event)
    def get(self, event_id):
        """get a user event given its identifier"""
        event = get_a_event(event_id)
        if not event:
            api.abort(404)
        else:
            return event
