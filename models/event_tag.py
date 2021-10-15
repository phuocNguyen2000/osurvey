
from settings import db
class EventTag(db.Model):
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'),primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'),primary_key=True)