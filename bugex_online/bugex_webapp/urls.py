# -*- coding: utf-8 -*-

"""
Project: BugEx Online
Authors: Amir Baradaran
         Tim Krones
         Frederik Leonhardt
         Christos Monogios
         Akmal Qodirov
         Iliana Simova
         Peter Stahl
"""

from django.conf.urls import patterns, include, url

from bugex_webapp.views import MainPageView, HowToPageView, ResultsPageView
from bugex_webapp.views import DeletePageView, UserPageView

urlpatterns = patterns('',
    url(r'main/$', MainPageView.as_view(), name='main-page'),
    url(r'howto/$', HowToPageView.as_view(), name='howto-page'),
    url(r'results/$', ResultsPageView.as_view(), name='results-page'),
    url(r'delete/$', DeletePageView.as_view(), name='delete-page'),
    url(r'user/$', UserPageView.as_view(), name='user-page'),
)
