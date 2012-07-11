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

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_admins, send_mail
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from bugex_webapp import UserRequestStatus, Notifications
from bugex_webapp.models import UserRequest, Fact
from bugex_webapp.forms import UserRequestForm, ChangeEmailForm, ContactForm
from bugex_webapp.forms import RegistrationForm, EmailBaseForm

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
    """Process the forms on the main page."""
    if request.method == 'POST':
        if request.POST['form-type'] == u'login-form':
            template_context = _log_user_in(request)

        elif request.POST['form-type'] == u'user-request-form':
            template_context = _submit_user_request(request)

        elif request.POST['form-type'] == u'registration-form':
            template_context = _register_user(request)

        elif request.POST['form-type'] == u'password-recovery-form':
            template_context = _recover_password(request)

    else:
        template_context = {
            'auth_form': AuthenticationForm(),
            'registration_form': RegistrationForm(),
            'user_req_form': UserRequestForm(),
            'password_recovery_form': EmailBaseForm()
        }

    return render(request, 'bugex_webapp/main.html', template_context)


def _recover_password(request):
    """Recover the password for a particular user."""
    password_recovery_form = EmailBaseForm(request.POST)

    if password_recovery_form.is_valid():
        email_address = password_recovery_form.cleaned_data['email_address']

        try:
            user = User.objects.get(username=email_address)
            new_password = User.objects.make_random_password(length=8)
            user.set_password(new_password)
            user.save()

            send_mail(
                subject=Notifications.CONTENT['RECOVERED_PASSWORD']['subject'],
                message=Notifications.HEADER_FOOTER.format(
                    Notifications.CONTENT['RECOVERED_PASSWORD']['content']
                    .format(new_password)
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )

            message = 'The password for user "{0}" has been recovered '\
                      'successfully and will be sent to your ' \
                      'email address.'.format(email_address)

        except User.DoesNotExist:
            message = 'The user "{0}" does not exist in the ' \
                      'database.'.format(email_address)

    else:
        message = 'You have not entered a valid email address.'

    template_context = {
        'auth_form': AuthenticationForm(),
        'registration_form': RegistrationForm(),
        'password_recovery_form': password_recovery_form,
        'message': message
    }

    return template_context


def _register_user(request):
    """Register a new user in the database."""
    registration_form = RegistrationForm(request.POST)

    if registration_form.is_valid():
        email_address = registration_form.cleaned_data['email_address']
        new_password = User.objects.make_random_password(length=8)

        try:
            user = User.objects.get(username=email_address)
            user.set_password(new_password)
            user.save()

            send_mail(
                subject=Notifications.CONTENT['RECOVERED_PASSWORD']['subject'],
                message=Notifications.HEADER_FOOTER.format(
                    Notifications.CONTENT['RECOVERED_PASSWORD']['content']
                    .format(new_password)
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email_address],
            )

            message = 'This email address is already registered in the '\
                      'database. An email containing the password has been '\
                      'sent to this address.'

        except User.DoesNotExist:

            User.objects.create_user(
                username=email_address,
                email=email_address,
                password=new_password
            )

            send_mail(
                subject=Notifications.CONTENT['USER_REGISTERED']['subject'],
                message=Notifications.HEADER_FOOTER.format(
                    Notifications.CONTENT['USER_REGISTERED']['content']
                    .format(
                        email_address, new_password
                    )
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email_address],
            )

            message = 'User "{0}" has been created successfully.'.format(
                email_address
            )

    else:
        message = 'User could not be created. Please try again.'

    template_context = {
        'auth_form': AuthenticationForm(),
        'registration_form': registration_form,
        'password_recovery_form': EmailBaseForm(),
        'message': message
    }

    return template_context


def _submit_user_request(request):
    """Submit a user request."""
    user_req_form = UserRequestForm(request.POST, request.FILES)

    if user_req_form.is_valid():

        UserRequest.new(
            user=get_or_create_user(request.user.email),
            test_case_name=user_req_form.cleaned_data['test_case'],
            archive_file=request.FILES['code_archive']
        )

        message= 'Upload successful! We have received your code.'

    else:
        message = 'Unfortunately, your request could not be processed.'

    template_context = {'user_req_form': user_req_form, 'message': message}

    return template_context


@login_required(login_url='/')
def change_user_credentials(request):
    """Change a user's credentials, i.e. email address and password."""
    if request.method == 'POST':

        if request.POST['form-type'] == u'change-email-form':
            template_context = _change_email_address(request)

        elif request.POST['form-type'] == u'change-password-form':
            template_context = _change_password(request)

    else:
        template_context = {'change_email_form': ChangeEmailForm()}

    return render(request, 'bugex_webapp/user.html', template_context)


def _change_password(request):
    """Change a user's password."""
    try:
        new_password = User.objects.make_random_password(length=8)
        request.user.set_password(new_password)
        request.user.save()

        send_mail(
            subject=Notifications.CONTENT['CHANGED_PASSWORD']['subject'],
            message=Notifications.HEADER_FOOTER.format(
                Notifications.CONTENT['CHANGED_PASSWORD']['content']
                .format(new_password)
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
        )

        message = 'Your new password has been successfully set.'

    except:
        message = 'Failure: Your new password could not be created.'

    template_context = {
        'change_email_form': ChangeEmailForm(),
        'message': message
    }

    return template_context


def _change_email_address(request):
    """Change a user's current email address."""
    change_email_form = ChangeEmailForm(request.POST)
    message = ''

    if change_email_form.is_valid():

        new_email_address_1 = change_email_form.cleaned_data['new_email_address_1']
        new_email_address_2 = change_email_form.cleaned_data['new_email_address_2']

        if new_email_address_1 == new_email_address_2:

            old_email_address = request.user.email
            request.user.username = new_email_address_2
            request.user.email = new_email_address_2
            request.user.save()

            send_mail(
                subject=Notifications.CONTENT['CHANGED_EMAIL_ADDRESS']['subject'],
                message=Notifications.HEADER_FOOTER.format(
                    Notifications.CONTENT['CHANGED_EMAIL_ADDRESS']['content']
                    .format(new_email_address_2)
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[old_email_address],
            )

            message = 'Your new email address has been successfully set.'

        else:
            message = 'Your entered email addresses are not identical.'

    else:
        message = 'This form is not valid.'

    template_context = {
        'change_email_form': change_email_form,
        'message': message
    }

    return template_context


def _log_user_in(request):
    """Log a user in."""
    message = ''
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            message = 'Your account has been disabled. ' \
                      'Please contact the administrator.'
    else:
        message = 'Your username and password didn\'t match. Please try again.'

    template_context = {
        'user_req_form': UserRequestForm(),
        'auth_form': AuthenticationForm(),
        'registration_form': RegistrationForm(),
        'password_recovery_form': EmailBaseForm(),
        'message': message,
    }

    return template_context


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
            
            content = 'Name:\n' + request.POST['name'] + \
                      '\n\nEmail:\n' + request.POST['email_address'] + \
                      '\n\nMessage:\n'+ request.POST['message']
            send_mail('[Contact Form] from ' + request.POST['name'], content, 
                      request.POST['email_address'], ['bugexonline@gmail.com'], 
                      fail_silently=True)

            messages.success(request, 'We received your email!')

        else:
            messages.error(
                request, 'Unfortunately, your request could not be processed!')

    else:
        form = ContactForm()

    return render(request, 'bugex_webapp/contact.html', {'form': form,})


def show_bugex_result(request, token):
    """Prepare the results data to be shown for a single user request."""

    try:
        user_request = UserRequest.objects.get(token=token)
        fact_type_list = [fact_type[0] for fact_type in Fact.FACT_TYPES]
        fact_list = user_request.result.fact_set.all()
        if fact_list:
            template_context = {
                'fact_type_list': fact_type_list,
                'fact_list': fact_list,
                'token': token
            }
            return render(request, 'bugex_webapp/results.html', template_context)

    except ObjectDoesNotExist:
        message = 'This BugEx result has already been deleted.'
        return render(request, 'bugex_webapp/delete.html', {'message': message})


def delete_bugex_result(request, delete_token):
    """Delete the results data for a specific user request."""

    # TODO: TestCase cannot be deleted. Make relation optional?
    try:
        user_request = UserRequest.objects.get(delete_token=delete_token)
        # Deleting underlying archive file
        user_request.codearchive.archive_file.delete()
        # Deleting BugExResult, CodeArchive, all Facts, all SourceFiles,
        # all ClassFiles, all Folders, all Lines
        user_request.result.delete()
        
        print 'alright: '+str(user_request.result)
        user_request.result = None
        user_request.save()
        # Delete the entire directory where the archive file was stored
        shutil.rmtree(user_request.folder)
        # Set user request status to DELETED
        user_request.update_status(UserRequestStatus.DELETED)

        message = 'Your BugEx result has been deleted successfully.'

    except ObjectDoesNotExist:
        message = 'This BugEx result has already been deleted.'

    return render(request, 'bugex_webapp/delete.html', {'message': message})


def get_source_file_content(request, token, class_name):
    """
    Returns the content of a java source code file, identified by the unique
    Token if the UserRequest and the fully qualified class name.

    Returns the content as plain text or 404, if the user request and/or source
    file does not exist.

    Arguments:
    token -- see UserRequest token
    class_name -- e.g. 'my.package.MyClass'
    """
    try:
        package_name = '.'.join(class_name.split('.')[:-1])
        class_name = class_name.split('.')[-1] + '.java'

        ur = UserRequest.objects.get(token=token)
        source_file = ur.codearchive.sourcefile_set.get(package=package_name, name=class_name)
    except ObjectDoesNotExist:
        raise Http404
    else:
        return HttpResponse(source_file.content, content_type="text/plain")
