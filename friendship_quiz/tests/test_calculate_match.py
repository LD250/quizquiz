
from django.test import TestCase

from users.tests.factories import UserFactory

from friendship_quiz.calculate_match import CalculateMatch
from .factories import QuestionFactory, ChoiceFactory, QuizFactory, AnswerFactory


class CalculateMatchTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.friend = UserFactory()
        self.quiz = QuizFactory()
        self.questions = [QuestionFactory() for _ in range(4)]

        self.choices = [[ChoiceFactory(question=self.questions[q_id]) for _ in range(3)] for q_id in range(4)]

        self.quiz.questions.add(*self.questions)

    def test_calculate_match_all_equal(self):
        u1_answers = [
            AnswerFactory(
                question=choice[0].question,
                choice=choice[0],
                quiz=self.quiz,
                user=self.user
            ) for choice in self.choices
        ]

        u2_answers = [
            AnswerFactory(
                question=choice[0].question,
                choice=choice[0],
                quiz=self.quiz,
                user=self.friend
            ) for choice in self.choices
        ]

        match = CalculateMatch().calculate_match(u1_answers, u2_answers)
        self.assertEquals(match, 1)

    def test_calculate_match_all_not_equal(self):
        u1_answers = [
            AnswerFactory(
                question=choice[0].question,
                choice=choice[0],
                quiz=self.quiz,
                user=self.user
            ) for choice in self.choices
        ]

        u2_answers = [
            AnswerFactory(
                question=choice[1].question,
                choice=choice[1],
                quiz=self.quiz,
                user=self.friend
            ) for choice in self.choices
        ]

        match = CalculateMatch().calculate_match(u1_answers, u2_answers)
        self.assertEquals(match, 0)

    def test_calculate_three_of_four_equal(self):
        u1_answers = [
            AnswerFactory(
                question=choice[0].question,
                choice=choice[0],
                quiz=self.quiz,
                user=self.user
            ) for choice in self.choices
        ]

        u2_answers = [
            AnswerFactory(
                question=choice[0].question,
                choice=choice[0],
                quiz=self.quiz,
                user=self.friend
            ) for choice in self.choices[:-1]
        ]

        u2_answers.append(
            AnswerFactory(
                question=self.choices[-1][1].question,
                choice=self.choices[-1][1],
                quiz=self.quiz,
                user=self.friend
            )
        )

        match = CalculateMatch().calculate_match(u1_answers, u2_answers)
        self.assertEquals(match, 3 / 4)
