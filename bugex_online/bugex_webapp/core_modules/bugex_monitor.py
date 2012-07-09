'''
Created on 19.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@googlemail.com>
'''
# stdlib dependencies
import logging
import sys, traceback
from datetime import datetime

# django dependencies
from bugex_webapp import UserRequestStatus

# internal dependencies
import core_config
from bugex_decorators import Singleton
from bugex_timer import PeriodicTask
from bugex_instance import BugExProcessInstance

@Singleton
class BugExMonitor(object):
    """
    The BugExMonitor needs to be notified upon a new user request.

    It will start the BugEx process and monitor the result file.
    It is a Singleton, retrieve an instance with:

    bug_mon = BugExMonitor.Instance()

    """

    def __init__(self):
        """
        Only to be called by Instance()

        Initializes the job list and the logging facilities.

        """
        # init file job list
        self.__monitor_jobs = list()

        # logging
        self.__log = logging.getLogger("BugExMonitor")
        self.__log.info('BugExMonitor created.')

    def __create_job(self, user_request):
        """
        For internal use only. This method takes care of initializing a task
        with all necessary data.

        """
        # get output path
        request_path = user_request.folder

        # gather necessary data
        user_archive_path = user_request.codearchive.path
        failing_test_case = user_request.test_case
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
        """
        This method should be called on system shutdown.
        It cancels all monitored tasks and their BugEx instances.

        """
        # cancel all jobs
        for job in self.__monitor_jobs:
            job.cancel()

        self.__log.info('Shutting down FileMonitor.')

    def new_request(self, request):
        """
        This is the notification interface. It needs to be called upon creation
        of a new UserRequest and will take care of executing BugEx and
        monitoring the process.

        It also updates the request's status according to the progress and
        persists the results to the database.

        """
        # create file job
        self.__create_job(request)


class BugExMonitorJob(object):
    """
    The BugExMonitorJob monitors one BugExInstance.

    If the instance terminates in time, it stores the result to the database.
    """

    def __init__(self, bug_ex_instance, user_request):
        """
        A BugExMonitorJob needs a BugExInstance to monitor and a UserRequest
        for status update and notifications.

        """
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


    def _run(self):
        """
        The run() method checks if
        - a stop criteria of the job has been met. This can either be the
          maxmimum execution time, or an unexpected BugEx exit code.
          In this case the job is being canceled.
        - BugEx finished successfully. In this case it tries to parse
          and persist the resulting XML file to the database.

        The run() method should be called periodically by a PeriodicTask.
        Calling the schedule() method will take care of scheduling and
        running the task.

        """
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
            self._log.debug('BugEx is not ready yet..')
            return
        elif not status == 0:
            self._user_request.update_status(UserRequestStatus.FAILED)
            self.cancel(
                ("BugEx terminated unsuccessfully (status code %s)! " +
                "Please check bugex.log in the request directory for more " +
                "details."), status)
            return

        # check result file
        if not self._bug_ex_instance.result_file.exists():
            self.cancel('Result file should exist, but does not.')
            return

        xml_content = self._bug_ex_instance.result_file.read()

        self._log.debug('Processing XML: \n%s',xml_content)

        # convert and store this to database
        try:
            # defered import to avoid circular dependency problems
            from bugex_webapp.models import BugExResult
            BugExResult.new(xml_content)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            self.cancel('Could not store the BugExResult: %s',e)
            self._user_request.update_status(UserRequestStatus.FAILED)
            return

        # success
        self.cancel('Success!')
        self._user_request.update_status(UserRequestStatus.FINISHED)


    def schedule(self, interval):
        """
        The schedule method starts the underlying BugEx instance.
        Also it sets up a periodic task to check for completion.

        The interval specifies the time in seconds between executing the
        run() method.

        """
        # start process
        self._bug_ex_instance.start()

        # create timer task
        self._task = PeriodicTask(interval, self._run)

        # start task
        self._task.start()
        self._log.info('Scheduled to run every %s seconds.', str(interval))


    def cancel(self, message, *args):
        """
        This method cancels the underlying task.

        """
        self._log.info(message, *args)
        self._task.cancel()
