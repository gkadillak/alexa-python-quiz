from python_quiz.app import db
from python_quiz.game.models import base


class User(base.BaseModel):

  __tablename__ = 'users'

  id = db.Column(db.String, primary_key=True)

  games = db.relationship('Game')

