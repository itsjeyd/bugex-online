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
# setup logging facilities
import logging

logging.basicConfig()

# defining Enums
class Enum(object):
    """ Parent class for all constant enums """

    @classmethod
    def const_name(cls, const_value):
        for const, value in vars(cls).items():
            if value == const_value:
                return const


class UserRequestStatus(Enum):
    """ Collection of possible statuses for UserRequests

    The possible values are:
    PENDING:    User input data has been recieved, the archive is being
                validated.
    VALIDATING: The user archive is being validated.
    VALID:      The user archive has been processed and is valid.
    INVALID:    The user archive has been processed and is invalid.
    PROCESSING: BugEx is running.
    FAILED:     BugEx failed unexpectedly.
    FINISHED:   BugEx terminated sucessfully.
    DELETED:    The user deleted the results.

    """

    PENDING = 1
    VALIDATING = 2
    VALID = 3
    INVALID = 4
    PROCESSING = 5
    FAILED = 6
    FINISHED = 7
    DELETED = 8


class XMLNode(Enum):
    """ Collection of possible node types in XML output of BugEx """

    FACT = './/fact'
    CLASS = 'className'
    LINE = 'lineNumber'
    METHOD = 'methodName'
    EXPL = 'explanation'
    TYPE = 'factType'


class Notifications(object):
    '''Messages for user email notification mapped to UserRequest statuses
    '''
    HEADER_FOOTER = 'Dear BugEx Online user,\n\n{0}\n\nBest,\nBugEx Online Team'
    CONTENT = {
        'PENDING': {
            'subject': 'Input files successfully received',
            'content': 'The input you\'ve submitted to BugEx Online has been ' +
                       'successfully uploaded and is being processed.'
        },
        'INVALID': {
            'subject': 'Your request could not be processed',
            'content': 'Unfortunately your request could not be processed.'
        },
        'FAILED': {
            'subject': 'Your request could not be processed',
            'content': 'Unfortunately your request could not be processed.'
        },
        'FINISHED': {
            'subject': 'Your BugEx result is available',
            'content': 'BugEx has finished processing your request.\n' +
                       'You can access the result here: {0}\n' +
                       'You can delete the result here: {1}'
        },
        'DELETED': {
            'subject': 'Your BugEx result has been deleted',
            'content': 'You have successfully deleted your BugEx result files.'
        },
        'CHANGED_EMAIL_ADDRESS': {
            'subject': 'Your email address has been changed',
            'content': 'You have successfully changed your email address.\n' +
                       'Your new email address is: {0}'
        }
    }