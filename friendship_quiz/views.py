from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from friendship_quiz.calculate_match import CalculateMatch
from .models import Choice, Quiz, Answer
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
            self.request.session['created_quiz'] = str(quiz.id)

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
        return True

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        quiz_id = self.kwargs['quiz_id']
        quiz_answers = self.request.session[self.kwargs['quiz_id']]["cleaned_data"]
        already_passed = Answer.objects.filter(quiz_id=quiz_id, user=self.request.user).exists()
        if (not already_passed and 'created_quiz' in self.request.session and
                self.request.session['created_quiz'] == quiz_id):
            Quiz.objects.filter(id=quiz_id, created_by=None).update(created_by=self.request.user)
            del self.request.session['created_quiz']
        if quiz_answers and not already_passed:
            already_passed = self.create_answers(self.request.user, quiz_id, quiz_answers)
        if already_passed:
            kwargs['quiz_url'] = reverse(
                'friendship_quiz:take-quiz',
                kwargs={'quiz_id': self.kwargs['quiz_id']}
            )
        quiz = Quiz.objects.select_related('created_by').get(id=quiz_id)

        if quiz.created_by and quiz.created_by != self.request.user:
            match = CalculateMatch().calculate_match(
                Answer.objects.filter(quiz_id=quiz_id, user=self.request.user),
                Answer.objects.filter(quiz_id=quiz_id, user=quiz.created_by)
            )
            kwargs['match'] = "{0:.2f} %".format(match * 100)
            kwargs['friend_name'] = quiz.created_by.first_name

        return kwargs
