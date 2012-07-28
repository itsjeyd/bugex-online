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

from django.core.exceptions import ValidationError
from django.test import TestCase

from bugex_webapp.models import CodeArchive
from bugex_webapp.validators import validate_source_file_extension
from bugex_webapp.validators import validate_class_file_extension
from bugex_webapp.validators import validate_archive_file_extension
from bugex_webapp.validators import validate_archive_copyright
from bugex_webapp.validators import validate_test_case_name

class ValidatorTestCase(TestCase):
    """The test case for the custom validators in bugex_webapp/validators.py"""

    fixtures = ('data_with_different_archive_extensions.json',)

    def setUp(self):
        """Set up Java source and class file names with different extensions."""
        self.java_source_file_names = (
            'JavaSourceFile.java',
            'JavaSourceFile.JAVA',
            'JavaSourceFile.JaVa',
            'JavaSourceFile.jAvA',
        )
        self.java_class_file_names = (
            'JavaClassFile.class',
            'JavaClassFile.CLASS',
            'JavaClassFile.ClAsS',
            'JavaClassFile.cLaSs'
        )
        self.valid_test_case_names = (
            'mypackage.TestClass#testMethod',
            'de.mypackage.TestClass#testMethod',
            'de.unisb.cs.st.BugExMock#getRandomFactType',
            'a.b.c.d.e.f.g.Ab#a234A',
            '_mypackage.$Test527Class#__testMethod',
            'de.$$$mypackage._$_TestClass#testMethod123'
        )
        self.invalid_test_case_names = (
            'Mypackage.TestClass#testMethod',
            'mypackage.testClass#testMethod',
            'mypackage.TestClass#TestMethod',
            'mypackage.TestClass',
            'de.mypackage',
            '#testMethod',
            '123mypackage.TestClass#testMethod',
            'mypackage.123TestClass#testMethod',
            'mypackage.TestClass#123testMethod'
        )

    def test_source_file_extension(self):
        """Verify that the Java source file extension validator works correctly."""
        for java_source_file in self.java_source_file_names:
            self.assertIsNone(validate_source_file_extension(java_source_file))

        with self.assertRaises(ValidationError):

            for java_class_file in self.java_class_file_names:
                validate_source_file_extension(java_class_file)

    def test_class_file_extension(self):
        """Verify that the Java class file extension validator works correctly."""
        for java_class_file in self.java_class_file_names:
            self.assertIsNone(validate_class_file_extension(java_class_file))

        with self.assertRaises(ValidationError):

            for java_source_file in self.java_source_file_names:
                validate_class_file_extension(java_source_file)

    def test_archive_file_extension(self):
        """Verify that the code archive file extension validator works correctly."""
        for code_archive in CodeArchive.objects.all():
            self.assertIsNone(
                validate_archive_file_extension(code_archive.archive_file)
            )

    def test_archive_copyright(self):
        """Verify that the archive copyright validator works correctly."""
        self.assertIsNone(validate_archive_copyright(True))
        self.assertRaises(ValidationError, validate_archive_copyright, False)

    def test_test_case_name(self):
        """Verify that the test case name validator works correctly."""
        for test_case_name in self.valid_test_case_names:
            self.assertIsNone(validate_test_case_name(test_case_name))

        with self.assertRaises(ValidationError):

            for test_case_name in self.invalid_test_case_names:
                validate_test_case_name(test_case_name)