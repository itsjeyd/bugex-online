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
    
    
    
    
    


