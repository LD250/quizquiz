from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db import transaction

from .models import Choice, Question, Quiz
from .forms import SelectQuestionsForm, AnswerQuestionsForm


class QuestionsView(generic.FormView):
    template_name = 'friendship_quiz/select_questions.html'
    form_class = SelectQuestionsForm

    def form_valid(self, form):

        with transaction.atomic():
            quiz = Quiz.objects.create()
            questions = form.cleaned_data['questions']
            quiz.questions.add(*questions)
            self.success_url = reverse('friendship_quiz:take-quiz', kwargs={'quiz_id': quiz.id})

        return super(QuestionsView, self).form_valid(form)


class TakeQuiz(generic.FormView):
    template_name = 'friendship_quiz/answer_questions.html'
    form_class = AnswerQuestionsForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        quiz = get_object_or_404(Quiz, id=self.kwargs['quiz_id'])
        kwargs.update({'quiz': quiz})
        return kwargs

    def form_valid(self, form):

        self.success_url = '{0}?next={1}'.format(
            reverse('social:begin', kwargs={'backend': 'facebook'}),
            reverse('friendship_quiz:done')
        )

        return super(TakeQuiz, self).form_valid(form)


class Done(generic.TemplateView):
    template_name = 'friendship_quiz/done.html'
