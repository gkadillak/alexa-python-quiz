from python_quiz import app
from python_quiz.game.models import base


class Question(base.BaseModel):
  __tablename__ = 'questions'

  id = app.db.Column(app.db.Integer, primary_key=True)

  body = app.db.Column(app.db.String, nullable=False)
  """The question itself"""

  option_one = app.db.Column(app.db.String, nullable=True)
  """The first option for the question"""

  option_two = app.db.Column(app.db.String, nullable=True)
  """The second option for the question"""

  option_three = app.db.Column(app.db.String, nullable=True)
  """The third option for the question"""

  option_four = app.db.Column(app.db.String, nullable=True)
  """The fourth option for the question"""

  answer = app.db.Column(app.db.Integer, nullable=False)
  """The answer for the question"""

  @property
  def answer_body(self):
    """
    Return the human readable answer, rather than just the number.
    This is useful when telling the user the answer to the question that they missed.

    @return: The human readable answer: "BaseException" rather than "3"
    """
    if self.answer == 1:
      return self.option_one
    elif self.answer == 2:
      return self.option_two
    elif self.answer == 3:
      return self.option_three
    elif self.answer == 4:
      return self.option_four
    else:
      raise ValueError('%s is not in the integer range 1-4' % self.answer)

  __mapper_args = {
    'polymorphic_identity': 'questions',
    'concrete': True
  }

  def __init__(self, body, option_one, option_two, option_three, option_four, answer):
    self.body = body
    self.option_one = option_one
    self.option_two = option_two
    self.option_three = option_three
    self.option_four = option_four
    self.answer = answer

  def __repr__(self):
    return '<Question: %s>' % self.body
