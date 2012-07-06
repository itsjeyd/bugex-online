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

PENDING = 1
VALID = 2
INVALID = 3
PROCESSING = 4
FAILED = 5
FINISHED = 6
DELETED = 7

#BugEx result file xml node names
FACT_NODE = './/fact'
CLASS_NODE = 'className'
LINE_NODE = 'lineNumber'
METHOD_NODE = 'methodName'
EXPL_NODE = 'explanation'
TYPE_NODE = 'factType'

#messages for user email notification, mapped to different UserRequest statuses
NOTIFY_HEADER_FOOTER = 'Dear BugEx Online user,\n\n%s\n\nBest,\nBugEx Online Team'
NOTIFICATIONS = {
                 1:('Input files successfully received',
                    'The input you\'ve submitted to BugEx Online has been ' +
                    'successfully uploaded and is being processed.'), 
                 3:('Your request could not be processed',
                     'Unfortunately your request could not be processed.'),
                 5:('Your request could not be processed',
                     'Unfortunately your request could not be processed.'),
                 6:('Your BugEx result is available',
                    'BugEx has finished processing your request. You can ' + 
                    'access the result here: %s.'),
                 7:('Your BugEx result has been deleted',
                    'You have successfully deleted your BugEx result files.')
                 }
