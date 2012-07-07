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

from django.core.mail import mail_admins
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from bugex_webapp.models import UserRequest, TestCase, CodeArchive
from bugex_webapp.forms import UserRequestForm, ChangeEmailForm, ContactForm

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


class ContactPageView(TemplateView):
    template_name = 'bugex_webapp/contact.html'
    

class MainPageLoginRegistrationView(TemplateView):
    template_name = 'bugex_webapp/main_with_login.html'


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


def submit_user_request(request):
    """Submit a user request.

    1. Bind the entered data to the UserRequestForm.
    2. Validate the form.
    3. Create a new user instance or get it from the database, if present.
    4. Create and save a new TestCase instance.
    5. Create and save a new CodeArchive instance.
    6. Create and save a new UserRequest instance.
    7. Send a confirmation email to the user.
       (Email will be sent to the console for testing purposes.)
    8. Render a template with the given form context.
       (Just for testing purposes.)

    """
    if request.method == 'POST':
        form = UserRequestForm(request.POST, request.FILES)

        if form.is_valid():

            UserRequest.new(
                user=get_or_create_user(form.cleaned_data['email_address']),
                test_case_name=form.cleaned_data['test_case'],
                archive_file=request.FILES['code_archive']
            )

            messages.success(request, 'Form submission was successful!')

        else:
            messages.error(request, 'Form submission failed!')

    else:
        form = UserRequestForm()

    return render(request, 'bugex_webapp/main.html', {'form': form,})


def change_email_address(request):
    """Change a user's current email address."""
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)

        if form.is_valid():

            current_email_address = form.cleaned_data['email_address']
            password = form.cleaned_data['password']
            new_email_address_1 = form.cleaned_data['new_email_address_1']
            new_email_address_2 = form.cleaned_data['new_email_address_2']

            user = User.objects.get(username=current_email_address)

            if user.check_password(password):
                if new_email_address_1 == new_email_address_2:

                    user.username = new_email_address_2
                    user.email = new_email_address_2
                    user.save()

                    messages.success(request,
                        'Your new email address has been set.'
                    )


            messages.success(request, 'Form submission was successful!')

        else:
            messages.error(request, 'Form submission failed!')

    else:
        form = ChangeEmailForm()

    return render(request, 'bugex_webapp/user.html', {'form': form,})


def log_user_in(request):
    """Log a user in."""
    error_message = ''
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/user/')
            else:
                error_message = 'not_active'
        else:
            error_message = 'not_authenticated'

    else:
        form = AuthenticationForm()

    dictionary = {'form': form, 'error': error_message}

    return render(request, '', dictionary)


def log_user_out(request):
    """Log a currently logged in user out."""
    logout(request)
    return render(request, '')


def change_password_request(request):
    """Test function for changing the user's password
    """    
    email_address = request.POST['email_address']
    user = User.objects.get(username__exact=email_address)
    user.make_random_password(length=8)
    user.save()
    user.email_user(
                subject='you successfully changed your password',
                message='dear user,\n\n your new password is "' + 
                        user.password + 
                        '" .\n\nbest regards,\n'\
                        'the bugex online group'
            )
    

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
            messages.error(request, 'Form submission failed!')

    else:
        form = ContactForm()

    return render(request, 'bugex_webapp/contact.html', {'form': form,})
