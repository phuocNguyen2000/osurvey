
from settings import db
from  sqlalchemy import  Sequence
class Address(db.Model):
    address_id=db.Column(db.Integer,Sequence('address_id_seq'),primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("User", back_populates="address_entities")
    province=db.Column(db.String(64),nullable=False,default="N/A")
    district=db.Column(db.String(64),nullable=False,default="N/A")
    ward=db.Column(db.String(64),nullable=False,default="N/A")
    street=db.Column(db.String(64),nullable=False,default="N/A")