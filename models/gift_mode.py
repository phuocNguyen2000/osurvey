
from settings import db
from  sqlalchemy import  Sequence
class GiftMode(db.Model):
    gift_mode_id=db.Column(db.Integer,Sequence('gift_mode_id_seq'),primary_key=True)
    mode=db.Column(db.String(),nullable=False,default="N/A")
    events=db.relationship('Event', secondary='event_gift_mode')
    