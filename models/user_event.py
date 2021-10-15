
from settings import db
from  sqlalchemy import  Sequence
class UserEvent(db.Model):
    user_event_id=db.Column(db.Integer,Sequence('user_event_id_seq'),primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    answers=db.relationship("Answer", back_populates="user_event")
    gift=db.relationship("Gift", back_populates="user_event")