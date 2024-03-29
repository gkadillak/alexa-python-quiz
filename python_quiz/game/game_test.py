import json
from unittest import mock

from python_quiz.game import game, models
from python_quiz.game.testing import test_foundation
from python_quiz.game.testing.fixtures import requests
from python_quiz.tools import sessions


class GameTests(test_foundation.TestFoundation):

  def test_questions_collection(self):
    """Test that a single game is successfully created"""
    with sessions.active_session() as session:
      games = models.Game.query.with_session(session).all()
      assert not games

    game.create_game(num_questions=1, session_id="abc", user_id=requests.SESSION_ID)

    with sessions.active_session() as session:
      games = models.Game.query.with_session(session).all()
      assert len(games) == 1

  def test_correct_answer(self):
    """Test basic assumptions about answering a question correctly"""
    with sessions.active_session() as session:
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])

    current_game_id = game.create_game(num_questions=1, session_id='123', user_id='1234')
    current_game = session.query(models.Game).get(current_game_id)
    is_correct = game.answer_current_question(session_id=current_game.session_id, guess='1')
    assert is_correct == True

    with sessions.active_session() as session:
      new_game = session.query(models.Game).get(current_game_id)
      assert new_game.count_correct == 1

  def test_incorrect_answer(self):
    """Test the basic assumptions about answering a question incorrectly"""
    with sessions.active_session() as session:
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])

    current_game_id = game.create_game(num_questions=1, session_id='123', user_id='1234')
    current_game = session.query(models.Game).get(current_game_id)
    is_correct = game.answer_current_question(session_id=current_game.session_id, guess='2')
    assert is_correct != True

    with sessions.active_session() as session:
      new_game = session.query(models.Game).get(current_game_id)
      assert new_game.count_correct == 0

  def test_answer_subsequent_questions(self):
    """Test a quiz game with more than one question"""
    with sessions.active_session() as session:
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])
      session.add_all([
        models.Question(body='what part deaux', option_one='1', option_two='2', option_three='3', option_four='4', answer='2')
      ])

    game.create_game(num_questions=2, session_id='123', user_id='1234')

    # answer all of the questions
    game.answer_current_question(session_id='123', guess='2')
    game.answer_current_question(session_id='123', guess='2')

    assert game.has_next_question(session_id='123') == False

  def test_game_flow(self):
    """
    This is really a test of the state machine. Let's say we have 2 questions for a quiz.
    If we have a list of questions as [A, B], what we want to do is...

    - Start the game and ask question B. The list should be untouched, [A, B]
    - Answer the question B which should pop off of the stack and then we should ask question [A]
    - We answer question A, and we're left with an empty list and the game is over.

    This is to fix the bug where we were getting to the point where we wanted to ask question A, but we had an
    empty stack so we would try to pop an empty list. In short, asking a question should not be a mutable operation.
    """
    with sessions.active_session() as session:
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])

    game.create_game(num_questions=2, session_id='123', user_id='1234')

    with self.app.app_context():
      game.respond_to_guess('123', '1')

    with sessions.active_session(should_commit=False):
      game._query_current_question(session_id='123', user_id='1')
    game.answer_current_question(session_id='123', guess='2')

    assert game.has_next_question(session_id='123') == False

  def test_unique_games(self):
    """Test that subsequent games don't repeat questions"""
    with sessions.active_session() as session:
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])

    # create a game with a single question
    game.create_game(num_questions=1, session_id='123', user_id='1234')

    # complete the first game
    with self.app.app_context():
      game.respond_to_guess('123', '1')

    game.create_game(num_questions=1, session_id='456', user_id='1234')

    # since the questions a person can be asked are unique, there should not be another question
    # to ask the user, therefore there should not be another question
    assert game.has_next_question(session_id='456') is False


class IntegrationTests(test_foundation.TestFoundation):

  def setUp(self):
    super().setUp()
    self.test_app = self.app.test_client()

  def test_full_quiz(self):
    """Test starting and ending a quiz"""
    with sessions.active_session() as session:
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])

    game.create_game(num_questions=2, session_id=requests.SESSION_ID, user_id=requests.USER_ID)
    with mock.patch("python_quiz.main.game.create_game"):
      self.test_app.post('/python_quiz', data=json.dumps(requests.start_game_body))

    self.test_app.post('/python_quiz', data=json.dumps(requests.correct_guess_body))
    response = self.test_app.post('/python_quiz', data=json.dumps(requests.correct_guess_body))
    end_of_game_response = json.loads(response.data)
    voice_response = end_of_game_response['response']['outputSpeech']['ssml']
    assert "You've answered 2 correct out of 2" in voice_response, "Expected summary to say all questions correct"

  def test_bad_answer_slot_type(self):
    """Test that if a user doesn't respond with the wrong slot type, we tell them that and keep the game going"""
    with sessions.active_session() as session:
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])

    game.create_game(num_questions=2, session_id=requests.SESSION_ID, user_id=requests.USER_ID)
    with mock.patch("python_quiz.main.game.create_game"):
      self.test_app.post('/python_quiz', data=json.dumps(requests.start_game_body))

    response_json = self.test_app.post('/python_quiz', data=json.dumps(requests.incorrect_guess_type_body))
    response = json.loads(response_json.data)
    voice_response = response['response']['outputSpeech']['ssml']

    assert '1.' not in voice_response, 'The response for help should not include a question'

    assert response['response']['shouldEndSession'] is False, "The response should be a question"
    with sessions.active_session(should_commit=True) as session:
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])
      session.add_all([
        models.Question(body='what', option_one='1', option_two='2', option_three='3', option_four='4', answer='1')
      ])

    game.create_game(num_questions=2, session_id=requests.SESSION_ID, user_id=requests.USER_ID)
    with mock.patch("python_quiz.main.game.create_game"):
      self.test_app.post('/python_quiz', data=json.dumps(requests.start_game_body))

    self.test_app.post('/python_quiz', data=json.dumps(requests.correct_guess_body))
    self.test_app.post('/python_quiz', data=json.dumps(requests.correct_guess_body))

  def test_incorrect_with_no_next_question_response_contains_answer(self):
    """Test that if you are on the last question, we should tell you the correct answer in the response"""
    with sessions.active_session(should_commit=True) as session:
      session.add_all([
        models.Question(body='what', option_one='one', option_two='two', option_three='three', option_four='four', answer='1')
      ])

    game.create_game(num_questions=1, session_id=requests.SESSION_ID, user_id=requests.USER_ID)
    with mock.patch("python_quiz.main.game.create_game"):
      self.test_app.post('/python_quiz', data=json.dumps(requests.start_game_body))

    response = self.test_app.post('/python_quiz', data=json.dumps(requests.incorrect_guess_body))
    response_json = json.loads(response.data)
    assert 'The correct answer is one' in response_json['response']['outputSpeech']['ssml']

  def test_incorrect_with_next_question_response_contains_answer(self):
    """Test that if you are not on the last question, we should tell you the correct answer in the response"""
    with sessions.active_session(should_commit=True) as session:
      session.add_all([
        models.Question(body='one', option_one='1', option_two='2', option_three='3', option_four='4', answer='1'),
        models.Question(body='two', option_one='1', option_two='2', option_three='3', option_four='4', answer='2'),
        models.Question(body='three', option_one='1', option_two='2', option_three='3', option_four='4', answer='3'),
      ])

    game_id = game.create_game(num_questions=3, session_id=requests.SESSION_ID, user_id=requests.USER_ID)
    with mock.patch("python_quiz.main.game.create_game"):
      self.test_app.post('/python_quiz', data=json.dumps(requests.start_game_body))

    self.test_app.post('/python_quiz', data=json.dumps(requests.incorrect_guess_body))
    response = self.test_app.post('/python_quiz', data=json.dumps(requests.incorrect_guess_body))
    response_json = json.loads(response.data)

    with sessions.active_session():
      current_game = models.Game.query.get(game_id)
      question_id = current_game.question_ids_snapshot[1]
      question = models.Question.query.get(question_id)
      assert 'The correct answer is %s' % question.answer in response_json['response']['outputSpeech']['ssml']
