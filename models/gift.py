
from settings import db
from  sqlalchemy import  Sequence
class Gift(db.Model):
    gift_id=db.Column(db.Integer,Sequence('gift_id_seq'),primary_key=True)
    price=db.Column(db.Float,nullable=True,default=0.0)
    user_event_id=db.Column(db.Integer, db.ForeignKey('user_event.user_event_id'))
    user_event=db.relationship("UserEvent", back_populates="gift")
    
    