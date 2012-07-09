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

from django import forms
from captcha.fields import CaptchaField

from bugex_webapp.validators import validate_archive_file_extension
from bugex_webapp.validators import validate_archive_copyright
from bugex_webapp.validators import validate_test_case_name
from bugex_webapp.validators import validate_name

class EmailBaseForm(forms.Form):
    """The EmailBaseForm form.

    The EmailBaseForm is used as a more generic replacement for
    RecoverPasswordForm and RegistrationForm.
    """
    email_address = forms.EmailField(help_text='Your current email address')


class RegistrationForm(EmailBaseForm):
    captcha = CaptchaField()


class EmailPasswordBaseForm(EmailBaseForm):
    """The EmailPasswordBaseForm form.

    The EmailPasswordBaseForm inherits from EmailBaseForm and
    introduces a new field for entering passwords. This is used
    as a more generic replacement for LoginForm.
    """
    password = forms.CharField(
        min_length=8, max_length=8,
        help_text='Your current password.'
    )


class UserRequestForm(forms.Form):
    """The UserRequestForm form for uploading user requests.

    The UserRequestForm inherits the field `email_address` from
    EmailBaseForm.
    """
    code_archive = forms.FileField(
        validators=[validate_archive_file_extension],
        help_text='The archive (ZIP or JAR) that contains your code.'
    )
    test_case = forms.CharField(
        max_length=100,
        validators=[validate_test_case_name],
        help_text='The name of the failing test case related to your program.'
    )
    has_copyright = forms.BooleanField(
        required=False,
        validators=[validate_archive_copyright],
        label='Copyright confirmation',
        help_text='Please confirm that you own the copyright to the files' \
                  ' that you are going to upload.'
    )


class AdditionalTestCaseForm(forms.Form):
    """The AdditionalTestCaseForm form for uploading additional test cases."""
    additional_test_case = forms.FileField(
        help_text='The additional failing test case that you want to upload.'
    )


class ChangeEmailForm(forms.Form):
    """The ChangeEmailForm for changing a user's email address.

    The ChangeEmailForm inherits the fields `email_address` and `password`
    from the EmailPassWordBaseForm.
    """
    new_email_address_1 = forms.EmailField(
        help_text='Please enter your new email address.'
    )
    new_email_address_2 = forms.EmailField(
        help_text='Please re-enter your new email address.'
    )


class ContactForm(EmailBaseForm):
    """ The ContactForm for users to send questions, suggestions, etc.

    The ContactForm inherits the field 'email_address' from EmailBaseForm.
    """
    name = forms.CharField(
        max_length=50,
        validators=[validate_name],
        help_text='Your name'
    )
    message = forms.CharField(
        widget=forms.Textarea,
        help_text='Your message'
    )

