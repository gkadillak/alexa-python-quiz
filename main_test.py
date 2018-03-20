import json
import unittest

import main

from unittest import mock

from game import game


class PythonQuizTests(unittest.TestCase):
        

    @mock.patch("main.QUIZ", new=game.QuizGame(num_questions=1))
    def test_answering_quiz_with_no_questions(self):
        # assert that if there are no more questions, we don't try to ask another
        main._ask_first_question()
        self.assertIsNotNone(main._answer_question('abc123'))
        
