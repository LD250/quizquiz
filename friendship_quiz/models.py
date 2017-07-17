import uuid
from django.db import models
from django.conf import settings


class Question(models.Model):
    text = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question)
    text = models.CharField(max_length=255)


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    questions = models.ManyToManyField(Question)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)
    quiz = models.ForeignKey(Quiz, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = (('question', 'quiz', 'user'),)
