from python_quiz.app import db


class Question(db.Model):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)

    body = db.Column(db.String, nullable=False)

    option_one = db.Column(db.String, nullable=True)

    option_two = db.Column(db.String, nullable=True)

    option_three = db.Column(db.String, nullable=True)

    option_four = db.Column(db.String, nullable=True)

    answer = db.Column(db.Integer, nullable=False)

    def __init__(self, body, option_one, option_two, option_three, option_four, answer):
        self.body = body
        self.option_one = option_one
        self.option_two = option_two
        self.option_three = option_three
        self.option_four = option_four
        self.answer = answer

    def __repr__(self):
        return '<Question: %s>' % self.body
