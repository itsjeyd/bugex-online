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

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from bugex_webapp.views import MainPageView, HowToPageView, ResultsPageView
from bugex_webapp.views import DeletePageView, UserPageView, submit_user_request

urlpatterns = patterns('',
    url(r'main/$', MainPageView.as_view(), name='main-page'),
    url(r'howto/$', HowToPageView.as_view(), name='howto-page'),
    url(r'results/$', ResultsPageView.as_view(), name='results-page'),
    url(r'delete/$', DeletePageView.as_view(), name='delete-page'),
    # When creating this URL pattern, the user page inside the admin
    # interface cannot be opened anymore. Have to examine that later on.
    #url(r'user/$', UserPageView.as_view(), name='user-page'),

    # This is for serving uploaded user files in development mode.
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'formtest/$', submit_user_request, name='formtest-page'),
    )