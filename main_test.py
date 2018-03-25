import json
import logging
import unittest

import main
import config

from unittest import mock

from game import game



class PythonQuizTests(unittest.TestCase):
        

    @mock.patch("main.QUIZ", new=game.QuizGame(num_questions=1))
    def test_answering_quiz_with_no_questions(self):
        # assert that if there are no more questions, we don't try to ask another
        main._ask_first_question()
        self.assertIsNotNone(main._answer_question('abc123'))

    def test_log_level_in_development(self):
        logger = logging.getLogger('test_logger')
        logger.setLevel = mock.MagicMock()

        config.set_log_level(logger, is_debug=True)

        logger.setLevel.assert_called_once_with(logging.DEBUG)

    def test_log_level_in_production(self):
        logger = logging.getLogger('test_logger')
        logger.setLevel = mock.MagicMock()

        config.set_log_level(logger, is_debug=False)

        logger.setLevel.assert_called_once_with(logging.WARNING)
