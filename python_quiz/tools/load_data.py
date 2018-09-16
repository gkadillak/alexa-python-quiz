# add the python_quiz package for imports later
import os
import sys
quiz_game_path = os.path.abspath('../quiz_game')
sys.path.append(quiz_game_path)

import argparse
import csv

from python_quiz.game import models
from python_quiz.tools import sessions


def load_data(data_file_name: str, dry_run=True):
  """Initialize database with all information from csv file"""
  session = sessions.create_session()

  # load_data all the currrent questions from csv to postgres table
  with open('./python_quiz/game/data/' + data_file_name) as f:
    questions = []
    csvfile = csv.reader(f, delimiter=':')
    for row in csvfile:
      quest = None
      try:
        quest = models.Question(body=row[0], option_one=row[1].strip(), option_two=row[2].strip(),
                                option_three=row[3].strip(), option_four=row[4].strip(), answer=int(row[5]))
      except Exception as e:
        print(e)

      questions.append(quest)

  if dry_run:
    print("NOT PERSISTING THE FOLLOWING QUESTIONS")
    print(questions)
  else:
    print("PERSISTING THE FOLLOWING QUESTIONS")
    session.add_all(questions)
    session.commit()


parser = argparse.ArgumentParser(description="Load new quiz questions into the database")
parser.add_argument('data_file_name', type=str,
                    help="The name of the text file under /python_quiz/game/data to use to create the new questions")
parser.add_argument('--dry-run', type=bool, help="Whether to persist the questions or not")

args = parser.parse_args()

load_data(args.data_file_name, dry_run=args.dry_run)
