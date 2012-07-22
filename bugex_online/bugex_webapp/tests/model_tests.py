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


class UserRequestTest(TestCase):
    """
    Tests for (public) methods + properties of the UserRequest model
    """
    fixtures = ['test_data.json']

    def setUp(self):
        self.user_request = UserRequest.objects.get(
            token='f99db44e-c841-444b-977b-ccc9baa11027')

    def test_result_url(self):
        """ Test the 'result_url' property of UserRequest """
        self.assertEqual(
            self.user_request.result_url,
            settings.APPLICATION_BASE_URL+
            '/result/f99db44e-c841-444b-977b-ccc9baa11027')

    def test_delete_url(self):
        """ Test the 'delete_url' property of UserRequest """
        self.assertEqual(
            self.user_request.delete_url,
            settings.APPLICATION_BASE_URL+
            '/delete/de608d71-2ab6-4776-957d-9d6c5ca11d03')

    def test_folder(self):
        """ Test the 'folder' property of UserRequest """
        self.assertEqual(
            self.user_request.folder,
            os.path.join(
                settings.MEDIA_ROOT,
                'user_2', 'f99db44e-c841-444b-977b-ccc9baa11027'))

    def test_relative_folder(self):
        """ Test the 'relative_folder' property of UserRequest """
        self.assertEqual(
            self.user_request.relative_folder,
            os.path.join('user_2', 'f99db44e-c841-444b-977b-ccc9baa11027'))

    def test_update_status(self):
        """ Tests the 'update_status method of User Request """
        old_status = self.user_request.status
        self.user_request.update_status(UserRequestStatus.PENDING)
        self.assertNotEqual(self.user_request.status, old_status)
        self.assertEqual(self.user_request.status, UserRequestStatus.PENDING)


class CodeArchiveTest(TestCase):
    """
    Tests for methods + properties of the CodeArchive model
    """
    fixtures = ['test_data.json']

    def setUp(self):
        self.code_archive = CodeArchive.objects.get(archive_format='JAR')

    def test_name(self):
        """ Test the 'name' property of CodeArchive """
        self.assertEqual(
            self.code_archive.name,
            'failing-program-0.0.2-SNAPSHOT-jar-with-dependencies.jar')

    def test_path(self):
        """
        Test the 'path' property of CodeArchive, which should return
        the absolute path of the physical archive file
        """
        self.assertEqual(
            self.code_archive.path,
            os.path.join(
                settings.MEDIA_ROOT,
                'user_2',
                'f99db44e-c841-444b-977b-ccc9baa11027',
                'failing-program-0.0.2-SNAPSHOT-jar-with-dependencies.jar'))

    def test_absolute_extracted_path(self):
        """
        Test the 'absolute_extracted_path' property of CodeArchive,
        which should return the absolute path of the root folder of
        the archive contents. We are calling this folder
        'tmp_extracted'.
        """
        self.assertEqual(
            self.code_archive.absolute_extracted_path,
            os.path.join(
                settings.MEDIA_ROOT,
                'user_2',
                'f99db44e-c841-444b-977b-ccc9baa11027',
                'failing-program-0.0.2-SNAPSHOT-jar-with-dependencies'))

