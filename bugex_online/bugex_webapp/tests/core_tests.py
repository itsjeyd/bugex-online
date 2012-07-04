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
import shutil
import logging
import time

from django.contrib.auth.models import User
from django.test import TestCase

from bugex_webapp import UserRequestStatus
from bugex_webapp.core_modules.core_config import WORKING_DIR
from bugex_webapp.core_modules.bugex_monitor import BugExMonitor
from bugex_webapp.core_modules.bugex_decorators import Singleton

from bugex_webapp.models import UserRequest, BugExResult


class BugExMonitoringTest(TestCase):
    """ Test for the Monitoring Function of BugExOnline
    """
    
    test_case = 'de.mypackage.TestMyClass#testGetMin'
    code_archive = 'failing-program-0.0.1-SNAPSHOT-jar-with-dependencies.jar'
    code_archive_location = '/home/freddy/{0}'.format(code_archive)
    token = '82230841-bcbe-451c-8b3e-e1365ad7f257'
    ureq = None
    
    def setUp(self):
        # setup loggin
        logging.basicConfig() 
        
        # create working directory
        print 'Setting up working directory at \'{0}\'..'.format(WORKING_DIR)
        if not os.path.exists(WORKING_DIR):
            print 'Creating working directory..'
            os.makedirs(WORKING_DIR)
        else:
            print 'Working directory already exists.'
        
        # create fake user
        user = User.objects.create(email='user@example.com')
        
        # create fake user request
        ur = UserRequest.new(user, self.test_case, self.code_archive)
        ur.token = '82230841-bcbe-451c-8b3e-e1365ad7f257'
        ur.save()
        
        self.ureq = ur
        
        # create user folder
        print 'Setting up user directory at \'{0}\'..'.format(ur.folder)
        if not os.path.exists(WORKING_DIR):
            print 'Creating user directory at \'{0}\'..'.format(ur.folder)
            os.makedirs(ur.folder)
        else:
            print 'User directory already exists.'
            
        # copy code archive to destination
        print 'Copying user archive from \'{0}\' to user directory..'.format(
            self.code_archive_location)
        
        shutil.copy(self.code_archive_location, ur.folder)
        

    def test_new(self):
        self.ureq.update_status(1)
        
        bug_mon = BugExMonitor.Instance()
        bug_mon.new_request(self.ureq)
        
        time.sleep(20)
        
        self.assertEqual(self.ureq.status, UserRequestStatus.FINISHED)
