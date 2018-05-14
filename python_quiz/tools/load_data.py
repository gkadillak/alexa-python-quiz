import csv

from python_quiz.game import models
from python_quiz.tools import sessions


def load_data():
  """Initialize database with all information from csv file"""
  session = sessions.create_session()

  # load_data all the currrent questions from csv to postgres table
  with open('./python_quiz/game/data/questions.txt') as f:
    questions = []
    csvfile = csv.reader(f)
    for row in csvfile:
      quest = None
      try:
        quest = models.Question(body=row[0], option_one=row[1].strip(), option_two=row[2].strip(),
                                option_three=row[3].strip(), option_four=row[4].strip(), answer=int(row[5]))
      except Exception as e:
        # Print what went wrong and inspect
        print(e)

      questions.append(quest)
  session.add_all(questions)
  session.commit()
  print(questions)

if __name__ == '__main__':
  load_data()
