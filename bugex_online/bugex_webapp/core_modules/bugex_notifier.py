'''
Created on Jun 29, 2012

@author: Iliana Simova
'''

from django.core.mail import send_mail
from bugex_webapp import Notifications, UserRequestStatus
import logging

class Notifier(object):
    
    def notify(self, a_user_req):
        pass
    
    def notify_user(self):
        pass


class EmailNotifier(Notifier):
    '''BugEx Online users notification via email.
    
    BugEx Online users will be notified via email when:
    - their input to the system has been successfully received (PENDING);
    - BugEx has successfully finished processing their request (FINISHED);
    - BugEx has failed to process their request due to internal error (FAILED);
    - BugEx has failed to process their request due to invalid input (INVALID);
    - they have successfully deleted their BugEx result files (DELETED);
    '''

    def __init__(self):
        self.__monitor_jobs = list()

        # logging
        self.__log = logging.getLogger("EmailNotifier")
        self.__log.info('EmailNotifier created.')
    
    def notify_user(self, user_request):
        '''User is notified in case of a change in the UserRequest status
        
        UserRequest instance is providing all data needed to notify the user 
        (user email, UserRequest status)
        
        user_request -- a UserRequest instance
        '''
        from bugex_webapp.models import UserRequest

        status = UserRequestStatus.const_name(user_request.status)
        
        if status not in ('VALID', 'PROCESSING', 'VALIDATING'):
            subject, content = self._get_content(user_request, status)
            try:
                send_mail(subject, content, 'bugexonline@gmail.com', 
                          [user_request.user.email], fail_silently=False)
            except Exception as e:
                self.__log.info("Email notification failed: %s", e)
                
    def _get_content(self, user_request, status):
        subject = Notifications.CONTENT[status]['subject']
        content = Notifications.HEADER_FOOTER.format(
            Notifications.CONTENT[status]['content']
        )
            
        if status == 'FINISHED':
            #include corresponding urls in the email content
            content = content.format(
                user_request.result_url,
                user_request.delete_url
            )
        
        return subject, content  

