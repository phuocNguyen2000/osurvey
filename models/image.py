
from settings import db
from  sqlalchemy import  Sequence
class Image(db.Model):
    image_id=db.Column(db.Integer,Sequence('image_id_seq'),primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    question = db.relationship("Question", back_populates="images")
    base64=db.Column(db.String(),nullable=False,default="N/A")
    