from sqlalchemy.dialects import postgresql

from python_quiz import app
from python_quiz.game.models import base


class Game(base.BaseModel):
  """
  A single quiz game. The nature of this model is such that
  the ids of the questions are a stack and the question is retrieved
  lazily
  """

  __tablename__ = 'games'

  id = app.db.Column(app.db.Integer, primary_key=True)

  count = app.db.Column(app.db.Integer)
  """The number of questions for the quiz"""

  count_correct = app.db.Column(app.db.Integer, default=0)
  """The number of questions answered correctly"""

  count_incorrect = app.db.Column(app.db.Integer, default=0)
  """The number of questions answered incorrectly"""

  question_ids_snapshot = app.db.Column(postgresql.ARRAY(app.db.Integer), nullable=False)
  """Represents the quiz as instantiated"""

  question_ids = app.db.Column(postgresql.ARRAY(app.db.Integer))
  """The current state of the game"""

  session_id = app.db.Column(app.db.String(), nullable=False)
  """The identifier as given by external party"""

  user_id = app.db.Column(app.db.String, app.db.ForeignKey('users.id'))

  __mapper_args__ = {
    'polymorphic_identity': 'games',
    'concrete': True
  }
