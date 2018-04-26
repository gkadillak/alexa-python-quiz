from sqlalchemy.dialects import postgresql

from python_quiz.app import db
from python_quiz.game.models import base


class Game(base.BaseModel):
  """
  A single quiz game. The nature of this model is such that
  the ids of the questions are a stack and the question is retrieved
  lazily
  """

  __tablename__ = 'games'

  id = db.Column(db.Integer, primary_key=True)

  count = db.Column(db.Integer)
  """The number of questions for the quiz"""

  count_correct = db.Column(db.Integer, default=0)
  """The number of questions answered correctly"""

  count_incorrect = db.Column(db.Integer, default=0)
  """The number of questions answered incorrectly"""

  question_ids_snapshot = db.Column(postgresql.ARRAY(db.Integer), nullable=False)
  """Represents the quiz as instantiated"""

  question_ids = db.Column(postgresql.ARRAY(db.Integer))
  """The current state of the game"""

  session_id = db.Column(db.String(), nullable=False)
  """The identifier as given by external party"""

  __mapper_args__ = {
    'polymorphic_identity': 'games',
    'concrete': True
  }
