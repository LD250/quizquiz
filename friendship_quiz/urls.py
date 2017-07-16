from django.conf.urls import url

from . import views

app_name = 'friendship_quiz'
urlpatterns = [
    url(r'^$', views.QuestionsView.as_view(), name='select-questions'),
    url(r'^(?P<quiz_id>[0-9a-f-]+)$', views.TakeQuiz.as_view(), name='take-quiz'),
    url(r'^done$', views.Done.as_view(), name='done'),
]