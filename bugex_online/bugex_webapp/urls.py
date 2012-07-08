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

from bugex_webapp.views import HowToPageView, ResultsPageView
from bugex_webapp.views import DeletePageView, change_user_credentials, process_main_page_forms
from bugex_webapp.views import submit_contact_form, log_user_out

urlpatterns = patterns('',
    url(r'^$', process_main_page_forms, name='main-page'),
    url(r'^howto/$', HowToPageView.as_view(), name='howto-page'),
    # url(r'^results/$', ResultsPageView.as_view(), name='results-page-overview'),
    url(r'^result/(?P<token>[a-z0-9\-]{36})$', ResultsPageView.as_view(), name='results-page'),
    url(r'^delete/$', DeletePageView.as_view(), name='delete-page'),
    url(r'^account/$', change_user_credentials, name='user-page'),
    url(r'^contact/$', submit_contact_form, name='contact-page'),

    url(r'^account/logout/$', log_user_out, name='logout'),

    # This is for serving uploaded user files in development mode.
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)