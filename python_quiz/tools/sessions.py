import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session():
  """
  Create an ORM session

  @rtype: sqlalchemy.orm.session.Session
  """
  engine = create_engine(os.environ['DATABASE_URL'])
  Session = sessionmaker(bind=engine)
  return Session()
