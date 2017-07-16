from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^how-well-do-you-match-your-best-friend-questions/',
        include('friendship_quiz.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(pattern_name='friendship_quiz:select-questions', permanent=False))
]