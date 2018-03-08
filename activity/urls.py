# coding: utf-8
from django.conf.urls import url
from activity.views import ActivityView

urlpatterns = [
    url(r'^activity', ActivityView.as_view()),
]
