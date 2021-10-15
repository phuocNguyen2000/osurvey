
from settings import db
class EventGiftMode(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'),primary_key=True)
    gift_mode_id = db.Column(db.Integer, db.ForeignKey('gift_mode.gift_mode_id'),primary_key=True)
    tip=db.Column(db.Integer)