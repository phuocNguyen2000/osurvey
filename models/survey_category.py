
from settings import db
class SurveyCategory(db.Model):
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.survey_id'),primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'),primary_key=True)