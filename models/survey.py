
from settings import db
from  sqlalchemy import  Sequence
class Survey(db.Model):
    survey_id=db.Column(db.Integer,Sequence('survey_id_seq'),primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("User", back_populates="owl_surveys")
    name=db.Column(db.String(300),nullable=False,default="N/A")
    questions=db.relationship("Question", back_populates="survey")
    status_id=db.Column(db.Integer, db.ForeignKey('status.status_id'),default=2)
    events=db.relationship("Event", back_populates="survey")
    base64=db.Column(db.String(),nullable=False,default="N/A")
    desc=db.Column(db.String(),nullable=False,default="N/A")
    status=db.relationship("Status", back_populates="surveys")
    categories=db.relationship('Category', secondary='survey_category')
    