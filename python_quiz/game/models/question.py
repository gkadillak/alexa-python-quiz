from python_quiz.app import db
from python_quiz.game.models import base


class Question(base.BaseModel):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)

    body = db.Column(db.String, nullable=False)
    """The question iteself"""

    option_one = db.Column(db.String, nullable=True)
    """The first option for the question"""

    option_two = db.Column(db.String, nullable=True)
    """The second option for the question"""

    option_three = db.Column(db.String, nullable=True)
    """The third option for the question"""

    option_four = db.Column(db.String, nullable=True)
    """The fourth option for the question"""

    answer = db.Column(db.Integer, nullable=False)
    """The answer for the question"""

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
