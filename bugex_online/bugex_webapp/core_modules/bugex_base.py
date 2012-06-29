'''
Created on 19.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@googlemail.com>
'''
# user request
from bugex_files import BugExFile
import core_config

# django
from bugex_webapp import PENDING

import uuid

class UserRequest(object):
    """
    The UserRequest is the central object linked to all important information.
    
    This is a mock implementation of the UserRequest, containing all information
    needed for the monitoring system.
    
    """
    def __init__(self):
        # create an unique token and set status to pending
        self.token = str(uuid.uuid4())
        self.status = PENDING

    @property
    def folder(self):
        """
        Returns the working  path on the disk for this request.
        
        """
        #return '/tmp/{0}/'.format(self.token)
        return "{0}/{1}/".format(core_config.WORKING_DIR,self.token)
        
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status
        # notify notifier..
        print 'Status of {0} changed to: {1}'.format(self.token, self._status)
        pass
