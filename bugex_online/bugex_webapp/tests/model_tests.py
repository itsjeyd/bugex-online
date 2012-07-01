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

from django.contrib.auth.models import User
from django.test import TestCase

from bugex_webapp import PENDING
from bugex_webapp.models import UserRequest


class UserRequestConstructorTest(TestCase):
    """ Tests for the UserRequest model """

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
