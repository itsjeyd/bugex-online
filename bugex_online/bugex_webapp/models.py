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


class UserRequest(models.Model):
    user = models.ForeignKey('User')
    code_archive = models.OneToOneField('CodeArchive')
    test_case = models.OneToOneField('TestCase')
    token = models.CharField()
    request_folder = models.CharField()
    status = models.IntegerField()
    result = models.OneToOneField('BugExResult')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.token, self. test_case)


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
