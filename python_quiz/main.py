from python_quiz.app import ask, flask_app

import logging

from flask_ask import question, statement, session
from python_quiz.game import game, constants
from python_quiz.game.constants import game_pb

logger = logging.getLogger(__name__)


@ask.launch
def start_skill():
  welcome_message = 'Welcome to Python quiz. Would you like to test your Python knowledge?'
  return question(welcome_message)


@ask.intent('AMAZON.YesIntent')
def start_quiz():
  session_id = session.get('sessionId')
  user_id = session['user']['userId']
  game.create_game(num_questions=1, session_id=session_id, user_id=user_id)
  first_question = game.ask_current_question(session_id, user_id)
  return question(first_question).simple_card(title="What is python?", content="1. Something\n2. Else\n3. Entirely")


@ask.intent('QuizAnswerIntent', mapping={'guess': 'Answer'})
def answer(guess):
  return _answer_question(guess)


def _answer_question(guess):
  session_id = session.get('sessionId')
  response, response_type = game.respond_to_guess(session_id, guess)
  if response_type == constants.game_pb.ResponseType.QUESTION:
    return question(response)
  elif response_type == constants.game_pb.ResponseType.STATEMENT:
    return statement(response)


@ask.intent('AMAZON.StopIntent')
def stop_quiz():
  return statement('Thanks for playing Python Quiz. Goodbye!')
