
import datetime
from settings import db
from  sqlalchemy import  Sequence
class Payment(db.Model):
    payment_id=db.Column(db.Integer,Sequence('payment_id_seq'),primary_key=True)
    event_id=db.Column(db.Integer, db.ForeignKey('event.event_id'))
    event=db.relationship("Event", back_populates="payment")
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user=db.relationship("User", back_populates="payments")
    total=db.Column(db.Float)
    state=db.Column(db.Boolean,nullable=False,default=False)
    paypal_pay_id=db.Column(db.String(),unique=True,nullable=False)
    checkout_token=db.Column(db.String(),unique=True,nullable=False)
    time_stame=db.Column(db.DateTime(timezone=True),default=datetime.datetime.utcnow())
    