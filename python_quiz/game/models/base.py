from datetime import datetime

from python_quiz.app import db


class BaseModel(db.Model):

  __abstract__ = True

  created = db.Column(db.DateTime, default=datetime.utcnow())

  # TODO: event for updating this value
  updated = db.Column(db.DateTime, default=datetime.utcnow())
