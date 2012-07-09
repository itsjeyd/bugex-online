'''
Created on 19.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@googlemail.com>
'''
import threading

class PeriodicTask(threading._Timer):
    """
    The PeriodicTask is a recurring Timer.
    
    Regularly executes a function, interval given in seconds, e.g.:
    
    pt = PeriodicTask(30.0, f, args=[], kwargs={})
    t.start()     # executes f every 30 seconds
    t.cancel()    # stop the tasks's action
    
    """
    
    def __init__(self, *args, **kwargs):
        threading._Timer.__init__(self, *args, **kwargs)
        self._canceled = False
        #print 'Created task..'
    
    def run(self):
        while True:
            if self._canceled:
                # timer has been canceled
                self.finished.clear()
                self.finished.set()
                break
            else:
                self.finished.clear()
                self.finished.wait(self.interval)
                if not self.finished.isSet():
                    # if last job finished, execute again
                    self.function(*self.args, **self.kwargs)
                else:
                    return
                self.finished.set()
            
    def cancel(self):
        # even a periodic task needs to be canceled sometimes!
        self._canceled = True
        #print 'Canceled task..'


class UserRequestThread(threading.Thread):
    """
    The UserRequestThread is responsible for calling _parse_archive()
    and _run_bugex() on the user request.

    This runs in a separate thread and allows the (browser) view to render
    before the archive is processed.

    """

    def __init__(self, user_request):
        """
        Arguments:

        user_request -- the user request to be used
        """
        super(UserRequestThread, self).__init__(group = None)
        self.user_request = user_request

    def run(self):
        self.user_request._async_processing()
        #self.user_request._parse_archive()
        #self.user_request._run_bugex()
