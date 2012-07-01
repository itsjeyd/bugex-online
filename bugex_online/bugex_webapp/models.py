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
import re
import uuid
from xml.etree.ElementTree import fromstring
from zipfile import ZipFile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from bugex_webapp import *
from bugex_webapp.validators import validate_source_file_extension
from bugex_webapp.validators import validate_class_file_extension
from bugex_webapp.validators import validate_archive_format
from bugex_webapp.core_modules.core_config import WORKING_DIR


class UserRequest(models.Model):
    """The UserRequest model.

    The UserRequest model represents a single request to be sent to BugEx.
    """
    user = models.ForeignKey(User)
    code_archive = models.OneToOneField('CodeArchive')
    test_case = models.OneToOneField('TestCase')
    token = models.CharField(max_length=100)
    status = models.PositiveIntegerField()
    result = models.OneToOneField('BugExResult', blank=True, null=True)

    def __unicode__(self):
        """Return a unicode representation for a UserRequest model object."""
        return u'{0}: {1}'.format(self.token, self.test_case)

    @staticmethod
    def new(user, test_case_name, code_archive_name):
        token = uuid.uuid4()
        test_case = TestCase.objects.create(name=test_case_name)
        code_archive_format = os.path.splitext(
            code_archive_name)[1][1:].strip().upper()
        code_archive = CodeArchive.objects.create(
                name=code_archive_name, archive_format=code_archive_format)
        return UserRequest(user=user, code_archive=code_archive,
                test_case=test_case, token=token, status=PENDING)

    @property
    def folder(self):
        return os.path.join(
            WORKING_DIR, 'user_%d' % self.user.id, self.token)

    def _build_path(self, *sub_folders):
        return os.path.join(self.folder, *sub_folders)

    def parse_archive(self):
        path = self._build_path(self.code_archive.name)
        path_extracted = self._build_path('tmp_extracted')
        try:
            archive = ZipFile(path, 'r')
            archive.extractall(path_extracted)
            archive.close()
        except:
            self.update_status(INVALID)
        else:
            self.code_archive.traverse(path_extracted)

    def update_status(self, new_status):
        self.status = new_status
        self.save()
        print 'Status of {0} changed to: {1}'.format(self.token, self.status)
        #call notifier


class CodeArchive(models.Model):
    """The CodeArchive model.

    The CodeArchive model represents a single code archive uploaded by the user.
    """
    EXTENSIONS = (
        ('JAR', 'jar'),
        ('ZIP', 'zip')
    )

    name = models.CharField(
        max_length=100,
        validators=[validate_archive_format],
        help_text='The name of this code archive.'
    )
    archive_format = models.CharField(
        max_length=3,
        choices=EXTENSIONS,
        validators=[validate_archive_format],
        help_text='The format of this archive (either *.jar or *.zip)'
    )

    def __unicode__(self):
        """Return a unicode representation for a CodeArchive model object."""
        return u'{0}'.format(self.name)

    def traverse(self, path):
        pass


class TestCase(models.Model):
    """The TestCase model.

    The TestCase model represents a single failing test case to be analyzed
    by BugEx.
    """
    name = models.CharField(max_length=100,
        help_text='The name of this test case.'
    )

    def __unicode__(self):
        """Return a unicode representation for a TestCase model object."""
        return u'{0}'.format(self.name)


class BugExResult(models.Model):
    """The BugExResult model.

    The BugExResult model represents a single result created by BugEx for
    a specific user request. A result is made up of one ore more facts.
    """
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date of creation',
        help_text='The date when this BugEx result was created.'
    )

    def __unicode__(self):
        """Return a unicode representation for a BugExResult model object."""
        return '{0}'.format(self.date)

    @staticmethod
    def new(xml_string):
        '''Creates a new instance of BugExResult.

        xml_string -- a string containing the xml output of BugEx
        '''
        try:
            facts = BugExResult._parse_xml(xml_string)
        except Exception:
            #re-raise any exceptions raised during xml parsing
            raise
        else:
            #instantiate a BugExResult and save all corresponding Facts
            #setting the ForeignKey field of each Fact properly
            be_res = BugExResult()
            be_res.save()
            for f in facts:
                f.bugex_result = be_res
                f.save()

    @staticmethod
    def _parse_xml(xml_string):
        '''Parse the xml string and if parse is successful create Facts
        '''
        facts = []

        try:
            #parse xml string and extract fact nodes
            facts_xml = fromstring(xml_string).findall(FACT_NODE)

            #create a Fact for each fact node in the xml file only if all
            #required information about the fact was found in the xml tree
            for f in facts_xml:
                try:
                    my_fact = Fact(
                           class_name=f.find(CLASS_NODE).text.strip(),
                           method_name=f.find(METHOD_NODE).text.strip(),
                           line_number=int(f.find(LINE_NODE).text.strip()),
                           explanation=f.find(EXPL_NODE).text.strip(),
                           fact_type=f.find(TYPE_NODE).text.strip())
                except Exception:
                    #nodes are missing
                    raise
                else:
                    facts.append(my_fact)
        except Exception:
            #xml string is empty or not valid
            raise
        else:
            return facts

    class Meta:
        """Inner class providing metadata options to the OutlineElement model."""
        verbose_name = 'BugEx result'


class Fact(models.Model):
    """The Fact model.

    The Fact model represents a single fact consisting of location, explanation
    and type of a specific failure.
    """
    FACT_TYPES = [
        ('A', 'TYPE_A'),
        ('B', 'TYPE_B'),
        ('C', 'TYPE_C'),
        # ...
    ]

    bugex_result = models.ForeignKey('BugExResult',
        help_text='The BugExResult instance associated with this fact.'
    )
    class_name = models.CharField(max_length=100,
        help_text='The class name associated with this fact.'
    )
    method_name = models.CharField(max_length=100,
        help_text='The method name associated with this fact.'
    )
    line_number = models.PositiveIntegerField(
        help_text='The line number associated with this fact.'
    )
    explanation = models.TextField(
        help_text='A detailed summary describing what the '\
                  'failure associated to this fact is about.'
    )
    fact_type = models.CharField(max_length=1,
        choices=FACT_TYPES,
        help_text='The type of this fact.'
    )

    def __unicode__(self):
        """Return a unicode representation for a Fact model object."""
        return 'type {0}, class {1}, line {2}'.format(
            self.fact_type, self.class_name, self.line_number
        )


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
        blank=True,
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

    @staticmethod
    def new(code_archive, name, path, folder=None):
        """
        Creates a new SourceFile object, parses its lines and stores everything
        to database.

        Raises an IOError, if the file can not be opened.
        """
        source_file = SourceFile(code_archive=code_archive, name=name)

        if folder:
            source_file.folder = folder

        for number, line in enumerate(open(path).readlines(), 1):
            Line.objects.create(
                code_archive=source_file.code_archive,
                number=number,
                content=line.strip())
            if line.startswith('package'):
                source_file.package = re.search('package +(.+);', line).group(1)

        source_file.save()


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
    definition = models.NullBooleanField(
        blank=True,
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
