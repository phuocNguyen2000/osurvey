
from settings import db
class SendNotification(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),primary_key=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.notification_id'),primary_key=True)
    send_at_time=db.Column(db.DateTime(timezone=True))