import factory

from friendship_quiz.models import Question, Choice, Quiz, Answer


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    text = factory.Sequence(lambda n: 'Question text {0}'.format(n))


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
    text = factory.Sequence(lambda n: 'Choice text {0}'.format(n))


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer
