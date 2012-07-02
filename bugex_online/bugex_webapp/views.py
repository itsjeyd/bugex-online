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

import os
import uuid

from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render

from bugex_webapp import PENDING
from bugex_webapp.models import UserRequest, TestCase, CodeArchive
from bugex_webapp.forms import UserRequestForm

class MainPageView(TemplateView):
    template_name = 'bugex_webapp/main.html'


class HowToPageView(TemplateView):
    template_name = 'bugex_webapp/howto.html'


class ResultsPageView(TemplateView):
    template_name = 'bugex_webapp/results.html'


class DeletePageView(TemplateView):
    template_name = 'bugex_webapp/delete.html'


class UserPageView(TemplateView):
    template_name = 'bugex_webapp/user.html'


def username_present(username):
    """Determine whether a particular user exists in the database."""
    if User.objects.filter(username=username).count():
        return True
    return False


def create_new_user(email_address):
    """Create and return a new user.

    If the user is already present in the database, return this user.

    """
    if not username_present(username=email_address):
        password = User.objects.make_random_password(length=8)
        user = User.objects.create_user(
            username=email_address,
            email=email_address,
            password=password
        )
        return user

    return User.objects.get(username=email_address)


def submit_user_request(request):
    """Submit a user request.

    1.  Bind the entered data to the UserRequestForm.
    2.  Validate the form.
    3.  Create a new user instance or get it from the database, if present.
    4.  Create and save a new TestCase instance.
    5.  Create and save a new UserRequest instance.
    6.  Create and save a new CodeArchive instance.
    7.  Add the CodeArchive instance to the UserRequest's code_archive field.
    8.  Save again the UserRequest instance.
    9.  Send a confirmation email to the user.
        (Email will be sent to the console for testing purposes.)
    10. Render a template with the given form context.
       (Just for testing purposes.)

    """
    if request.method == 'POST':
        form = UserRequestForm(request.POST, request.FILES)

        if form.is_valid():
            user = create_new_user(form.cleaned_data['email_address'])

            test_case = TestCase.objects.create(
                name=form.cleaned_data['test_case']
            )

            user_request = UserRequest()
            user_request.user = user
            user_request.token = uuid.uuid4()
            user_request.status = PENDING
            user_request.test_case = test_case
            user_request.save()

            code_archive = CodeArchive()
            archive_content = request.FILES['code_archive']
            archive_name = archive_content.name
            archive_file_ext = os.path.splitext(archive_name)[1][1:].strip()

            code_archive.archive_file.save(
                name=archive_name,
                content=archive_content
            )

            code_archive.archive_format = archive_file_ext.upper()
            code_archive.save()

            user_request.code_archive = code_archive
            user_request.save()

            user.email_user(
                subject='We successfully received your request',
                message='Dear user,\n\nyour request for the ' \
                        'code archive "' + archive_name + '" was ' \
                        'processed successfully.\n\nBest regards,\n' \
                        'The BugEx Online Group'
            )

            messages.success(request, 'Form submission was successful!')

        else:
            messages.error(request, 'Form submission failed!')

    else:
        form = UserRequestForm()

    return render(request, 'formtests/form.html', {'form': form})