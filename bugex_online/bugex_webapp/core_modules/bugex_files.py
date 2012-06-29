'''
Created on 21.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@googlemail.com>
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
            logging.info("File does not exist: %s", self.path)
            return False
    
    def read(self):
        if not self.exists():
            raise Exception('File does not exist: %s', self.path)

        try:
            f = open(self.path, 'r')
            return f.read()
        except Exception as e:
            logging.warn("Something went wrong while reading the file '%s': %s",
                         self.path, e.strerror)
            
        finally:
            f.close()


class BugExResultFile(BugExFile):
    """
    This represents a BugEx result file.
    
    It provides a method to convert itself to a model class.
    """
    
    def __init__(self, file_path):
        BugExFile.__init__(self, file_path, file_type="XML")

    def convert(self):
        pass