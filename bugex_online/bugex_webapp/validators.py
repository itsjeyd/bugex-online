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

This module contains custom validator functions for validating fields
of models and forms. For more information about validators, see:

https://docs.djangoproject.com/en/1.4/ref/validators/

"""

import re

from django.core.exceptions import ValidationError

def validate_source_file_extension(file_name):
    """Validate the name field of the SourceFile model.

    Before saving an instance of the SourceFile model into
    the database, this function will be called, checking for
    the correct file extension `.java`. If the extension is
    different, a ValidationError is raised and the instance
    will not be saved to the database.

    Arguments:
    file_name -- value of SourceFile model's `name` field

    """
    if not file_name.endswith('.java'):
        raise ValidationError(
            u'{0} is not a Java source file'.format(file_name)
        )

def validate_class_file_extension(file_name):
    """Validate the name field of the ClassFile model.

    Before saving an instance of the ClassFile model into
    the database, this function will be called, checking for
    the correct file extension `.class`. If the extension is
    different, a ValidationError is raised and the instance
    will not be saved to the database.

    Arguments:
    file_name -- value of ClassFile model's `name` field

    """
    if not file_name.endswith('.class'):
        raise ValidationError(
            u'{0} is not a Java class file'.format(file_name)
        )

def validate_archive_file_extension(archive_file):
    """Validate the archive_file field of the CodeArchive model.

    Before saving an instance of the CodeArchive model into
    the database, this function will be called, checking for
    the correct archive file extension. If the extension is different,
    a ValidationError is raised and the instance will not be
    saved to the database.

    Arguments:
    archive_file -- value of CodeArchive model's `archive_file` field

    """
    if not archive_file.name.endswith(('.zip', '.jar')):
        raise ValidationError(
            u'{0} is not a valid archive format'.format(archive_file.name)
        )

def validate_archive_copyright(has_copyright):
    """Validate the has_copyright field of the UserRequestForm form.

    Before saving an instance of the CodeArchive model into
    the database, this function will be called, checking whether
    the user confirmed to own the copyright for the code they intend to upload.
    If the user refuses to confirm, a ValidationError is raised and the
    instance will not be saved to the database.

    Arguments:
    has_copyright -- Boolean value of UserRequestForm form's
                    `has_copyright` field

    """
    if not has_copyright:
        raise ValidationError(
            u'You must confirm to own the copyright on the code archive'
        )

def validate_test_case_name(test_case_name):
    """
    Validate the name of a test case in the TestCase model and in the
    UserRequestForm form.

    Before saving an instance of the TestCase model into
    the database, this function will be called, checking whether
    the test case name is of the format "de.mypackage.TestMyClass#testGetMin".
    If the format is not correct, a ValidationError is raised and the
    instance will not be saved to the database.

    Arguments:
    test_case_name -- value of TestCase model's `name` field

    """
    test_case_name_pattern = re.compile(r"""^
        (?P<package> [a-z0-9]+\. )+
        (?P<class> [A-Z][A-Za-z0-9]+\# )
        (?P<method> [a-z][A-Za-z0-9]+ )$""",
        re.VERBOSE
    )
    if not test_case_name_pattern.match(test_case_name):
        raise ValidationError(
            u'Your entered test case name does not have the ' +
            u'needed format "de.mypackage.TestMyClass#testGetMin"'
        )
        
        
def validate_name(name):
    """
    Validate the name of a user in the contact form.
    
    We are accepting only letters and numbers as valid name

    Arguments:
    name -- value of the name of the user

    """
    name_pattern = re.compile(r"""
        ^[a-zA-Z][a-zA-Z\d]*$""",
        re.VERBOSE
    )
    if not name_pattern.match(name):
        raise ValidationError(
            u'Your entered a name does not have the ' +
            u'letters or numbers only'
        )