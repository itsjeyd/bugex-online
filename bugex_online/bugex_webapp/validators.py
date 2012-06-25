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
            '{0} is not a Java source file'.format(file_name)
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
            '{0} is not a Java class file'.format(file_name)
        )