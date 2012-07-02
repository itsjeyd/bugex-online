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