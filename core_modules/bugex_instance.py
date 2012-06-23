'''
Created on 21.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@dfki.de>
'''
from bugex_files import BugExFile, BugExResultFile
from datetime import datetime
import logging
import subprocess
#from py4j.java_gateway import JavaGateway

class BugExInstance(object):
    '''
    Abstract representation of a BugEx instance.

    Stores information about a running BugEx process.
    Available implementations:
    - BugExProcessInstance (utilizes subprocess module)
    - BugExJavaInstance (utilizes Py4J java gateway)

    '''
    RESULT_FILE_NAME = 'bugex-results.xml'

    def __init__(self, user_archive_path, failing_test_case_name
                 , working_folder_path, token, artificial_delay = 0):
        '''
        Constructor
        '''
        self._failing_test_case = failing_test_case_name    # a String
        self._working_folder = working_folder_path          # a String (path, trailing /)
        self._artificial_delay = artificial_delay           # an Integer
        self._token = token                                 # a String
        
        self._user_archive = BugExFile(user_archive_path,'zip')
        self.result_file = BugExResultFile(self._build_path(self.RESULT_FILE_NAME))
        self.debug = False      # in debug mode, consider delay
        self._start_date = None
        
        if not self._user_archive.exists():
            raise Exception('The defined user archive does not exist: \'%s\''
                            ,self._user_archive.path)
    
    def start(self):
        raise Exception('This is an abstract class!')
    
    def kill(self):
        raise Exception('This is an abstract class!')
    
    @property
    def status(self):
        raise Exception('This is an abstract class!')
    
    def _build_path(self, file_name):
        file_path = self._working_folder + file_name
        return file_path
    
class BugExJavaInstance(BugExInstance):
    '''
    TODO
    '''

    def __init__(self):
        '''
        TODO
        '''
        
        self.gateway = 'gateway-placeholder'
        pass

        
class BugExProcessInstance(BugExInstance):
    """
    Representation of a BugEx instance as threaded subprocess.
    
    Stores information about a running BugEx process. After creating the
    instance, it needs to be started via the start() method.

    
    bug_ex = BugExProcessInstance( '/home/freddy/bugex.jar'
                                  , '/tmp/828272/achive.jar'
                                  , 'class.Name#failMethod'
                                  , '/tmp/828272/')
    
    """
    
    def __init__(self, bug_ex_executable, user_archive_path
                 , failing_test_case_name, working_folder_path, token
                 , artificial_delay = 0):
        
        BugExInstance.__init__(self, user_archive_path
                               , failing_test_case_name, working_folder_path
                               , token, artificial_delay)
        
        self.name = 'bugex-instance-'+self._token+'-subprocess'

        # process information
        self._bug_ex_executable = bug_ex_executable
        # process variable
        self.__process = None
        
        # logging
        self._log = logging.getLogger(self.name)
        self._log.setLevel('INFO') # for testing purpose
        
        # done!
        self._log.info('Created BugExProcessInstance \'%s\'', self.name)
        
        
    def start(self):
        """
        Creates necessary subprocess and starts it.
        """
        
        self._start_date = datetime.now()
        
        # prepare arguments
        args = self.__build_args()
        
        # create log file
        log_file = open(super(BugExProcessInstance,self)._build_path('bugex.log')
                        , 'w')
        log_file.write("BugEx Process Log - "+self.name+"\n\n")
        
        #print self._user_archive.path
        
        # run bugex
        self.__process = subprocess.Popen(args, stdout=log_file, stderr=log_file)
            
    
    def kill(self):
        self.__run_check()
        self.__process.kill()


    @property
    def status(self):
        self.__run_check()
        
        # get status from subprocess
        status = self.__process.poll()
        
        self._log.info("Status after %s seconds: %s"
                       , datetime.now() - self._start_date, status)
        
        if status is None:
            return -1
        else:
            return status


    def __run_check(self):
        if self.__process is None:
            raise Exception('You have to start the instance \'{}\' first!'.format(self.name))
    
    
    def __build_args(self):
        args = "java -jar {0} {1} {2} {3}"
        fargs = ""
        if self.debug:
            # consider delay
            args += " {4}"
            fargs = args.format(self._bug_ex_executable, self._user_archive.path
                                , self._failing_test_case, self._working_folder
                                , self._artificial_delay)
        else:
            # ignore delay
            fargs = args.format(self._bug_ex_executable, self._user_archive.path
                                , self._failing_test_case, self._working_folder)
        
        return fargs.split()