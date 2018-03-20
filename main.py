import logging

from flask import Flask
from flask_ask import Ask, statement, question, session

from game import game


app = Flask(__name__)
ask = Ask(app, '/python_quiz')

logger = logging.getLogger(__name__)

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
    global QUIZ
    QUIZ = game.QuizGame(num_questions=1)
    return question(QUIZ.current_question().ask())


@ask.intent('QuizAnswerIntent')
def answer(guess):
    return _answer_question(guess)

def _answer_question(guess):
    logger.info('Quiz game: %s', QUIZ)
    if QUIZ.is_complete():
        # statements end the loop between the user and the device
        return statement('The quiz has ended! You got {number_correct} out of {total}'.format(number_correct=QUIZ.number_correct, total=QUIZ.total_questions))

    is_answer_correct = QUIZ.answer(guess)
    response = '{response_message} {next_question}'
    if is_answer_correct:
        correct_response = 'Correct! Next question:'
        response = response.format(response=correct_response,
                                   next_question=QUIZ.current_question().ask())
        return question(response)

    # answering points to a new question - we may be at the end
    if not QUIZ.current_question():
        # statements end the loop between the user and the device
        return statement('The quiz has ended! You got {number_correct} out of {total}'.format(number_correct=QUIZ.number_correct, total=QUIZ.total_questions))

    incorrect_response = 'Incorrect...next question:'
    response = response.format(response_message=incorrect_response,
                               next_question=QUIZ.current_question().ask())
    return question(response)


@ask.intent('AMAZON.StopIntent')
def stop_quiz():
    return statement('Goodbye!')
