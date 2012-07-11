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

from bugex_webapp.views import HowToPageView
from bugex_webapp.views import change_user_credentials, process_main_page_forms
from bugex_webapp.views import submit_contact_form, log_user_out, show_bugex_result
from bugex_webapp.views import delete_bugex_result, get_source_file_content
from bugex_webapp.views import results_overview

urlpatterns = patterns('',
    url(r'^$', process_main_page_forms, name='main-page'),
    url(r'^howto/$', HowToPageView.as_view(), name='howto-page'),
    # url(r'^results/$', ResultsPageView.as_view(), name='results-page-overview'),
    url(r'^result/(?P<token>[a-z0-9\-]{36})$', show_bugex_result, name='results-page'),
    url(r'^delete/(?P<delete_token>[a-z0-9\-]{36})$', delete_bugex_result, name='delete-page'),
    url(r'^account/$', change_user_credentials, name='user-page'),
    url(r'^contact/$', submit_contact_form, name='contact-page'),

    url(r'^account/logout/$', log_user_out, name='logout'),

    url(r'^overview/(?P<user_id>[1-9][0-9]*)$', results_overview, name='overview-page'),
    url(r'^source/(?P<token>[a-z0-9\-]{36})/(?P<class_name>([a-z0-9]+\.)+[A-Z][A-Za-z0-9]+)$', get_source_file_content, name='source-page'),

    # This is for serving uploaded user files in development mode.
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
