import logging
import os

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def create_session():
  """
  Create an ORM session

  @rtype: sqlalchemy.orm.session.Session
  """
  testing_database_url = os.environ.get('TESTING_DATABASE_URL')
  production_database_url = os.environ.get('DATABASE_URL')
  if not testing_database_url and not production_database_url:
    raise ValueError("Cannot create a session without a database url!")

  engine = create_engine(testing_database_url if testing_database_url else production_database_url)
  Session = sessionmaker(bind=engine)
  return Session()


@contextmanager
def active_session(should_commit=True):
  """
  Context manager that simply opens and then later closes the session.
  Accessing any attribute on an entity added to the session will result in a `DetachedInstanceError`

  @return: sqlalchemy.orm.session.Session
  """
  session = create_session()
  try:
    yield session
    if should_commit:
      session.commit()
  except Exception as exc:
    session.rollback()
    logger.error("Exception when rolling back: %s" % exc)
    raise
  finally:
    session.close()
