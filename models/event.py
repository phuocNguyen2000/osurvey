

import datetime
from settings import db
from  sqlalchemy import  Sequence
class Event(db.Model):
    event_id=db.Column(db.Integer,Sequence('question_id_seq'),primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.survey_id'))
    survey = db.relationship("Survey", back_populates="events")
    users =db.relationship('User', secondary='user_event')
    start=db.Column(db.DateTime(timezone=True))
    end=db.Column(db.DateTime(timezone=True))
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user=db.relationship("User", back_populates="own_events")
    price = db.Column(db.Integer,default=0)
    give_away = db.Column(db.Integer,default=0)
    limit=db.Column(db.Integer)
    time_stame=db.Column(db.DateTime(timezone=True),default=datetime.datetime.utcnow())
    tags=db.relationship('Tag', secondary='event_tag')
    status_id= db.Column(db.Integer, db.ForeignKey('status_for_event.status_for_event_id'),default=2)
    status=db.relationship("StatusForEvent", back_populates="events")
    gift_modes=db.relationship('GiftMode', secondary='event_gift_mode')
    payment=db.relationship("Payment", back_populates="event")