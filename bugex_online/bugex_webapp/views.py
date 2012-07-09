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

import shutil

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_admins
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response

from bugex_webapp import UserRequestStatus
from bugex_webapp.models import UserRequest, Fact
from bugex_webapp.forms import UserRequestForm, ChangeEmailForm, ContactForm, RegistrationForm

class HowToPageView(TemplateView):
    template_name = 'bugex_webapp/howto.html'


def get_or_create_user(email_address):
    """Create and return a new user.

    If the user is already present in the database, return this user.

    """
    if not User.objects.filter(username=email_address).count():
        password = User.objects.make_random_password(length=8)
        user = User.objects.create_user(
            username=email_address,
            email=email_address,
            password=password
        )
        return user

    return User.objects.get(username=email_address)


def process_main_page_forms(request):
    if request.method == 'POST':
        if request.POST['form-type'] == u'login-form':
            error_message = _log_user_in(request)
            template_context = {
                'auth_form': AuthenticationForm(),
                'user_req_form': UserRequestForm(),
                'error': error_message,
                'registration_form': RegistrationForm()
            }

        elif request.POST['form-type'] == u'user-request-form':
            template_context = _submit_user_request(request)

        elif request.POST['form-type'] == u'registration-form':
            registration_form = RegistrationForm(request.POST)
            message = ''

            if registration_form.is_valid():
                email_address = registration_form.cleaned_data['email_address']

                if not User.objects.filter(username=email_address).count():
                    password = User.objects.make_random_password(length=8)
                    print password
                    User.objects.create_user(
                        username=email_address,
                        email=email_address,
                        password=password
                    )

                    # messages.success(request, 'User has been created successfully.')
                    message = 'User "{0}" has been created successfully.'.format(email_address)
            else:
                # messages.error(request, 'User could not be created.')
                message = 'User could not be created. Please try again.'

            template_context = {
                'auth_form': AuthenticationForm(),
                'registration_form': registration_form,
                'message': message
            }

    else:
        template_context = {
            'auth_form': AuthenticationForm(),
            'user_req_form': UserRequestForm(),
            'registration_form': RegistrationForm()
        }


    return render(request, 'bugex_webapp/main.html', template_context)


def _submit_user_request(request):
    """Submit a user request."""

    user_req_form = UserRequestForm(request.POST, request.FILES)

    if user_req_form.is_valid():

        UserRequest.new(
            user=get_or_create_user(request.user.email),
            test_case_name=user_req_form.cleaned_data['test_case'],
            archive_file=request.FILES['code_archive']
        )

        messages.success(
            request, 'Upload successful! We have received your code.')

    else:
        messages.error(
            request, 'Unfortunately, your request could not be processed.')

    template_context = {'user_req_form': user_req_form}

    return template_context


@login_required(login_url='/')
def change_user_credentials(request):
    """Change a user's credentials, i.e. email address and password."""
    if request.method == 'POST':
        if request.POST['form-type'] == u'change-email-form':
            change_email_form = _change_email_address(request)
        elif request.POST['form-type'] == u'change-password-form':
            _change_password(request)
            change_email_form = ChangeEmailForm()

    else:
        change_email_form = ChangeEmailForm()

    return render(request,
        'bugex_webapp/user.html',
        {'form': change_email_form}
    )


def _change_password(request):
    """Change a user's password."""
    new_password = User.objects.make_random_password(length=8)
    print new_password
    request.user.set_password(new_password)
    request.user.save()

    messages.success(request, 'Your new password has been set.')


def _change_email_address(request):
    """Change a user's current email address."""

    change_email_form = ChangeEmailForm(request.POST)

    if change_email_form.is_valid():

        new_email_address_1 = change_email_form.cleaned_data['new_email_address_1']
        new_email_address_2 = change_email_form.cleaned_data['new_email_address_2']

        if new_email_address_1 == new_email_address_2:

            request.user.username = new_email_address_2
            request.user.email = new_email_address_2
            request.user.save()

            messages.success(request,
                'Your new email address has been set.'
            )

        else:
            messages.error(request, 'Your entered email addresses are not identical.')

    else:
        messages.error(request, 'This form is not valid.')

    return change_email_form


def _log_user_in(request):
    """Log a user in."""
    error_message = ''
    print request.POST
    auth_form = AuthenticationForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'not_active'
    else:
        error_message = 'not_authenticated'

    return error_message


def log_user_out(request):
    """Log a currently logged in user out."""
    logout(request)
    return HttpResponseRedirect('/')


def submit_contact_form(request):
    """Submit a contact form request
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            mail_admins('Email from the contact form',
                'Name: ' + request.POST['name'] + '\n\nMessage: '+ request.POST['message']
            )

            messages.success(request, 'We received your email!')

        else:
            messages.error(
                request, 'Unfortunately, your request could not be processed!')

    else:
        form = ContactForm()

    return render(request, 'bugex_webapp/contact.html', {'form': form,})


def show_bugex_result(request, token):
    """Prepare the results data to be shown for a single user request."""
    user_request = UserRequest.objects.get(token=token)
    fact_type_list = [fact_type[0] for fact_type in Fact.FACT_TYPES]
    fact_list = user_request.result.fact_set.all()
    if fact_list:
        template_context = {'fact_type_list': fact_type_list, 'fact_list': fact_list}
        return render(request, 'bugex_webapp/results.html', template_context)

    message = 'This BugEx result has already been deleted.'
    return render(request, 'bugex_webapp/delete.html', {'message': message})


def delete_bugex_result(request, delete_token):
    """Delete the results data for a specific user request."""

    # TODO: TestCase and BugExResult can not be deleted because of
    # one-to-one relations. Make relations optional?
    try:
        user_request = UserRequest.objects.get(delete_token=delete_token)
        # Deleting underlying archive file
        user_request.codearchive.archive_file.delete()
        # Deleting CodeArchive, all SourceFiles, all ClassFiles, all Folders, all Lines
        user_request.codearchive.delete()
        # Deleting all Facts
        user_request.result.fact_set.all().delete()
        # Delete the entire directory where the archive file was stored
        shutil.rmtree(user_request.folder)
        # Set user request status to DELETED
        user_request.status = UserRequestStatus.DELETED
        user_request.save()

        message = 'Your BugEx result has been deleted successfully.'

    except ObjectDoesNotExist:
        message = 'This BugEx result has already been deleted.'

    return render(request, 'bugex_webapp/delete.html', {'message': message})


def get_source_file_content(request, token, class_name):
    ur = UserRequest.objects.get(token=token)

    package_name = '.'.join(class_name.split('.')[:-1])
    class_name = class_name.split('.')[-1] + '.java'

    source_file = ur.codearchive.sourcefile_set.get(package=package_name, name=class_name)

    return HttpResponse(source_file.content, content_type="text/plain")
