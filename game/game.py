import csv
import collections


class QuizGame:

    def __init__(self, num_questions):
        self.questions = self._create_questions(num_questions=num_questions)  # collections.deque
        self.total_questions = num_questions
        self.number_correct = 0

    def next_question(self):
        if self.questions:
            return self.questions.pop()
        return None

    def _create_questions(self, num_questions):
        return QuestionsCollection(num_questions=num_questions)

    def current_question(self):
        if self.questions:
            return self.questions[-1]
        return None

    def next_question(self):
        if len(self.questions) >= 2:
            return self.questions[-2]
        return None

    def answer(self, guess):
        is_correct = self.current_question().answer(guess)
        if is_correct:
            self.number_correct += 1
        self.questions.pop()
        return is_correct

    def is_complete(self):
        return not bool(len(self.questions))

    def __str__(self):
        pass

    def __repr__(self):
        pass


class QuestionsCollection:

    def __init__(self, num_questions):
        self.questions = self.create_question_collection(num_questions)
        self.num_questions = num_questions

    def create_question_collection(self, num_questions):
        questions = []
        counter = 0
        with open('game/data/questions.txt', 'r') as csvfile:
            question_reader = csv.reader(csvfile, delimiter=',')
            # TODO: make the question collection order for every instantiation
            for row in question_reader:
                if counter != num_questions:
                    # create the question and put it in the queue
                    q = Question(*row)
                    questions.append(q)
                    counter += 1
                else:
                    break
        return questions

    def pop(self):
        return self.questions.pop()

    def __len__(self):
        return len(self.questions)

    def __iter__(self):
        return self.questions

    def __getitem__(self, key):
        return self.questions[key]

    def __str__(self):
        if self.is_complete():
            return '<Quiz {number_correct}/{num_questions}>'.format(question)
        return '<Quiz {question} {current_question_number}/{num_questions}>'.format(question=self.questions[0],
                                                                                    current_question_number=len(self.questions),
                                                                                    num_questions=self.num_questions)


class Question:

    def __init__(self, question, choice_one, choice_two, choice_three, choice_four, answer):
        self.question = question
        self.choice_one = choice_one
        self.choice_two = choice_two
        self.choice_three = choice_three
        self.choice_four = choice_four
        self.correct_answer = answer

    def answer(self, guess):
        return self.correct_answer == guess

    def ask(self):
        return """
        {question}? Is it one: {choice_one}, two: {choice_two},
        three: {choice_three}, or four: {choice_four}?
        """.format(question=self.question,
                   choice_one=self.choice_one,
                   choice_two=self.choice_two,
                   choice_three=self.choice_three,
                   choice_four=self.choice_four)

    def __str__(self):
        return self.question

    def __repr__(self):
        return self.question
