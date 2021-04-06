from .. import db

#Location model for event
class Location(db.Model):
    """
    Location model for created event
    """
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    longitude = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.String(500), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return '<id: location: {}'.format(self.location)
