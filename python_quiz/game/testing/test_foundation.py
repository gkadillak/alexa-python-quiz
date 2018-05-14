import unittest

from contextlib import contextmanager
from unittest import mock

import os
from flask import Flask

from python_quiz import config
from python_quiz.app import db


class TestFoundation(unittest.TestCase):

  def setUp(self):
    """
    Create the current version of the production database
    """
    os.environ['TESTS_RUNNING'] = '1'
    # migrate all changes to the db
    self.app = Flask(__name__)
    self.app.config.from_object(config.TestingConfig)
    db.init_app(self.app)
    with self.app.app_context():
      db.session.close_all()
      db.drop_all()
      db.create_all()


  def tearDown(self):
    """
    Close all connections that the app knows about and wipe the entire database
    """
    with self.app.app_context():
      db.session.close_all()
      db.drop_all()


