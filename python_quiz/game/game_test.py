import unittest

from . import game


class GameTests(unittest.TestCase):

    def test_questions_collection(self):
        question_collection = game.GameInterface(num_questions=2)
        self.assertEqual(len(question_collection), 2)


class QuizGameTests(unittest.TestCase):

    def test_correct_answer(self):
        quiz_game = game.QuizGame(num_questions=1)
        is_correct = quiz_game.answer(quiz_game.game[0].correct_answer)

        self.assertTrue(is_correct)
        self.assertEqual(quiz_game.number_correct, 1)

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
