'''
Created on Jun 29, 2012

@author: Iliana Simova
'''

from django.core.mail import send_mail
from bugex_webapp import Notifications, UserRequestStatus
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
        status = user_request.status
        subject = Notifications.CONTENT[status][0]
        content = Notifications.HEADER_FOOTER %Notifications.CONTENT[status][1]
        
        if status == UserRequestStatus.FINISHED:
            content %(user_request.result_url, user_request.delete_url)
        
        try:
            self.send_notification(status, user_request.user.email, 
                                   subject, content)
        except Exception as e:
            # TODO log stuff
            pass
            
    def send_notification(self, status, user_email, subject, content):
        '''Send an email to the user.
        '''
        send_mail(subject, content, 'bugexonline@gmail.com', [user_email],
                  fail_silently=False)
        
        
        
