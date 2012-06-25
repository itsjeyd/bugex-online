'''
Created on 19.06.2012

@author: Frederik Leonhardt <frederik.leonhardt@googlemail.com>
'''
# user request
from bugex_files import BugExFile
import uuid

# config
import ConfigParser, os, logging
from bugex_decorators import Singleton

class UserRequest(object):
    """
    The UserRequest is the central object linked to all important information.
    
    This is a mock implementation of the UserRequest, containing all information
    needed for the monitoring system.
    
    """
    def __init__(self):
        # create an unique token and set status to pending
        self.token = str(uuid.uuid4())
        self.status = 'PENDING'

    @property
    def path(self):
        """
        Returns the working  path on the disk for this request.
        
        """
        #return '/tmp/{0}/'.format(self.token)
        return "{0}/{1}/".format(BugExConfig.Instance().working_dir,self.token)
        
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status
        # notify notifier..
        print 'Status of {0} changed to: {1}'.format(self.token, self._status)
        pass


@Singleton    
class BugExConfig(object):
    """
    The BugExConfig is linked to a configuration file and contains all
    variables, which can be customized by the system administrator.
    
    The entries dictionary contains an overview over all supported
    options.
    
    BugExConfig is a Singleton, instantiate with:
    
    conf = BugExConfig.Instance()
    
    """

    # all supported entries of the config file and their sections
    entries = {'WORKING_DIR': 'BugExOnline',    # working directory of BugExOnline
               
               'DEBUG': 'BugExOnline',          # determines if bugex instances run in debug mode,
                                                # gives more log output and uses artificial delay for mockup
                                                
               'RESULT_FILE_NAME': 'BugEx',     # name of the result file produced by bugex
               
               'EXECUTABLE': 'BugEx',           # full path to bugex executable
               
               'CHECK_INTERVAL': 'Monitoring',  # monitoring interval in seconds
               
               'MAX_RETRIES': 'Monitoring',     # maximum number of retries
               
               'MAX_LIFE_TIME' : 'Monitoring'}  # maximum life time of a monitoring job

    # name of the config file
    CONFIG_FILE_NAME = 'core.conf'

    def __init__(self, force_defaults = False):
        """
        Tries to initialize the BugExConfig by loading the config file.
        
        Writes default config file, if no config file exists yet.
        Setting force_defaults to True will force a config rebuild as well.
        
        """
        # members
        self._config = ConfigParser.RawConfigParser()
        self._config_path = "{0}/{1}".format(os.getcwd(),self.CONFIG_FILE_NAME)
        config_file = BugExFile(self._config_path, "conf")
        
        # logging
        self.__log = logging.getLogger("BugExConfig")
        self.__log.setLevel('INFO')
        
        if not config_file.exists() or force_defaults:
            # write defaults to file
            self.__write_defaults()
        
        # load file
        self.reload_config()
    
    
    def __write_defaults(self):
        """
        Writes the default configuration to file.
        
        """
        
        self._config.add_section('BugEx')
        self._config.set('BugEx', 'RESULT_FILE_NAME', 'bugex-results.xml')
        self._config.set('BugEx', 'EXECUTABLE',
            '/home/freddy/bugex-mock-0.0.4-SNAPSHOT-jar-with-dependencies.jar')
        
        self._config.add_section("BugExOnline")
        self._config.set('BugExOnline', 'WORKING_DIR', '/tmp')
        self._config.set('BugExOnline', 'DEBUG', 'True')

        self._config.add_section("Monitoring")
        self._config.set('Monitoring', 'CHECK_INTERVAL', '1.0')
        self._config.set('Monitoring', 'MAX_RETRIES', '100')
        self._config.set('Monitoring', 'MAX_LIFE_TIME', str(12 * 60 * 60))

        self.__log.info("Writing default configuration to '%s'", self._config_path)

        try:
            with open(self._config_path, 'wb') as configfile:
                self._config.write(configfile)
        except IOError as e:
            self.__log.error("Could not write to configuration file '%s': %s",
                             self._config_path, e.strerror)


    def reload_config(self):
        """
        Reloads the configuration file.
        
        """
        
        self.__log.info("Reloading config file '%s'...", self._config_path)
        self._config.read(self._config_path)
        
        # log config content
        config_content = "Using configuration:"
        for section in self._config.sections():
            config_content += "\n[{}]".format(str(section))
            config_items = self._config.items(section)
            for item in config_items:
                key, value = item
                config_content += "\n{0} = {1}".format(str(key),str(value))
  
        self.__log.info(config_content)


    def _get_option(self, option):
        """
        Returns an arbitrary configuration option.
        
        Automatically looks up the appropriate Section from Entries-Table.
        
        """
        
        return self._config.get(self.entries[option], option)
    
    def str2bool(self, v):
        """
        Converts a string to a boolean value.
        
        Returns true if string is "yes", "true", "t" or 1.
        Returns false in any other case.
        
        """
        
        return v.lower() in ("yes", "true", "t", "1")
    
    # convenient getters for the options
    @property
    def working_dir(self):
        return str(self._get_option('WORKING_DIR'))
    
    @property
    def result_file_name(self):
        return str(self._get_option('RESULT_FILE_NAME'))
    
    @property
    def executable(self):
        return str(self._get_option('EXECUTABLE'))
    
    @property
    def debug(self):
        return self.str2bool(self._get_option('DEBUG'))

    @property
    def check_interval(self):
        return float(self._get_option('CHECK_INTERVAL'))

    @property
    def max_retries(self):
        return int(self._get_option('MAX_RETRIES'))
    
    @property
    def max_life_time(self):
        return int(self._get_option('MAX_LIFE_TIME'))