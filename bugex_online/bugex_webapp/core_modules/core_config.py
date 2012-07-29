# [ BUG EX ONLINE ]

# A boolean that turns on/off debug mode.
# It determines if bugex instances run in debug mode,
# which produces more log output and uses artificial delay for the mockup
DEBUG = True

# Defines the artificial delay for the BugEx Mockup in seconds.
# Will only be used in DEBUG mode.
ARTIFICIAL_DELAY = 5


# [ BUG EX ]

# The name of the result file produced by BugEx.
RESULT_FILE_NAME = 'bugex-results.xml'

# Absolute path of the BugEx executable.
EXECUTABLE = '/var/django/bugex-mock-0.0.6-SNAPSHOT-jar-with-dependencies.jar'

# [ MONITORING ]

# Interval in seconds, in which the system will check if a BugEx process has finished.
# Default is 30.0 seconds.
CHECK_INTERVAL = 5.0

# Maximum lifetime in seconds a monitor job will live.
# Default is 12 hours.
MAX_LIFE_TIME = 12 * 60 * 60
