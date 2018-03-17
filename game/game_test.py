import unittest

from . import game

class GameTests(unittest.TestCase):

    def test_questions_collection(self):
        question_collection = game.QuestionsCollection(num_questions=2)
        self.assertEqual(len(question_collection), 2)
