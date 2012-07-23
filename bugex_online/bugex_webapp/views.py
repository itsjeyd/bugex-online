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
import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from bugex_webapp import UserRequestStatus, Notifications
from bugex_webapp.models import UserRequest, Fact
from bugex_webapp.forms import UserRequestForm, ChangeEmailForm, ContactForm
from bugex_webapp.forms import RegistrationForm, EmailBaseForm
from bugex_webapp.core_modules.password_generator import get_pronounceable_pass


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
            user = User.objects.get(email=email_address)
            new_password = get_pronounceable_pass(3,2)
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
        new_password = get_pronounceable_pass(3,2)

        try:
            user = User.objects.get(email=email_address)
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
            
            user = User.objects.create_user(
                username='-1', # dummy username just for now
                email=email_address,
                password=new_password
            )

            # now use id as username
            user.username = user.id
            user.save()

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
            user=request.user,
            test_case_name=user_req_form.cleaned_data['test_case'],
            archive_file=request.FILES['code_archive']
        )

        message= 'Upload successful! We have received your code.'

    else:
        message = 'Unfortunately, your request could not be processed.'

    template_context = {'user_req_form': user_req_form, 'message': message}

    return template_context


@login_required(login_url='/')
def provide_user_content(request):
    """Change a user's credentials, i.e. email address and password."""
    requests_by_user = UserRequest.objects.filter(user=request.user)

    if request.method == 'POST':

        if request.POST['form-type'] == u'change-email-form':
            template_context = _change_email_address(request)
            template_context['requests_by_user'] = requests_by_user

        elif request.POST['form-type'] == u'change-password-form':
            template_context = _change_password(request)
            template_context['requests_by_user'] = requests_by_user

    else:
        template_context = {'change_email_form': ChangeEmailForm(),
                            'requests_by_user': requests_by_user}

    return render(request, 'bugex_webapp/user.html', template_context)


def _change_password(request):
    """Change a user's password."""
    try:
        new_password = get_pronounceable_pass(3,2)
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
            message = 'The email addresses you entered are not identical.'

    else:
        message = 'Input not valid.'

    template_context = {
        'change_email_form': change_email_form,
        'message': message
    }

    return template_context


def _log_user_in(request):
    """Log a user in."""
    message = ''
    email_address = request.POST['username'] # this is actually the email
    password = request.POST['password']
    
    # a little workarounce, because we are looking up users based on email
    try:
        # lookup the correct user object
        pre_auth_user = User.objects.get(email=email_address)
    except ObjectDoesNotExist:
        user = None
    else:
        # authenticate with name
        user = authenticate(
                username=pre_auth_user.username, password=password)

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
    message = ''
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data['name']
            email_address = form.cleaned_data['email_address']
            message = form.cleaned_data['message']

            content = 'Name:\n' + name + \
                      '\n\nEmail:\n' + email_address + \
                      '\n\nMessage:\n'+ message
            send_mail('[Contact Form] from ' + name, content,
                      email_address, [settings.EMAIL_HOST_USER],
                      fail_silently=True)

            message = 'Thank you very much! We received your email.'

        else:
            message = 'Unfortunately, your contact request could not be processed.'

    else:
        form = ContactForm()

    template_context = {'form': form, 'message': message}

    return render(request, 'bugex_webapp/contact.html', template_context)


def show_bugex_result(request, token):
    """Prepare the results data to be shown for a single user request."""

    # first of all, we check if a user request is associated with the token
    user_request = get_object_or_404(UserRequest, token=token)

    # now we have to check the current status to properly inform the user
    ur_status = user_request.status

    if ur_status == UserRequestStatus.FINISHED:
        # prepare context and render response

        # Dictionary of facts
        # Format: fact_dict = {'Type_A': [(0, fact0), (1, fact1), ...],
        #                      'Type_B': [(2, fact2), (3, fact3), ...],
        #                      ...
        #                     }
        fact_list = enumerate(user_request.result.fact_set.all())
        fact_dict = {}
        for fact_type in Fact.FACT_TYPES:
            fact_dict[fact_type[0]] = []

        for number, fact in fact_list:
            fact_dict[fact.fact_type].append((number, fact))

        template_context = {
            'fact_dict': fact_dict,
            'token': token
        }
        return render(request, 'bugex_webapp/results.html', template_context)

    elif ur_status == UserRequestStatus.FAILED:
        # something went wrong
        message = "BugEx failed to process your input data.\
        Please try again or contact an administrator."
    elif ur_status == UserRequestStatus.DELETED:
        # already deleted, sorry.
        message = "This BugEx result has already been deleted."
    elif ur_status == UserRequestStatus.INVALID:
        # not our fault - the user messed it up!
        message = "The archive you provided was invalid.\
        Please try again."
    else:
        # still working..
        message = "Your results are not ready yet. Please give us some more\
        time and check again later."

    # .. and render it!
    return render(request, 'bugex_webapp/status.html',
            {'message': message,
            'pagetitle': 'Result status'})


@login_required(login_url='/')
def delete_bugex_result(request, delete_token):
    """Delete the results data for a specific user request."""

    # get user request
    user_request = get_object_or_404(UserRequest, delete_token=delete_token)

    # check if this request already has been deleted
    if user_request.status == UserRequestStatus.DELETED:
        message = 'This BugEx result has already been deleted.'
    else:
        try:
            # Deleting underlying archive file
            user_request.codearchive.archive_file.delete()
            # Deleting BugExResult, CodeArchive, all Facts, all SourceFiles,
            # all ClassFiles, all Folders, all Lines
            if user_request.result:
                # only try to delete result, if there actually is one
                user_request.result.delete()
                user_request.result = None # manually set relation to null
                user_request.save()
            user_request.codearchive.delete()
            # Delete the entire directory where the archive file was stored
            shutil.rmtree(user_request.folder)
            # Set user request status to DELETED
            user_request.update_status(UserRequestStatus.DELETED)

            message = 'Your BugEx result has been deleted successfully.'

        except Exception as e:
            # something unexpected, we have to log this
            message = 'Sorry, we could not delete this result.'
            logging.error(message+' Exception: '+str(e))

    # render status page with appropriate content
    return render(request, 'bugex_webapp/status.html',
            {'message': message,
            'pagetitle': 'Delete result'})


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
    package_name = '.'.join(class_name.split('.')[:-1])
    class_name = class_name.split('.')[-1] + '.java'

    ur = get_object_or_404(UserRequest, token=token)

    try:
        source_file = ur.codearchive.sourcefile_set.get(package=package_name, name=class_name)
    except ObjectDoesNotExist:
        #raise Http404
        # no source available
        return HttpResponse("Source code not available.", content_type="text/plain")
    else:
        return HttpResponse(source_file.content, content_type="text/plain")
