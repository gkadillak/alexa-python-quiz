from textwrap import wrap

from sqlalchemy import func
from flask import render_template

from python_quiz.game import models
from python_quiz.game.constants import game_pb
from python_quiz.tools import sessions


def ask_current_question(session_id, account_id):
  user = get_or_create_user(account_id)
  session = sessions.create_session()
  # what if a user has multiple games with the same session id? order by ascending and pick the first one
  game = session.query(models.Game).filter(models.Game.session_id==session_id).first()
  current_question = session.query(models.Question).get(game.question_ids.pop())
  session.add(game)
  session.commit()
  return render_template('ask_question',
                         question=current_question.body,
                         option_one=current_question.option_one,
                         option_two=current_question.option_two,
                         option_three=current_question.option_three,
                         option_four=current_question.option_four), current_question

def display_card(question):
  title = '\n'.join(wrap(question.body, width=7)) + '?'
  content = '1. {option_one}\n2.{option_two}\n3.{option_three}\n4.{option_four}'.format(option_one=question.option_one,
                                                                                        option_two=question.option_two,
                                                                                        option_three=question.option_three,
                                                                                        option_four=question.option_four)
  return title, content


def get_or_create_user(user_id):
  session = sessions.create_session()
  user = models.User.query.get(user_id)
  if user:
    session.close()
    return user

  user = models.User(account_id=user_id)
  session.add(user)
  session.commit()
  session.close()
  return user

def respond_game_summary(session_id):
  session = sessions.create_session()
  game = session.query(models.Game).filter(models.Game.session_id == session_id).first()
  session.close()
  return render_template('end_game', number_correct=game.count_correct, total=game.count)

def respond_to_guess(session_id, guess):
  is_correct = answer_current_question(session_id, guess)
  is_last_question = has_next_question(session_id)

  session = sessions.create_session()
  game = session.query(models.Game).filter(models.Game.session_id == session_id).first()
  session.close()

  # if the answer is correct, tell the user, and there is a next question, ask it!
  if is_correct and not is_last_question:
    correct_answer_response = render_template('correct_with_next_question')
    next_question_response = ask_current_question(session_id)
    return correct_answer_response + next_question_response, game_pb.ResponseType.QUESTION

  # if the answer is correct and there is no next question, return the game summary
  elif is_correct and is_last_question:
    return render_template('correct_with_no_next_question', count_correct=game.count_correct, count_total=game.count), game_pb.ResponseType.STATEMENT

  # if the answer is incorrect, and there is a next question, ask it!
  elif not is_correct and not is_last_question:
    incorrect_answer_response = render_template('incorrect_with_next_question')
    next_question_response = ask_current_question(session_id)
    return incorrect_answer_response + next_question_response, game_pb.ResponseType.QUESTION

  # if the answer is incorrect, and there is no next question, return the game summary
  elif not is_correct and is_last_question:
    return render_template('incorrect_with_no_next_question', count_correct=game.count_correct, count_total=game.count), game_pb.ResponseType.STATEMENT

def create_game(num_questions, session_id, user_id):
  """
  Instantiate a game and persist it to the database

  @param num_questions: Number of questions to use for the quiz
  @type num_questions: int

  @param session_id: The external identifier of the session
  @type session_id: str

  @param user_id: The identifier of the user, as defined by Amazon
  @type user_id: str

  @return: Game
  @rtype: python_quiz.game.models.Game
  """
  session = sessions.create_session()
  user = get_or_create_user(user_id)
  ids = session.query(models.Question.id).order_by(func.random()).limit(num_questions).all()
  game = models.Game(count=num_questions, question_ids=ids, question_ids_snapshot=ids, session_id=session_id, user_id=user.id)
  session.add(game)
  session.commit()
  session.close()
  return game

def answer_current_question(session_id, guess):
  """
  Answer the current question based on the current session

  @param session_id: The identifier for the current session
  @type session_id: str

  @param guess: The user's guess for the number they believe is correct: ('1', '2', '3', '4')
  @type guess: str

  @rtype: True if the guess is correct
  """
  session = sessions.create_session()
  game = session.query(models.Game).filter(models.Game.session_id == session_id).first()
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

def has_next_question(session_id):
  """Whether there is still a question that has not been asked yet"""
  session = sessions.create_session()
  game = session.query(models.Game).filter(models.Game.session_id == session_id).first()
  session.close()
  return len(game.question_ids) != 0

