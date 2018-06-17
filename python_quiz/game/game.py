import logging
from textwrap import wrap

from sqlalchemy import func, desc
from flask import render_template

from python_quiz.game import models
from python_quiz.game.constants import game_pb
from python_quiz.tools import sessions

logger = logging.getLogger(__name__)


def ask_current_question(session_id, account_id):
  with sessions.active_session() as session:
    get_or_create_user(account_id, session)
    game = session.query(models.Game).filter(models.Game.session_id==session_id).first()
    current_question = session.query(models.Question).get(game.question_ids.pop())
    logger.info('game=%s question=%s', game.id, current_question.body)
    session.add(game)
    session.commit()
    return render_template('ask_question',
                           question=current_question.body,
                           option_one=current_question.option_one,
                           option_two=current_question.option_two,
                           option_three=current_question.option_three,
                           option_four=current_question.option_four), current_question.id

def display_card(question_id):
  with sessions.active_session() as session:
    current_question = models.Question.query.with_session(session).get(question_id)
    title = '\n'.join(wrap(current_question.body, width=7)) + '?'
    content = '1. {option_one}\n2.{option_two}\n3.{option_three}\n4.{option_four}' \
      .format(option_one=current_question.option_one,
              option_two=current_question.option_two,
              option_three=current_question.option_three,
              option_four=current_question.option_four)
  return title, content


def get_or_create_user(user_id, session):
  """
  Based on the unique user id, fetch the user, fallback to creating the user

  @param user_id: The unique identifier for the user
  @type user_id: str

  @param session: The open connection to the database
  @type session: sqlalchemy.orm.session.Session

  @return: User
  @rtype: python_quiz.game.models.User
  """
  user = session.query(models.User).get(user_id)
  if user:
    logger.info('get_or_create_user user found for user_id=%s', user_id)
    return user

  logger.info('user not found for user_id=%s so creating user', user_id)
  user = models.User(id=user_id)
  session.add(user)
  return user


def respond_game_summary(session_id):
  with sessions.create_session() as session:
    game = models.Game.with_session(session).filter(models.Game.session_id == session_id).first()
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

  @return: ID of the game that was created
  @rtype: int
  """
  with sessions.active_session(should_commit=False) as session:
    user = get_or_create_user(user_id, session)
    ids_raw = session.query(models.Question.id).order_by(func.random()).limit(num_questions).all()
    ids = [i[0] for i in ids_raw]
    current_game = models.Game(count=num_questions, question_ids=ids, question_ids_snapshot=ids,
                               session_id=session_id, user_id=user.id)
    session.add(current_game)
    session.commit()
    current_game_id = current_game.id
    return current_game_id


def answer_current_question(session_id, guess):
  """
  Answer the current question based on the current session

  @param session_id: The identifier for the current session
  @type session_id: str

  @param guess: The user's guess for the number they believe is correct: ('1', '2', '3', '4')
  @type guess: str

  @rtype: True if the guess is correct
  """
  with sessions.active_session(should_commit=False) as session:
    current_game = session.query(models.Game)\
      .filter(models.Game.session_id == session_id).order_by(desc(models.Game.created)).first()
    question_id = current_game.question_ids.pop()
    current_question = models.Question.query.with_session(session).get(question_id)
    logger.info("question=%s, guess=%s", current_question, guess)
    is_correct = current_question.answer == int(guess)

    if is_correct:
      current_game.count_correct += 1
    else:
      current_game.count_incorrect += 1

    session.add(current_game)
    session.commit()
    return is_correct

def has_next_question(session_id):
  """Whether there is still a question that has not been asked yet"""
  with sessions.create_session() as session:
    game = models.Game.query.with_session(session).filter(models.Game.session_id == session_id).first()
    return len(game.question_ids)

