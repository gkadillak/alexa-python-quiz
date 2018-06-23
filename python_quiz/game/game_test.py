from python_quiz.game import game, models
from python_quiz.game.testing import test_foundation
from python_quiz.tools import sessions


class GameTests(test_foundation.TestFoundation):

  def test_questions_collection(self):
    """Test that a single game is successfully created"""
    with sessions.active_session() as session:
      games = models.Game.query.with_session(session).all()
      assert not games

    game.create_game(num_questions=1, session_id="abc", user_id="123")

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

    current_game_id = game.create_game(num_questions=2, session_id='123', user_id='1234')

    # answer all of the questions
    game.answer_current_question(session_id='123', guess='2')
    game.answer_current_question(session_id='123', guess='2')

    assert game.has_next_question(session_id='123') == False
