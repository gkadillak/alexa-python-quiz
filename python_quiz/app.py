import logging
import os

from flask import Flask
from flask_ask import Ask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from . import config

flask_app = Flask(__name__)
flask_app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app=flask_app)

ask = Ask(app=flask_app, route='/python_quiz')
configs = config

# models need to be imported to track migration changes
try:
  from .game import models
except ImportError:
  pass

migrate = Migrate(flask_app, db)


logger = logging.getLogger(__name__)
flask_ask_logger = logging.getLogger('flask_ask')

from . import main
