

from settings import db
from  sqlalchemy import  Sequence
class Category(db.Model):
    category_id=db.Column(db.Integer,Sequence('category_id_seq'),primary_key=True)
    name=db.Column(db.String(),nullable=False,default="N/A")
    base64=db.Column(db.String(),nullable=False,default="N/A")