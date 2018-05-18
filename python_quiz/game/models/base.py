from datetime import datetime

import app


class BaseModel(app.db.Model):

  __abstract__ = True

  created = app.db.Column(app.db.DateTime, default=datetime.utcnow())

  # TODO: event for updating this value
  updated = app.db.Column(app.db.DateTime, default=datetime.utcnow())
