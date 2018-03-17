import csv
import collections


class QuizGame:

    def __init__(self, num_questions):
        self.questions = self.create_questions(num_questions=num_questions)  # collections.deque
        self.total_questions = num_questions
        self.number_correct = 0

    def next_question(self):
        return self.questions.pop()

    def create_questions(self, num_questions):
        # pick random numbers for num_questions based on the total number of questions
        pass

    def answer_question(self, answer):
        question = self.questions.pop()
        is_correct = question.answer(answer)
        if is_correct:
            self.number_correct += 1
        return is_correct


class QuestionsCollection:

    def __init__(self, num_questions):
        self.questions = self.create_question_collection(num_questions)

    def create_question_collection(self, num_questions):
        _collection = collections.deque()
        counter = 0
        with open('game/data/questions.txt', 'r') as csvfile:
            question_reader = csv.reader(csvfile, delimiter=',')
            for row in question_reader:
                if counter != num_questions:
                    # create the question and put it in the queue
                    q = Question(*row)
                    _collection.append(q)
                    counter += 1
                else:
                    break
        return _collection

    def __len__(self):
        return len(self.questions)

    def __iter__(self):
        return self.questions




class Question:
    def __init__(self, question, choice_one, choice_two, choice_three, choice_four):
        self.question = question
        self.choice_one = choice_one
        self.choice_two = choice_two
        self.choice_three = choice_three
        self.choice_four = choice_four


