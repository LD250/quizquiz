from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import Question, Quiz

MINIMUM_QUESTIONS = 4
MAXIMUM_QUESTIONS = 5


class SelectQuestionsForm(forms.Form):
    error_messages = {
        'selected_count_not_correct': format_lazy(
            _('You have to select from {0} to {1} questions'),
            MINIMUM_QUESTIONS,
            MAXIMUM_QUESTIONS),
    }
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def clean_questions(self):
        questions_count = len(self.cleaned_data['questions'])
        if questions_count < MINIMUM_QUESTIONS or questions_count > MAXIMUM_QUESTIONS:
            self.add_error(
                'questions',
                self.error_messages['selected_count_not_correct']
            )
        return self.cleaned_data['questions']


class AnswerQuestionsForm(forms.Form):
    error_messages = {
        'answer_not_correct': _('Please select answer')
    }

    def __init__(self, *args, quiz=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.questions = quiz.questions.prefetch_related('choice_set').all()

        for question in self.questions:
            choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
            self.fields['question_{id}'.format(id=question.id)] = forms.ChoiceField(
                choices=choices,
                label=question.text
            )

    def clean(self):
        clean_data = self.cleaned_data
        return clean_data
