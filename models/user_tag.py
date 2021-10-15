
from settings import db
class UserTag(db.Model):
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'),primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),primary_key=True)