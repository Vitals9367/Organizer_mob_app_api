from datetime import datetime

from app.main import db
from app.main.model.event import Event
from typing import Dict, Tuple

#Getting all events
def get_all_events():
    return Event.query.all()

#Getting all user events
def get_all_user_events(user_id):
    return Event.query.filter_by(created_by=user_id).all()

#Getting event by id
def get_a_event(id):
    return Event.query.filter_by(id=id).first()

#Saving changes to database
def save_changes(data: Event) -> None:
    db.session.add(data)
    db.session.commit()

#Creating new event
def save_new_event(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:

    try:
        new_event = Event(
            title=data['title'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            created_by=data['created_by'],
        )
        
        #saving event into db
        save_changes(new_event)
        
        response_object = {
            'status': 'success',
            'message': 'Plan created successfully.',
            'plan': {
                'title': new_event.title,
                'date':  str(new_event.date),
                'created_by': new_event.created_by,
            }
        }
        return response_object, 200

    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e.args,
        }
        return response_object, 500
