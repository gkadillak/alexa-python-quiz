import json

from sqlalchemy import func
from flask import render_template

from python_quiz.game import models
from python_quiz.tools import sessions


def ask_current_question(session_id):
  session = sessions.create_session()
  game = session.query(models.Game).filter(models.Game.session_id==session_id).first()
  current_question = session.query(models.Question).get(game.question_ids.pop())
  session.add(game)
  session.commit()
  return render_template('ask_question',
                  question=current_question.body,
                  option_one=current_question.option_one,
                  option_two=current_question.option_two,
                  option_three=current_question.option_three,
                  option_four=current_question.option_four)


class QuizGame:

  def __init__(self, num_questions, session_id):
    self.game = self._create_quiz(num_questions=num_questions, session_id=session_id)

  def _create_quiz(self, num_questions, session_id):
    return GameInterface(num_questions=num_questions, session_id=session_id)

  def next_question(self):
    return self.game.next_question()

  @property
  def current_question(self):
    return self.game.current_question

  def answer(self, guess, session_id):
    return self.game.answer_current_question(guess)

  def to_json(self):
    response = dict(current_question=self.current_question,
                    next_question=self.next_question,
                    correct_answer=self.current_question.correct_answer)
    return json.dumps(response)

  def is_complete(self):
    return self.game.is_complete()

def create_game(num_questions, session_id):
  """
  Instantiate a game and persist it to the database

  @param num_questions: Number of questions to use for the quiz
  @type num_questions: int

  @param session_id: The external identifier of the session
  @type session_id: str

  @return: Game
  @rtype: python_quiz.game.models.Game
  """
  session = sessions.create_session()
  ids = session.query(models.Question.id).order_by(func.random()).limit(num_questions).all()
  game = models.Game(count=num_questions, question_ids=ids, question_ids_snapshot=ids, session_id=session_id)
  session.add(game)
  session.commit()
  session.close()
  return game

class GameInterface:

  def __init__(self, num_questions, session_id):
    self.game = self.create_game(num_questions, session_id=session_id)


  def next_question(self):
    """
    Return the next question from the list of question id's and save
    the current state of the game. Mutates the game state.

    @return: The next question
    @rtype: python_quiz.game.models.Question
    """
    session = sessions.create_session()
    question_id = self.game.question_ids.pop()
    session.add(self.game)
    session.commit()
    session.close()
    return models.Question.query.get(question_id)

  @property
  def current_question(self):
    """
    The next unanswered question. Does not mutate the game state.

    @return: The next unanswered question
    @rtype: python_quiz.game.models.Question
    """
    session = sessions.create_session()
    question_id = self.game.question_ids[-1]
    question = session.query(models.Question).get(question_id)
    session.close()
    return question

  def __len__(self):
    return len(self.game.count)

  def __iter__(self):
    return [models.Question.query.get(i) for i in self.game.question_ids]

  def __getitem__(self, key):
    return models.Question.query.get(key)

  def answer_current_question(self, guess, session_id):
    """Answer the current question and update the game totals of correct/incorrect"""
    session = sessions.create_session()
    is_correct = self.current_question.answer == int(guess)

    if is_correct:
      self.game.count_correct +=1
    else:
      self.game.count_incorrect += 1
    session.add(self.game)
    session.commit()
    session.close()
    return is_correct()

  def is_complete(self):
    return len(self.game.question_ids)

def answer_current_question(guess, session_id):
  """Answer the current question based on the session_id"""
  session = sessions.create_session()
  game = models.Game.query.get(session_id)
  question_id = game.question_ids.pop()
  current_question = models.Question.query.get(question_id)
  is_correct = current_question.answer == int(guess)

  if is_correct:
    game.count_correct += 1
  else:
    game.count_incorrect += 1
  session.add(game)
  session.commit()
  session.close()
  return is_correct

