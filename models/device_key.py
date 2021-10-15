
from settings import db
from  sqlalchemy import  Sequence
class DeviceKey(db.Model):
    device_id=db.Column(db.Integer,Sequence('device_id_seq'),primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("User", back_populates="device_keys")
    key=db.Column(db.String(),unique=True,nullable=False)
    