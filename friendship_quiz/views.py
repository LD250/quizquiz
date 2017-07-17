from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question, Quiz, Answer
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

        return super().form_valid(form)


class TakeQuiz(generic.FormView):
    template_name = 'friendship_quiz/answer_questions.html'
    form_class = AnswerQuestionsForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        quiz = get_object_or_404(Quiz, id=self.kwargs['quiz_id'])
        kwargs.update({'quiz': quiz})
        return kwargs

    def form_valid(self, form):

        self.request.session[self.kwargs['quiz_id']] = {
            "cleaned_data": form.cleaned_data
        }
        if self.request.user.is_authenticated():
            self.success_url = reverse('friendship_quiz:done', kwargs={'quiz_id': self.kwargs['quiz_id']})
        else:
            # deal with anonymous user info
            self.success_url = '{0}?next={1}'.format(
                reverse('social:begin', kwargs={'backend': 'facebook'}),
                reverse('friendship_quiz:done', kwargs={'quiz_id': self.kwargs['quiz_id']})
            )

        return super().form_valid(form)


class Done(LoginRequiredMixin, generic.TemplateView):
    template_name = 'friendship_quiz/done.html'

    def create_answers(self, user, quiz_id, quiz_answers):
        Answer.objects.filter(quiz_id=quiz_id, user=user).delete()
        choices_ids = quiz_answers.values()
        choices = Choice.objects.filter(id__in=choices_ids).select_related('question')
        answers = []
        for choice in choices:
            answers.append(
                Answer(
                    question=choice.question,
                    choice=choice,
                    quiz_id=quiz_id,
                    user=user
                )
            )
        Answer.objects.bulk_create(answers)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        quiz_answers = self.request.session[self.kwargs['quiz_id']]["cleaned_data"]
        if quiz_answers:
            self.create_answers(self.request.user, self.kwargs['quiz_id'], quiz_answers)
            kwargs['quiz_url'] = reverse(
                'friendship_quiz:take-quiz',
                kwargs={'quiz_id': self.kwargs['quiz_id']}
            )

        kwargs['quiz_has_answers'] = bool(quiz_answers)

        return kwargs
