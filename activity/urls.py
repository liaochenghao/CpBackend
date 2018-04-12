# coding: utf-8
from django.conf.urls import url
from activity.views import ActivityView, ActivityStartAtView

urlpatterns = [
    url(r'^activity$', ActivityView.as_view()),
    url(r'^activity/start$', ActivityStartAtView.as_view()),
]
