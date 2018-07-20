from sqlalchemy.dialects import postgresql

from python_quiz import app
from python_quiz.game.models import base
from python_quiz.game.models.column_types import MutableList


class User(base.BaseModel):

  __tablename__ = 'users'

  id = app.db.Column(app.db.String, primary_key=True)

  asked_questions = app.db.Column(MutableList.as_mutable(postgresql.ARRAY(app.db.Integer)), default=[])
  """All of the questions a user has been asked"""

  games = app.db.relationship('Game')
