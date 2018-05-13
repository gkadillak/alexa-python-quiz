import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session():
  """
  Create an ORM session

  @rtype: sqlalchemy.orm.session.Session
  """
  if 'TESTS_RUNNING' in os.environ:
    engine = create_engine(os.environ['TESTING_DATABASE_URL'])
  else:
    engine = create_engine(os.environ['DATABASE_URL'])
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
  except:
    session.rollback()
    raise
  finally:
    session.close()
