# [ BUG EX ONLINE ]

from os import getcwd

# The absolute path to the bugex_online directory
ROOT_PATH = getcwd()

# Working directory of BugExOnline.
# It holds all user data.
#WORKING_DIR = '/tmp/bugex'

# A boolean that turns on/off debug mode.
# It determines if bugex instances run in debug mode,
# which produces more log output and uses artificial delay for the mockup
DEBUG = True

# Defines the artificial delay for the BugEx Mockup in seconds.
# Will only be used in DEBUG mode.
ARTIFICIAL_DELAY = 10


# [ BUG EX ]

# The name of the result file produced by BugEx.
RESULT_FILE_NAME = 'bugex-results.xml'

# Absolute path of the BugEx executable.
EXECUTABLE = '{0}/../java_mock/bin/bugex-mock-0.0.5-SNAPSHOT-jar-with-dependencies.jar'.format(ROOT_PATH)

# [ MONITORING ]

# Interval in seconds, in which the system will check if a BugEx process has finished.
# Default is 30.0 seconds.
CHECK_INTERVAL = 5.0

# Maximum lifetime in seconds a monitor job will live.
# Default is 12 hours.
MAX_LIFE_TIME = 12 * 60 * 60
