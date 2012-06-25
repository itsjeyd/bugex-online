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

import uuid
from os import path
from django.core.exceptions import ValidationError
from django.db import models
from bugex_webapp import PENDING
from bugex_webapp.validators import validate_source_file_extension
from bugex_webapp.validators import validate_class_file_extension
from core_config import WORKING_DIR


class UserRequest(models.Model):
    user = models.ForeignKey('User')
    code_archive = models.OneToOneField('CodeArchive')
    test_case = models.OneToOneField('TestCase')
    token = models.CharField()
    status = models.IntegerField()
    result = models.OneToOneField('BugExResult')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.token, self. test_case)

    @staticmethod
    def new():
        token = uuid.uuid4()
        return UserRequest(token=token, status=PENDING)

    @property
    def folder(self):
        return path.join(
            WORKING_DIR, self.user.id, self.token)


class CodeArchive(models.Model):
    EXTENSION_CHOICES = (('jar', 'Type of archive: jar'),
                         ('zip', 'Type of archive: zip'))
    name = models.CharField()
    extension = models.CharField(choices=EXTENSION_CHOICES) # This is called "type" in class diagram

    def __unicode__(self):
        return u'{0}'.format(self.name)


class TestCase(models.Model):
    name = models.CharField()

    def __unicode__(self):
        return u'{0}'.format(self.name)


class AnonymousUser(models.Model):
    registration_date = models.DateField()
    email_address = models.EmailField()

    def __unicode__(self):
        return '{0}'.format(self.email_address)

    def register(self):
        '''Create a registered user
        '''
        pass

    def update_email(self, new_email):
        #self.email_address = new_email
        pass

    def update_password(self):
        pass


class RegisteredUser(AnonymousUser):
    password = models.CharField() #size?

    def generate_password(self):
        pass


class Folder(models.Model):
    """The Folder model.

    The Folder model represents a single folder inside the code archive.
    """
    name = models.CharField(max_length=100,
        help_text='The name of this folder.'
    )
    code_archive = models.ForeignKey('CodeArchive',
        help_text='The code archive that this folder resides in.'
    )
    parent_folder = models.ForeignKey('self', null=True, blank=True,
        help_text='The parent folder of this folder, if it exists.'
    )

    def __unicode__(self):
        """Return a unicode representation for a Folder model object."""
        return '{0}'.format(self.name)


class ProjectFile(models.Model):
    """The ProjectFile model.

    The ProjectFile model provides many-to-one relationships
    to the CodeArchive model (one or more project files are included in
    one code archive) and to the Folder model (one or more project files
    are included in one folder).

    This is an abstract base class that will not be saved to the database.
    Its fields are inherited by two subclasses SourceFile and ClassFile.
    """
    code_archive = models.ForeignKey('CodeArchive',
        help_text='The code archive that this project file resides in.'
    )
    folder = models.ForeignKey('Folder',
        help_text='The folder that this project file resides in.'
    )

    class Meta:
        """Inner class providing metadata options to the ProjectFile model."""
        abstract = True


class SourceFile(ProjectFile):
    """The SourceFile model.

    The SourceFile model represents a Java source file with
    file extension `.java`.
    """
    name = models.CharField(
        max_length=100,
        validators=[validate_source_file_extension],
        help_text='The name of this source file.'
    )

    package = models.CharField(
        max_length=100,
        blank=True,
        help_text='The name of the package that this source file resides in.'
    )

    def __unicode__(self):
        """Return a unicode representation for a SourceFile model object."""
        return '{0}'.format(self.name)

class ClassFile(ProjectFile):
    """The ClassFile model.

    The ClassFile model represents a Java class file with
    file extension `.class`.
    """
    name = models.CharField(
        max_length=100,
        validators=[validate_class_file_extension],
        help_text='The name of this class file.'
    )

    def __unicode__(self):
        """Return a unicode representation for a ClassFile model object."""
        return '{0}'.format(self.name)


class Line(models.Model):
    """The Line model.

    The Line model represents a single line of source code that is taken
    from the SourceFile model.
    """
    source_file = models.ForeignKey('SourceFile',
        help_text='The source file that this line resides in.'
    )
    number = models.PositiveIntegerField(
        verbose_name='line number',
        help_text='The line number of this line in the source file.'
    )
    content = models.CharField(
        max_length=100,
        help_text='The code that is included in this line.'
    )
    definition = models.BooleanField(
        default=False,
        verbose_name='definition of model, method or class ?',
        help_text='Is this source code line a definition of a ' \
                  'model, method or class ?'
    )

    def __unicode__(self):
        """Return a unicode representation for a Line model object."""
        return '{0}: line {1}'.format(self.source_file.name, self.number)


class OutlineElement(models.Model):
    """The OutlineElement model.

    The OutlineElement model is an abstract base class that will
    not be saved to the database. Its fields are inherited by three
    subclasses MethodElement, FieldElement and ClassElement.
    """
    ACCESS_LEVELS = (
        ('PUB', 'public'),
        ('PRI', 'private'),
        ('PRO', 'protected'),
        ('PAC', 'package-private')
    )

    line = models.OneToOneField('Line',
        help_text='The line element associated with this outline element.'
    )
    class_element = models.ForeignKey('ClassElement', null=True, blank=True,
        help_text='The class element that this outline element resides in.'
    )
    access_level = models.CharField(max_length=3, choices=ACCESS_LEVELS,
        help_text='The access level modifier of this outline element.'
    )
    name = models.CharField(max_length=100,
        help_text='The name of this outline element.'
    )
    comment = models.TextField(blank=True,
        help_text='An optional comment associated with this outline element.'
    )

    class Meta:
        """Inner class providing metadata options to the OutlineElement model."""
        abstract = True


class MethodElement(OutlineElement):
    """The MethodElement model.

    The MethodElement model defines method definitions in Java source files.
    """
    arguments = models.CharField(max_length=200,
        help_text='The arguments and their types of this method.'
    )
    return_type = models.CharField(max_length=100,
        help_text='The type of the return value of this method.'
    )

    def __unicode__(self):
        """Return a unicode representation for a MethodElement model object."""
        return '{0}'.format(self.name)

    def save(self, *args, **kwargs):
        """Override save() method to prevent a MethodElement being saved
        without an associated ClassElement.

        This model's base class (OutlineElement) defines a ClassElement to be
        optional because a ClassElement does not necessarily have to reside in
        another ClassElement. This is not a valid behavior for a MethodElement
        since a Java method can only reside within a Java class. Thus,
        a ValidationError is raised if no ClassElement has been associated
        with this MethodElement.
        """
        if self.class_element is None:
            raise ValidationError('ClassElement may not be NULL!')
        else:
            super(MethodElement, self).save(*args, **kwargs)


class FieldElement(OutlineElement):
    """The FieldElement model.

    The FieldElement model defines variable definitions in Java source files.
    """
    field_type = models.CharField(max_length=100,
        help_text='The type of this variable.'
    )

    def __unicode__(self):
        """Return a unicode representation for a FieldElement model object."""
        return '{0}'.format(self.name)

    def save(self, *args, **kwargs):
        """Override save() method to prevent a FieldElement being saved
        without an associated ClassElement.

        This model's base class (OutlineElement) defines a ClassElement to be
        optional because a ClassElement does not necessarily have to reside in
        another ClassElement. This is not a valid behavior for a FieldElement
        since a Java field can only reside within a Java class. Thus,
        a ValidationError is raised if no ClassElement has been associated
        with this FieldElement.
        """
        if self.class_element is None:
            raise ValidationError('ClassElement may not be NULL!')
        else:
            super(FieldElement, self).save(*args, **kwargs)


class ClassElement(OutlineElement):
    """The ClassElement model.

    The ClassElement model defines class definitions in Java source files.
    """
    def __unicode__(self):
        """Return a unicode representation for a ClassElement model object."""
        return '{0}'.format(self.name)
