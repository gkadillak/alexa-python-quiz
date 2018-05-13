from python_quiz import app
from python_quiz.game.models import base


class User(base.BaseModel):

  __tablename__ = 'users'

  id = app.db.Column(app.db.String, primary_key=True)

  games = app.db.relationship('Game')
