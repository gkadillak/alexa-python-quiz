import unittest

from python_quiz.game import game, models
from python_quiz import test_foundation
from python_quiz.tools import sessions


class GameTests(test_foundation.TestFoundation):

  def test_questions_collection(self):
    """Test that a single game is successfully created"""
    games = models.Game.query.all()
    assert not games

    game.create_game(num_questions=2, session_id="abc", user_id="123")
    games = models.Game.query.all()
    assert len(games) == 1

  def test_correct_answer(self):
    print('starting test')
    # create a question for the game we can answer
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
    quiz_game = game.QuizGame(num_questions=1)
    is_correct = quiz_game.answer('IMWRONG')

    self.assertFalse(is_correct)
    self.assertEqual(quiz_game.number_correct, 0)

  def test_quiz_not_complete(self):
    quiz_game = game.QuizGame(num_questions=1)
    self.assertFalse(quiz_game.is_complete())

    quiz_game.answer('doesntmatter')
    self.assertTrue(quiz_game.is_complete())

  def test_no_next_question(self):
    quiz_game = game.QuizGame(num_questions=0)
    self.assertIsNone(quiz_game.next_question())

  def test_answer_subsequent_questions(self):
    quiz_game = game.QuizGame(num_questions=2)
    first_question = quiz_game.next_question()
    quiz_game.answer('blah')
    second_question = quiz_game.next_question()
    self.assertNotEqual(first_question, second_question)

class QuestionTests(unittest.TestCase):

  def test_ask_question(self):
    posed_question = 'what is your favorite color?'
    choices = ('red', 'blue', 'purple', 'yellow')
    quiz_question = game.Question(posed_question, *choices, answer='blue')
    ask = quiz_question.ask()
    self.assertIn(posed_question, ask)
    for choice in choices:
      self.assertIn(choice, ask)
