'''
Created on 21.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@googlemail.com>
'''
# internal dependencies
from bugex_files import BugExFile, BugExResultFile
import core_config

# external dependencies
from datetime import datetime
import logging
import subprocess
import os
import shlex
#from py4j.java_gateway import JavaGateway

class BugExInstance(object):
    '''
    Abstract representation of a BugEx instance.

    Stores information about a running BugEx process.
    Available implementations:
    - BugExProcessInstance (utilizes subprocess module)
    - BugExJavaInstance (utilizes Py4J java gateway)

    '''
    #RESULT_FILE_NAME = 'bugex-results.xml'

    def __init__(self, user_archive_path, failing_test_case_name
                 , working_folder_path, token, artificial_delay = 0):
        '''
        Constructor, initializes members and checks if the user archive exists.

        '''
        self._failing_test_case = failing_test_case_name    # a String
        self._working_folder = working_folder_path          # a String (path, trailing /)
        self._artificial_delay = artificial_delay           # an Integer
        self._token = token                                 # a String

        self._user_archive = BugExFile(user_archive_path,'zip')

        # load result file name from config
        result_file_name = core_config.RESULT_FILE_NAME

        self.result_file = BugExResultFile(
                                self._build_path(result_file_name))
        self.debug = False      # in debug mode, consider delay
        self._start_date = None # start with start() method

        #print "ok, guys."
        #print "der case is {0}, der folder is {1}, das delay betraegt {2}, token is wompe? {3}, das user archive findeste hier {4}".format(
        #         failing_test_case_name, working_folder_path, artificial_delay, token, user_archive_path)

        if not self._user_archive.exists():
            raise Exception('The defined user archive does not exist: \'{0}\''.format(
                            self._user_archive.path))

    def start(self):
        raise Exception('This is an abstract class!')

    def kill(self):
        raise Exception('This is an abstract class!')

    @property
    def status(self):
        raise Exception('This is an abstract class!')

    def _build_path(self, file_name):
        """
        Returns absolute path for a file in the working folder.

        """
        file_path = os.path.join(self._working_folder,file_name)
        return file_path


class BugExJavaInstance(BugExInstance):
    '''
    Representation of a BugEx instance via Py4J gateway.

    TODO: Not implemented yet.
    '''

    def __init__(self):
        '''
        TODO: Not implemented yet.
        '''

        self.gateway = 'gateway-placeholder'

        raise Exception('Not implemented yet.')



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

    def __init__(self, bug_ex_executable, user_archive_path,
                  failing_test_case_name, working_folder_path, token,
                  artificial_delay = 0):

        BugExInstance.__init__(
            self, user_archive_path, failing_test_case_name,
            working_folder_path, token, artificial_delay)

        self.name = 'bugex-instance-'+self._token+'-subprocess'

        # process information
        self._bug_ex_executable = bug_ex_executable
        # process variable
        self.__process = None

        #print "und bugex is hier {0}".format(
        #         bug_ex_executable)


        # logging
        self._log = logging.getLogger(self.name)

        if self.debug:
            self._log.setLevel('INFO') # show more stuff in debug mode

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
        """
        Kills the current process.

        """

        self.__run_check()
        self.__process.kill()


    @property
    def status(self):
        """
        Retrieves exit code from the process.

        Returns -1, if process has not finished yet.

        """

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
        """
        Checks if current process is running, raises Exception if not.

        """

        if self.__process is None:
            raise Exception(
                'You have to start the instance \'{}\' first!'.format(self.name))


    def __build_args(self):
        """
        Builds the command line arguments for a BugEx subprocess.

        Returns a list of arguments.

        The pattern is:
        java -jar <bug_ex_executable> <input_archive_path> <failing_test_case>
            <working_folder> (<artificial_delay>)

        """

        args = 'java -jar "{0}" "{1}" "{2}" "{3}"'
        if self.debug:
            # consider delay
            args += ' "{4}"'
            args = args.format(
                self._bug_ex_executable, self._user_archive.path,
                self._failing_test_case, self._working_folder,
                self._artificial_delay)
        else:
            # ignore delay
            args = args.format(
                self._bug_ex_executable, self._user_archive.path,
                self._failing_test_case, self._working_folder)
        return shlex.split(args)
