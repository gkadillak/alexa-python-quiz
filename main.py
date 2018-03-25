import logging
import os

from flask import Flask
from flask_ask import Ask, statement, question, session

import config

from game import game


app = Flask(__name__)
ask = Ask(app, '/python_quiz')


logger = logging.getLogger(__name__)
flask_logger = logging.getLogger('flask_ask')
is_debug = bool(int(os.environ.get('FLASK_DEBUG')))

config.set_log_level(flask_logger, is_debug=is_debug)

QUIZ = None


@ask.launch
def start_skill():
    welcome_message = 'Welcome to Python quiz. Would you like to test your Python knowledge?'
    return question(welcome_message)


@ask.on_session_started
def new_session():
    logger.info('New session started')


@ask.intent('AMAZON.YesIntent')
def start_quiz():
    return _ask_first_question()


def _ask_first_question():
    global QUIZ
    QUIZ = game.QuizGame(num_questions=2)
    return question(QUIZ.current_question().ask())


@ask.intent('QuizAnswerIntent', mapping={'guess': 'Answer'})
def answer(guess):
    return _answer_question(guess)


def _answer_question(guess):
    logger.info('Quiz game: %s', QUIZ)
    if QUIZ.is_complete():
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
