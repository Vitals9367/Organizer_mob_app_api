from .. import db

#Event model
class Event(db.Model):
    """
    Event model for created event
    """
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    location = db.relationship('Location', backref='event', uselist=False)
    chatroom = db.relationship('Chatroom', backref='event', uselist=False)
    private = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<id: plan: {}'.format(self.plan)

