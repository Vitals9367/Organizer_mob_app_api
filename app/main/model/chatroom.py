from .. import db

#Chatroom model
class Chatroom(db.Model):
    """
    Chatroom model for created event
    """
    __tablename__ = 'chatroom'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    #Missing chat user list ...

    def __repr__(self):
        return '<id: chatroom: {}'.format(self.chatroom)
