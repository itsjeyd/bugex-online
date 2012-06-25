'''
Created on 19.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@googlemail.com>
'''
# internal dependencies
from bugex_decorators import Singleton
from bugex_timer import PeriodicTask
from bugex_base import UserRequest, BugExConfig
from bugex_instance import BugExProcessInstance
from bugex_files import BugExFile
import core_config

# external dependencies
from datetime import datetime
import logging

@Singleton
class BugExMonitor(object):
    """
    The BugExMonitor needs to be notified upon a new user request.
    
    It will start the BugEx process and monitor the result file.
    It is a Singleton, retrieve an instance with:
    
    bug_mon = BugExMonitor.Instance()
    
    """
    
    def __init__(self):
        # init file job list
        self.__monitor_jobs = list()

        # logging
        self.__log = logging.getLogger("BugExMonitor")
        self.__log.info('BugExMonitor created.')

    def __create_job(self, user_request):
        # get output path
        request_path = user_request.folder
        
        # gather necessary data
        user_archive_path = user_request.user_archive.path
        failing_test_case = user_request.failing_test_case
        token = user_request.token
        
        # get config options
        bugex_executable = core_config.EXECUTABLE
        bugex_debug = core_config.DEBUG
        bugex_interval = core_config.CHECK_INTERVAL
        bugex_delay = core_config.ARTIFICIAL_DELAY
        
        # create instance
        bugex_instance = BugExProcessInstance(
            bugex_executable, user_archive_path, failing_test_case,
            request_path, token, bugex_delay)
        
        bugex_instance.debug = bugex_debug
        
        # create job
        job = BugExMonitorJob(bugex_instance, user_request)
        job.schedule(bugex_interval)
        
        # store reference to job
        self.__monitor_jobs.append(job)
        
        
    def shutdown(self):
        # cancel all jobs
        for job in self.__monitor_jobs:
            job.cancel()
            
        self.__log.info('Shutting down FileMonitor.')
    
    def new_request(self, request):
        # create file job
        self.__create_job(request)


class BugExMonitorJob(object):
    """
    The BugExMonitorJob monitors one BugExInstance.
    
    If the instance terminates in time, it stores the result to the database.
    """
    
    def __init__(self, bug_ex_instance, user_request):
        # members
        self._bug_ex_instance = bug_ex_instance
        self._user_request = user_request
        self._task = None # no task yet
        self._tries = 0
        self._creation_date = datetime.now()
    
        # job name
        self.name = 'job-' + user_request.token
        
        # logging
        self._log = logging.getLogger(self.name)
                
        if core_config.DEBUG:
            self._log.setLevel('DEBUG')
        else:
            self._log.setLevel('INFO')
            
        # done!
        self._log.info('Created FileMonitorJob \'%s\'', self.name)
    
    def run(self):
        self._log.debug('running the job.. (try %s)', str(self._tries))
        
        # increase try count
        self._tries += 1
        
        # check stop criteria
        
        # (1) life time
        time_diff = datetime.now() - self._creation_date    #timedelta
        if (time_diff.total_seconds() > core_config.MAX_LIFE_TIME):
            self.cancel('Maximum life time exceeded (%s seconds)',
                        str(time_diff.total_seconds()))
            return
        
        # (2) check process status
        status = self._bug_ex_instance.status
        
        if status == -1:
            self._log.debug('BugEx is not ready..')
            return
        elif not status == 0:
            self._user_request.status = 'FAIL'
            self.cancel('BugEx terminated unsuccessfully (status code %s)!', status)
            return
        
        # check result file
        if not self._bug_ex_instance.result_file.exists():
            self.cancel('Result file should exist, but does not.')
            return
           
        print (self._bug_ex_instance.result_file.read())
        
        # convert and store this to database
        pass
    
        # success
        self.cancel('Success!')
        self._user_request.status = 'SUCCESS'
        pass
    
    def schedule(self, interval):
        # start process
        self._bug_ex_instance.start()
        
        # create timer task
        self._task = PeriodicTask(interval, self.run)
        
        # start task
        self._task.start()
        self._log.info('Scheduled to run every %s seconds.', str(interval))
            
    def cancel(self, message, *args):
        self._log.info(message, *args)
        self._task.cancel()
    
    def convert(self, result_file):
        pass
        
#
#TESTING AREA
#

# singleton tests
#f = Foo() # Error, this isn't how you get the instance of a singleton
#f = FileMonitor.Instance() # Good. Being explicit is in line with the Python Zen
#g = FileMonitor.Instance() # Returns already created instance
#print f is g # True

#test_file = BugExFile('/home/freddy/bugex-results.xml','xml')
#status_file = BugExFile('/home/freddy/bugex-results.xml','xml')

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format = FORMAT) # this has to be done somewhen!
#logging.basicConfig() 

user_request = UserRequest()
user_request.token = '82230841-bcbe-451c-8b3e-e1365ad7f257'
user_request.user_archive = BugExFile(user_request.folder+'failing-program-0.0.1-SNAPSHOT-jar-with-dependencies.jar','jar')
user_request.failing_test_case = 'de.mypackage.TestMyClass#testGetMin'

bug_mon = BugExMonitor.Instance()
bug_mon.new_request(user_request)
#bug_mon.new_request(UserRequest())
#file_mon.new_request(UserRequest())

"""
raw_shell_input_sh  = '/home/freddy/bugex.sh /home/freddy/bugex-mock-0.0.4-SNAPSHOT-jar-with-dependencies.jar /home/freddy/failing-program-0.0.1-SNAPSHOT-jar-with-dependencies.jar de.mypackage.TestMyClass#testGetMin /home/freddy/ 1'
raw_shell_input_jv  = 'java -jar /home/freddy/bugex-mock-0.0.4-SNAPSHOT-jar-with-dependencies.jar /home/freddy/failing-program-0.0.1-SNAPSHOT-jar-with-dependencies.jar de.mypackage.TestMyClass#testGetMin /home/freddy/ 1'
raw_shell_input_jv2 = 'java -jar /home/freddy/bugex-mock-0.0.4-SNAPSHOT-jar-with-dependencies.jar failing-program-0.0.1-SNAPSHOT-jar-with-dependencies.jar de.mypackage.TestMyClass#testGetMin /home/freddy/ 1'
"""
"""
subprocess.Popen(['java'
                  ,'-jar'
                  ,'/home/freddy/bugex-mock-0.0.4-SNAPSHOT-jar-with-dependencies.jar'
                  ,'/home/freddy/failing-program-0.0.1-SNAPSHOT-jar-with-dependencies.jar'
                  ,'de.mypackage.TestMyClass#testGetMin'
                  ,'/home/freddy/'
                  ,'10'])
"""
"""
args = raw_shell_input_jv.split()
sp = subprocess.Popen(args)

args2 = raw_shell_input_jv2.split()
sp2 = subprocess.Popen(args2, cwd='/home/freddy/')
print sp2.poll()

import time
time.sleep(5)

#streamdata = sp2.communicate()[0]
print sp2.poll()
print sp2.returncode

#subprocess.Popen([raw_shell_input_sh], shell=True)
"""