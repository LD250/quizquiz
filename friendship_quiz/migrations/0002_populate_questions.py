# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 16:55
from __future__ import unicode_literals

from django.db import migrations

QUESTIONS = [
    ('What is your favorite color?', ('yellow', 'blue', 'green')),
    ('What is your favorite animal?', ('rabbit', 'hedgehog', 'cat')),
    ('What is your favorite place?', ('Home', 'Rome', 'Lviv', 'Munich')),
    ('What is your favorite restaurant?', ('I prefer home food', 'MacDonalds', 'Pizza')),
    ('What is your favorite music?', ('Rock', 'Classic', 'Pop')),
    ('What is your favorite dish?', ('fish', 'meat', 'vegetables', 'all')),
    ('What is your favorite vehicle?', ('bike', 'car', 'motorbike', 'bus')),
    ('Do you like to travel?', ('yes', 'no')),


]


def populate_questions(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Question = apps.get_model('friendship_quiz', 'Question')
    Choice = apps.get_model('friendship_quiz', 'Choice')
    choices = []
    for question_text, answers in QUESTIONS:
        question = Question.objects.create(text=question_text)
        for choice_text in answers:
            choices.append(Choice(question=question, text=choice_text))
    Choice.objects.bulk_create(choices)


def clear_questions(apps, schema_editor):
    Question = apps.get_model('friendship_quiz', 'Question')
    Choice = apps.get_model('friendship_quiz', 'Choice')
    Choice.objects.all().delete()
    Question.objects.all().delete()



class Migration(migrations.Migration):

    dependencies = [
        ('friendship_quiz', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_questions, clear_questions),
    ]
