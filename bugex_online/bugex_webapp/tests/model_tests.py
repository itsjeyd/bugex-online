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

