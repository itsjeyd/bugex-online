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


