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

from django.contrib.auth.models import User
from django.test import TestCase

from bugex_webapp import PENDING
from bugex_webapp.core_modules.core_config import WORKING_DIR
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
        self.assertEqual(ur.status, PENDING)

    def test_folder(self):
        ur = UserRequest.objects.get(id=1)
        path = os.path.join(WORKING_DIR, 'user_1', ur.token)
        self.assertEqual(ur.folder, path)
