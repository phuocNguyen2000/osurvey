

from settings import db
from  sqlalchemy import  Sequence
class Tag(db.Model):
    tag_id=db.Column(db.Integer,Sequence('tag_id_seq'),primary_key=True)
    name=db.Column(db.String(),nullable=False,default="N/A")
    users=db.relationship('User', secondary='user_tag')
    events=db.relationship('Event', secondary='event_tag')