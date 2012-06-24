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

from django.db import models

from bugex_webapp.validators import validate_source_file_extension, \
    validate_class_file_extension

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
        return '{0}: line {1}'.format(self.source_file, self.number)