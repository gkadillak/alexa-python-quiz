import logging

from flask import Flask
from flask_ask import Ask, statement, question, session


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
    QUIZ = QuizGame()
    return question(QUIZ.next_question())


@ask.intent('QuizAnswerIntent')
def answer(answer):

    if QUIZ.has_ended:
        # statements end the loop between the user and the device
        statement('The quiz has ended! You got {number_correct} out of {total}'.format(number_correct=QUIZ.number_correct, total=QUIZ.total_questions))

    question = QUIZ.next_question()
    if answer == QUIZ.current_answer:
        next_question = 'Correct! Next question: {question}'.format(question=question)
        # questions expect a response and keep the loop between the device and the user alive
        return question(next_question)

    next_question = 'Incorect...next question: {question}'.format(question=question)
    return question(next_question)


@ask.intent('AMAZON.StopIntent')
def stop_quiz():
    return statement('Goodbye!')
