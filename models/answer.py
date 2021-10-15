

from settings import db
from  sqlalchemy import  Sequence
class Answer(db.Model):
    answer_id=db.Column(db.Integer,Sequence('answer_id_seq'),primary_key=True)
    answer=db.Column(db.String(),nullable=False,default="N/A")
    base64=db.Column(db.String(),nullable=False,default="N/A")
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    user_event_id = db.Column(db.Integer, db.ForeignKey('user_event.user_event_id'))
    user_event=db.relationship("UserEvent", back_populates="answers")