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

import re
import uuid
import os
import logging
import shutil
import threading
from xml.etree.ElementTree import fromstring
from zipfile import ZipFile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from bugex_webapp import UserRequestStatus, XMLNode
from bugex_webapp.validators import validate_source_file_extension
from bugex_webapp.validators import validate_class_file_extension
from bugex_webapp.validators import validate_archive_file_extension
from bugex_webapp.validators import validate_test_case_name
from bugex_webapp.core_modules.bugex_monitor import BugExMonitor
from bugex_webapp.core_modules.bugex_timer import UserRequestThread

class UserRequest(models.Model):
    """The UserRequest model.

    The UserRequest model represents a single request to be sent to BugEx.
    """
    user = models.ForeignKey(User)
    test_case = models.OneToOneField('TestCase')
    token = models.CharField(max_length=36)
    status = models.PositiveIntegerField()
    result = models.OneToOneField('BugExResult', blank=True, null=True)

    def __unicode__(self):
        """Return a unicode representation for a UserRequest model object."""
        return u'{0}: {1}'.format(self.token, self.test_case)

    @staticmethod
    def new(user, test_case_name, archive_file):
        """
        Creates a new UserRequest object, saves it to database and returns a
        reference to it.

        Also triggers archive parsing and runs BugEx.

        Arguments:

        user            -- the user associated to the request
        test_case_name  -- the fully qulified nam eof the test case
        archive_file    -- the uploaded file (user archive)

        """
        # logging
        log = logging.getLogger(__name__)
        log.setLevel('DEBUG')

        # create unique token for request
        token = str(uuid.uuid4())
        log.info("Created token for incoming UserReqest: %s", token)
        log.debug("Creating test case...")

        # create test case object
        test_case = TestCase.objects.create(name=test_case_name)

        # create user request object
        user_request = UserRequest.objects.create(
            user=user,
            test_case=test_case,
            token=token,
            status=UserRequestStatus.PENDING
        )

        log.debug("Creating code archive..")

        # create code archive
        code_archive = CodeArchive()
        code_archive.user_request = user_request
        # save file to disk
        code_archive.archive_file.save(
            name=archive_file.name,
            content=archive_file
        )
        # extract file type
        archive_file_ext = os.path.splitext(archive_file.name)[1][1:].strip()
        code_archive.archive_format = archive_file_ext.upper()
        code_archive.save()

        # save user request
        user_request.save()

        # update status to PENDING
        user_request.update_status(UserRequestStatus.PENDING)

        # Now the user input has been validated, and thus
        # the http request should respond.
        # Therefore, further action will be carried out asynchronously
        log.debug("Starting threaded execution..")
        
        thread = UserRequestThread(user_request)
        thread.start()

        """
        log.debug("Parsing archive..")

        # try to parse archive
        try:
            user_request._parse_archive()
        except Exception as e:
            log.info("Parsing failed: %s", e)
        else:
            log.debug("Running BugEx..")
            # run BugEx
            user_request._run_bugex()
        """

        log.debug("Returning to view..")
        
        # return reference to view
        return user_request


    def _async_processing(self, user_request):
        """
        This method is to be called by a Thread.

        It starts parsing the archive asynchronously, so that the HTTP request
        can terminate.

        """
        log = logging.getLogger(__name__)
        log.debug("Parsing archive..")

        # try to parse archive
        try:
            user_request._parse_archive()
        except Exception as e:
            log.info("Parsing failed: %s", e)
        else:
            log.debug("Running BugEx..")
            # run BugEx
            user_request._run_bugex()


    @property
    def folder(self):
        """
        Returns the absolute root folder of this request.
        """
        return os.path.join(
            settings.MEDIA_ROOT, self.relative_folder
        )

    @property
    def relative_folder(self):
        """
        Returns the relative root folder of this request.

        (relative to MEDIA_ROOT)
        """
        return os.path.join(
            'user_{0}'.format(self.user.id), self.token
        )

    @property
    def code_archive_path(self):
        """
        Returns the absolute path to the code archive.
        """
        return os.path.join(
            settings.MEDIA_ROOT, self.codearchive.archive_file.name
        )

    def _build_path(self, *sub_folders):
        return os.path.join(self.folder, *sub_folders)

    def _parse_archive(self):
        """
        Traverses the archive and parses its files.
        Stores the folder structure, relevant files and file contents in the
        database.

        This step is important to display the source code later on.
        """
        # VALIDATION phase starts now
        self.update_status(UserRequestStatus.VALIDATING)

        # extract user archive
        path_extracted = self.codearchive.absolute_extracted_path #_build_path('tmp_extracted')
        try:
            archive = ZipFile(self.code_archive_path, 'r')
            archive.extractall(path_extracted)
            archive.close()
        except:
            # oops, no zip?
            self.update_status(UserRequestStatus.INVALID)
            # raise exception for handling somewhere else
            raise
        else:
            # trigger archive traversal
            self.codearchive.traverse()

            # archive seems to be VALID!
            self.update_status(UserRequestStatus.VALID)
            
            # delete temporary folder again
            shutil.rmtree(path_extracted)

    
    def _run_bugex(self):
        """
        Creates and starts a BugEx Instance by notifying the BugExMonitor.

        """
        # PROCESSING phase stars now
        self.update_status(UserRequestStatus.PROCESSING)

        # notify monitor
        bugex_mon = BugExMonitor.Instance()
        bugex_mon.new_request(self)


    def update_status(self, new_status):
        """
        Updates the status of this user request and saves itself to the
        database.

        Also triggers notification of the user.

        Arguments:
        new_status  -- the new status of the request (see UserRequestStatus)
        """
        self.status = new_status
        self.save()
        print 'Status of {0} changed to: {1}'.format(
            self.token, UserRequestStatus.const_name(self.status))

        # TODO call notifier


def archive_file_path(instance, filename):
    """
    Dynamically generate the upload path for the FileField archive_file in
    a single CodeArchive instance.

    All code archives will be saved to MEDIA_ROOT/user_id/token/*.{zip|jar}

    Arguments:
    instance -- the respective CodeArchive instance
    filename -- the file name of the archive file to be uploaded

    """
    return os.path.join(instance.user_request.relative_folder, filename)


class CodeArchive(models.Model):
    """The CodeArchive model.

    The CodeArchive model represents a single code archive uploaded by the user.
    """
    EXTENSIONS = (
        ('JAR', 'jar'),
        ('ZIP', 'zip')
    )

    user_request = models.OneToOneField('UserRequest',
        help_text='The UserRequest instance associated with this CodeArchive'
    )
    archive_file = models.FileField(
        upload_to=archive_file_path,
        validators=[validate_archive_file_extension],
        help_text='The code archive file that should be uploaded.'
    )
    archive_format = models.CharField(
        max_length=3,
        choices=EXTENSIONS,
        help_text='The format of this archive (either *.jar or *.zip)'
    )

    def __unicode__(self):
        """Return a unicode representation for a CodeArchive model object."""
        return u'{0}'.format(self.archive_file.name)


    @property
    def absolute_extracted_path(self):
        """
        Returns the absolute path to the extracted archive.

        """
        return self.user_request._build_path('tmp_extracted')

    def traverse(self):
        # ok, lets create the root folder
        root_folder = Folder.objects.create(
                # the name of the root folder does not really matter..
                name = 'tmp_extracted',
                parent_folder = None,
                code_archive = self)

        # easy enough, now let it traverse itself
        root_folder.traverse()


class TestCase(models.Model):
    """The TestCase model.

    The TestCase model represents a single failing test case to be analyzed
    by BugEx.
    """
    name = models.CharField(max_length=100,
        validators=[validate_test_case_name],
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
            be_res = BugExResult.objects.create()
            #be_res.save()
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
            facts_xml = fromstring(xml_string).findall(XMLNode.FACT)

            #create a Fact for each fact node in the xml file only if all
            #required information about the fact was found in the xml tree
            for f in facts_xml:
                try:
                    my_fact = Fact(
                        class_name=f.find(XMLNode.CLASS).text.strip(),
                        method_name=f.find(XMLNode.METHOD).text.strip(),
                        line_number=int(f.find(XMLNode.LINE).text.strip()),
                        explanation=f.find(XMLNode.EXPL).text.strip(),
                        fact_type=f.find(XMLNode.TYPE).text.strip())
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

    @property
    def is_root_folder(self):
        if self.parent_folder is None:
            return True
        return False
    
    @property
    def absolute_path(self):
        if self.is_root_folder:
            # just use absolute extracted path
            return self.code_archive.absolute_extracted_path
        else:
            # recursively build path from parent
            return os.path.join(
                self.parent_folder.absolute_path,
                self.name)


    def _get_path_elements(self, my_path):
        '''Returns the current and parent folder names of a specified path 
        my_path -- a path string
        '''
        elements = os.path.split(os.path.abspath(my_path))
        this_f = elements[1]
        parent_f = os.path.split(os.path.abspath(elements[0]))[1]
        return parent_f, this_f


    def traverse(self):
        #print 'in Folder.traverse(): name: {0}, path: {1}'.format(self.name,self.absolute_path)
        for f in os.listdir(self.absolute_path):
            f_path = os.path.join(self.absolute_path, f)
            #if f_path points to a class or java file, create it
            if os.path.isfile(f_path):
                ext = os.path.splitext(f)[1][1:].strip()
                if ext == 'java':
                    try:
                        SourceFile.new(code_archive=self.code_archive, name=f,
                        folder=self, path=f_path)
                    except Exception as e:
                        print e
                        #if something goes wring during SourceFile creation,
                        #change UserRequest status to INVALID
                elif ext == 'class':
                    ClassFile.objects.create(code_archive=self.code_archive,
                        folder=self, name=f)
            else:
                #current file is a folder, continue traversing
                child = Folder.objects.create(
                            name = f,
                            code_archive = self.code_archive,
                            parent_folder = self)
                child.traverse()


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
        null=True,
        help_text='The name of the package that this source file resides in.'
    )

    class_element = models.OneToOneField('ClassElement',
        blank=True,
        null=True,
        help_text='The class element associated with this source file.'
    )

    @staticmethod
    def new(code_archive, name, path, folder):
        """
        Creates a new SourceFile object, parses its lines and stores everything
        to database.

        Raises an IOError, if the file can not be opened.
        """
        source_file = SourceFile.objects.create(
                code_archive=code_archive,
                name=name,
                folder=folder)

        print 'Parsing {0}..'.format(path)

        # read and store lines and extract package name
        for number, line in enumerate(open(path).readlines(), 1):
            #print 'line: {0}'.format(line)
            Line.objects.create(
                source_file=source_file,
                number=number,
                content=line.strip())
            if line.startswith('package'):
                #print 'package line: {0}'.format(line)
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
