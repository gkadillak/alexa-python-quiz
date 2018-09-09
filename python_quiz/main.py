import logging

from flask import render_template
from flask_ask import question, session, statement

from python_quiz.app import ask, flask_app
from python_quiz.game import constants, game
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
  game.create_game(num_questions=3, session_id=session_id, user_id=user_id)
  rendered_question, question_id = game.ask_current_question(template_name='ask_question', session_id=session_id, user_id=user_id)
  title, content = game.display_card(question_id)
  return question(rendered_question).simple_card(title=title, content=content)


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


@ask.intent('AMAZON.NoIntent')
def no_means_no():
  return statement('Thanks for playing Python Quiz. Goodbye!')

@ask.intent('AMAZON.CancelIntent')
def cancel():
  return statement('Thanks for playing Python Quiz. Goodbye!')


@ask.intent('AMAZON.HelpIntent')
def helper():
  """Tell the user how the game works"""
  help_text = render_template('help')
  return question(help_text)


@ask.intent('AMAZON.RepeatIntent')
def repeat_question():
  """Repeat the last question for the user"""
  session_id = session.get('sessionId')
  user_id = session['user']['userId']
  rendered_question, question_id = game.ask_current_question(template_name='ask_question', session_id=session_id, user_id=user_id)
  title, content = game.display_card(question_id)
  return question(rendered_question).simple_card(title=title, content=content)

# legal nonsense
@flask_app.route('/terms')
def terms():
  return render_template('terms.html')


@flask_app.route('/policy')
def privacy_policy():
  """Generated free from shopify"""
  return render_template('privacy_policy.html')
