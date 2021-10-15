
from settings import db
from  sqlalchemy import  Sequence
class Option(db.Model):
    option_id=db.Column(db.Integer,Sequence('option_id_seq'),primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    question = db.relationship("Question", back_populates="options")
    content=db.Column(db.String(3000),nullable=True)
    type=db.Column(db.String(3000),nullable=False,default="N/A")
    