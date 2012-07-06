'''
Created on Jun 29, 2012

@author: Iliana Simova
'''

from django.core.mail import send_mail
from bugex_webapp import *
from bugex_webapp.models import UserRequest

class Notifier(object):
    
    def notify(self, a_user_req):
        pass
    
    def notify_user(self):
        pass


class EmailNotifier(Notifier):
    '''BugEx Online users notification via email.
    
    BugEx Online users will be notified via email when:
    - their input to the system has been successfully received;
    - BugEx has successfully finished processing their request;
    - BugEx has failed to process their request due to internal error;
    - BugEx has failed to process their request due to invalid input;
    - they have successfully deleted their BugEx result files;
    '''
    
    def notify_user(self, user_request):
        '''User is notified in case of a change in the UserRequest status
        
        UserRequest instance is providing all data needed to notify the user 
        (user email, UserRequest status)
        
        user_request -- a UserRequest instance
        '''
        try:
            self.send_notification(user_request.status,
                               user_request.user.email)
        except:
            #most probably the user email does not exist/is invalid;
            #set the status of the UserRequest to INVALID
            user_request.update_status(INVALID)
            
    def send_notification(self, ur_status, user_email):
        '''Send an email to the user.
        '''
        subject = NOTIFICATIONS[ur_status][0]
        content = NOTIFY_HEADER_FOOTER %NOTIFICATIONS[ur_status][1]
        
        send_mail(subject, content, 'bugexonline@gmail.com', [user_email],
                  fail_silently=False)
        
        
        
