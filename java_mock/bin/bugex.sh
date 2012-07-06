#!/bin/sh
#
# BUGEX-MOCK start script
#
# Date: 20/06/2012
#
# Author: Frederik Leonhardt
#
# Usage:
#
# bugex.sh <input_archive> <failing_test_case> <output_file>
#
# - 1st argument specifies external jar archive with failing test case (Format: '/home/freddy/failing-program.jar')
# - 2nd argument specifies failing test case (Format: 'fully.qualified.class.name#method')
# - 3rd argument specifies output folder (Format: '/home/freddy/')
# - (optional) 4th argument specifies artificial delay of BugEx in seconds, for simulating long runs (Format: '60')
# 
# Example:
#
# bugex.sh failing-program.jar de.mypackage.TestMyClass#testGetMin /home/freddy/

BUGEX_CURRENT=0.0.5

if [ $# -lt 3 ]
then
    echo "Invalid number of arguments ($#)!"
    echo "Usage: `basename $0` <input_archive> <failing_test_case> <output_file> (<delay>)"
    exit 65
else
 echo "Running BugEx version $BUGEX_CURRENT..."
 java -jar bugex-mock-$BUGEX_CURRENT-SNAPSHOT-jar-with-dependencies.jar $*
fi
