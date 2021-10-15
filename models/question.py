
from settings import db
from  sqlalchemy import  Sequence
class Question(db.Model):
    question_id=db.Column(db.Integer,Sequence('question_id_seq'),primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.survey_id'))
    survey = db.relationship("Survey", back_populates="questions")
    content=db.Column(db.String(3000),nullable=False,default="N/A")
    options=db.relationship("Option", back_populates="question")
    images = db.relationship("Image", back_populates="question")
    allow_diffent_answer=db.Column(db.Boolean,nullable=False,default=False)
    type=db.Column(db.Integer,nullable=False,default=0)