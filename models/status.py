

from settings import db
from  sqlalchemy import  Sequence
class Status(db.Model):
    status_id=db.Column(db.Integer,Sequence('status_id_seq'),primary_key=True)
    name=db.Column(db.String(),nullable=False,default="N/A")
    surveys=db.relationship("Survey", back_populates="status")