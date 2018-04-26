from python_quiz.app import ask, flask_app

import logging

from flask_ask import question, statement, session
from python_quiz.game import game

logger = logging.getLogger(__name__)


@ask.launch
def start_skill():
  welcome_message = 'Welcome to Python quiz. Would you like to test your Python knowledge?'
  return question(welcome_message)


@flask_app.route('/word')
def word():
  return 'word'


@ask.intent('AMAZON.YesIntent')
def start_quiz():
  session_id = session.get('sessionId')
  game.create_game(1, session.get('sessionId'))
  first_question = game.ask_current_question(session_id)
  return question(first_question)


def _start_quiz(session_id):
  return game.QuizGame(num_questions=1, session_id=session_id)


@ask.intent('QuizAnswerIntent', mapping={'guess': 'Answer'})
def answer(guess):
  return _answer_question(guess)


def _answer_question(guess):
  logger.info('Quiz game: %s', QUIZ)

  if game.quiz_is_complete(session_id):
    # statements end the loop between the user and the device
    return statement('The quiz has ended! You got {number_correct} out of {total}'.format(number_correct=QUIZ.number_correct, total=QUIZ.total_questions))

  is_answer_correct = QUIZ.answer(guess)
  response = '{response_message} {next_question}'

  # answering points to a new question - we may be at the end
  if not QUIZ.current_question():
    # statements end the loop between the user and the device
    return statement('The quiz has ended! You got {number_correct} out of {total}'.format(number_correct=QUIZ.number_correct, total=QUIZ.total_questions))

  incorrect_response = 'Incorrect...'
  correct_response = 'Correct!'
  response = response.format(response_message=correct_response if is_answer_correct else incorrect_response,
                             next_question=QUIZ.current_question().ask())
  return question(response)


@ask.intent('AMAZON.StopIntent')
def stop_quiz():
  return statement('Thanks for playing Python Quiz. Goodbye!')
