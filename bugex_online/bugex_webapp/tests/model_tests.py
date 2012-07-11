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

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from bugex_webapp import UserRequestStatus
from bugex_webapp.models import CodeArchive
from bugex_webapp.models import UserRequest


class UserRequestConstructorTest(TestCase):
    """ Tests for the static constructor of the UserRequest model
    (UserRequest.new)
    """

    test_case = 'FooTest.testFoo'
    code_archive = 'archive.jar'

    def setUp(self):
        user = User.objects.create(email='user@example.com')
        ur = UserRequest.new(user, self.test_case, self.code_archive)
        ur.save()

    def test_token(self):
        ur = UserRequest.objects.get(id=1)
        self.assertEqual(len(str(ur.token)), 36)

    def test_test_case(self):
        ur = UserRequest.objects.get(id=1)
        self.assertEqual(ur.test_case.name, 'FooTest.testFoo')

    def test_code_archive(self):
        ur = UserRequest.objects.get(id=1)
        self.assertEqual(ur.code_archive.name, 'archive.jar')

    def test_code_archive_format(self):
        ur = UserRequest.objects.get(id=1)
        self.assertEqual(ur.code_archive.archive_format, 'JAR')

    def test_status(self):
        ur = UserRequest.objects.get(id=1)
        self.assertEqual(ur.status, UserRequestStatus.PENDING)

    def test_folder(self):
        ur = UserRequest.objects.get(id=1)
        path = os.path.join(settings.MEDIA_ROOT, 'user_1', ur.token)
        self.assertEqual(ur.folder, path)


class UserRequestUpdateStatusTest(TestCase):
    """  """
    test_case = 'FooTest.testFoo'
    code_archive = 'archive.jar'

    def setUp(self):
        user = User.objects.create(email='user@example.com')
        ur = UserRequest.new(user, self.test_case, self.code_archive)
        ur.save()

    def test_update_status(self):
        ur = UserRequest.objects.get(id=1)
        old_status = ur.status
        ur.update_status(UserRequestStatus.VALID)
        self.assertNotEqual(old_status, ur.status)
        self.assertEqual(UserRequestStatus.VALID, ur.status)


class CodeArchiveTest(TestCase):
    """
    Tests for methods + properties of the CodeArchive model
    """
    fixtures = ['test_data.json']

    def test_name(self):
        """ Test the 'name' property of CodeArchive """
        code_archive = CodeArchive.objects.get(archive_format='JAR')
        self.assertEqual(
            code_archive.name,
            'failing-program-0.0.2-SNAPSHOT-jar-with-dependencies.jar')

    def test_path(self):
        """
        Test the 'path' property of CodeArchive, which should return
        the absolute path of the physical archive file
        """
        code_archive = CodeArchive.objects.get(archive_format='JAR')
        self.assertTrue(code_archive.path.endswith(
            'uploads/user_2/f99db44e-c841-444b-977b-ccc9baa11027/' \
            'failing-program-0.0.2-SNAPSHOT-jar-with-dependencies.jar'))

    def test_absolute_extracted_path(self):
        """
        Test the 'absolute_extracted_path' property of CodeArchive,
        which should return the absolute path of the root folder of
        the archive contents. We are calling this folder
        'tmp_extracted'.
        """
        code_archive = CodeArchive.objects.get(archive_format='JAR')
        self.assertTrue(code_archive.absolute_extracted_path.endswith(
            'uploads/user_2/f99db44e-c841-444b-977b-ccc9baa11027/' \
            'tmp_extracted'))

