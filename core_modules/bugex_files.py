'''
Created on 21.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@dfki.de>
'''
import logging

class BugExFile(object):
    """
    A (physical) File representation in the BugEx System.
    
    Has a path and type. Provides methods for checking file existence and
    reading file contents.
    
    """
    def __init__(self, file_path, file_type):
        self.path = file_path
        self.type = file_type
    
    def exists(self):
        try:
            with open(self.path, 'r') as f:
                f.close()
            return True
        except IOError as e:
            logging.log("File does not exist: %s", self.path)
            return False
    
    def read(self):
        if not self.exists():
            raise Exception('File does not exist: %s', self.path)

        f = open(self.path, 'r')
        return f.read()


class BugExResultFile(BugExFile):
    """
    This represents a BugEx result file.
    
    It provides a method to convert itself to a model class.
    """
    
    def __init__(self, file_path):
        BugExFile.__init__(self, file_path, file_type="XML")

    def convert(self):
        pass