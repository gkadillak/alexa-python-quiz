import logging
import os

from flask import Flask
from flask_ask import Ask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from python_quiz.tools import config

flask_app = Flask(__name__)
flask_app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app=flask_app)

ask = Ask(app=flask_app, route='/python_quiz')
configs = config

# models need to be imported to track migration changes
try:
  from python_quiz.game import models
except ImportError:
  pass

migrate = Migrate(flask_app, db)


logger = logging.getLogger(__name__)
flask_ask_logger = logging.getLogger('flask_ask')

from python_quiz import main

if __name__ == '__main__':
  flask_app.run(host='0.0.0.0')
