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

class Enum(object):
    """ Parent class for all constant enums """

    @classmethod
    def const_name(cls, const_value):
        for const, value in vars(cls).items():
            if value == const_value:
                return const


class UserRequestStatus(Enum):
    """ Collection of possible statuses for UserRequests """

    PENDING = 1
    VALID = 2
    INVALID = 3
    PROCESSING = 4
    FAILED = 5
    FINISHED = 6
    DELETED = 7


class XMLNode(Enum):
    """ Collection of possible node types in XML output of BugEx """

    FACT = './/fact'
    CLASS = 'className'
    LINE = 'lineNumber'
    METHOD = 'methodName'
    EXPL = 'explanation'
    TYPE = 'factType'
