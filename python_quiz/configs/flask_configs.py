import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
  DEBUG = False
  DATABASE_URL = 'postgresql://{username}:{password}@localhost:5432/python_quiz'.format(
    username=os.environ.get('DATABASE_USERNAME'), password=os.environ.get('DATABASE_PASSWORD'))
  SQLALCHEMY_DATABASE_URI = DATABASE_URL


class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True
  DATABASE_URL = 'postgresql://localhost:5432/test_python_quiz'
  FLASK_APP = 'app.py'


class TestingConfig(Config):
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URL')
  LANG = 'en_US.UTF-8'
  DATABASE_URL = 'postgresql://localhost:5432/test_python_quiz'
  ASK_VERIFY_REQUESTS = False
