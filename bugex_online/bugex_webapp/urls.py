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

from bugex_webapp.views import MainPageView, HowToPageView, ResultsPageView, MainPageLoginRegistrationView
from bugex_webapp.views import DeletePageView, UserPageView, submit_user_request, change_email_request, create_new_user
from bugex_webapp.views import submit_contact_form

urlpatterns = patterns('',
    url(r'main/$', submit_user_request, name='main-page'),
    url(r'howto/$', HowToPageView.as_view(), name='howto-page'),
    url(r'results/$', ResultsPageView.as_view(), name='results-page'),
    url(r'delete/$', DeletePageView.as_view(), name='delete-page'),
    url(r'user/$', change_email_request, name='user-page'),
    url(r'main_with_login/$', MainPageLoginRegistrationView.as_view(), name='main_with_login-page'),
    url(r'contact/$', submit_contact_form, name='contact-page'),
    # When creating this URL pattern, the user page inside the admin
    # interface cannot be opened anymore. Have to examine that later on.
    #url(r'user/$', UserPageView.as_view(), name='user-page'),

    # This is for serving uploaded user files in development mode.
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'formtest/$', submit_user_request, name='formtest-page'),
    )