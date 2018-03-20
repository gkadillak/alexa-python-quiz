import json
import unittest

import main
import test_data


from unittest import mock

from game import game




class PythonQuizTests(unittest.TestCase):
        

    @mock.patch("main.QUIZ", new=game.QuizGame(num_questions=0))
    def test_answering_quiz_with_no_questions(self):
        # assert that if there are no more questions, we don't try to ask another
        main._answer_questions('abc')
        self.assertTrue(main.QUIZ_GAME.is_complete())
        
