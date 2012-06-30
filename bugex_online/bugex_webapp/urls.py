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
from bugex_webapp.previews import BugExFormPreview
from bugex_webapp.forms import EmailBaseForm, EmailPasswordBaseForm
from bugex_webapp.forms import UserRequestForm, AdditionalTestCaseForm
from bugex_webapp.forms import ChangeEmailForm

urlpatterns = patterns('',
    url(r'main/$', MainPageView.as_view(), name='main-page'),
    url(r'howto/$', HowToPageView.as_view(), name='howto-page'),
    url(r'results/$', ResultsPageView.as_view(), name='results-page'),
    url(r'delete/$', DeletePageView.as_view(), name='delete-page'),
    url(r'user/$', UserPageView.as_view(), name='user-page'),

    # These URLs are for checking the forms via the formtools app.
    url(r'form/emailbase$', BugExFormPreview(EmailBaseForm)),
    url(r'form/emailpasswordbase$', BugExFormPreview(EmailPasswordBaseForm)),
    url(r'form/userrequest$', BugExFormPreview(UserRequestForm)),
    url(r'form/additionaltestcase$', BugExFormPreview(AdditionalTestCaseForm)),
    url(r'form/changeemail$', BugExFormPreview(ChangeEmailForm)),
)
