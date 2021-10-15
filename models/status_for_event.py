

from settings import db
from  sqlalchemy import  Sequence
class StatusForEvent(db.Model):
    status_for_event_id=db.Column(db.Integer,Sequence('status_for_event_id_seq'),primary_key=True)
    name=db.Column(db.String(),nullable=False,default="N/A")
    events=db.relationship("Event", back_populates="status")