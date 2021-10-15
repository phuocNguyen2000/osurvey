
from settings import db
from  sqlalchemy import  Sequence
class Notification(db.Model):
    notification_id=db.Column(db.Integer,Sequence('notification_id_seq'),primary_key=True)
    content=db.Column(db.String(),nullable=False)
    