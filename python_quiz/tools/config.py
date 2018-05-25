import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTS_RUNNING = True
    SQLALCHEMY_DATABASE_URI = os.environ['TESTING_DATABASE_URL']
    LANG = 'en_US.UTF-8'
    DATABASE_URL = 'postgresql://localhost:5432/test_python_quiz'


class BootstrapTesting(object):
    FLASK_DEBUG = 1
    FLASK_APP = os.path.expanduser('~/projects/quiz_game/python_quiz/app.py')
    DATABASE_URL = 'postgresql://localhost:5432/test_python_quiz'
    TESTING_DATABASE_URL = 'postgresql://localhost:5432/test_python_quiz'
    APP_SETTINGS = 'python_quiz.tools.config.TestingConfig'
    LANG = 'en_US.UTF-8'
