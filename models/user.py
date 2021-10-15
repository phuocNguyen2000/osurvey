import hashlib
import hmac
from  sqlalchemy import  Sequence
from werkzeug.security import generate_password_hash, check_password_hash
from settings import db

class User(db.Model):
    user_id = db.Column(db.Integer,Sequence('user_id_seq'),primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name =  db.Column(db.String(64),nullable=False)
    user_name=db.Column(db.String(128),unique=True,nullable=False)
    email =  db.Column(db.String(128),unique=True,nullable=False)
    password =  db.Column(db.String(128), index=True,nullable=False)
    id_recognition=db.Column(db.String(),unique=True)
    sex=db.Column(db.String(64),nullable=False,default="N/A")
    nationality=db.Column(db.String(64),nullable=False,default="N/A")
    home=db.Column(db.String(64),nullable=False,default="N/A")
    address_entities=db.relationship("Address", back_populates="user")
    dob=db.Column(db.String(64),nullable=False,default="N/A")
    type=db.Column(db.String(64),nullable=False,default="N/A")
    do_surveys =db.relationship('Event', secondary='user_event')
    own_events=db.relationship("Event", back_populates="user")
    owl_surveys = db.relationship("Survey", back_populates="user")
    tags=db.relationship('Tag', secondary='user_tag')
    notifications=db.relationship('Notification', secondary='send_notification')
    payments=db.relationship("Payment", back_populates="user")
    
    
    device_keys=db.relationship("DeviceKey", back_populates="user")
    def __repr__(self):
        return  '<User full name {} {} ,email {}>'.format(self.first_name,self.last_name,self.email)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def hmacsha512(key, self):
        byteKey = key.encode('utf-8')
        byteData = self.encode('utf-8')
        return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()