#!/bin/sh
#
# BUGEX-MOCK start script
#
# Author: Frederik Leonhardt
#
# Usage:
#
# bugex.sh <input_archive> <failing_test_case> <output_file>
#
# - First argument specifies external jar archive with failing test case (Format: '/home/freddy/failing-program.jar')
# - Second argument specifies failing test case (Format: 'fully.qualified.class.name#method')
# - Third argument specifies output folder (Format: '/home/freddy/')
#
# Example:
#
# bugex.sh failing-program.jar de.mypackage.TestMyClass#testGetMin /home/freddy/
if [ $# -ne 3 ]
then
    echo "Invalid number of arguments!"
    echo "Usage: `basename $0` <input_archive> <failing_test_case> <output_file>"
    exit 65
else
 java -jar bugex-mock-0.0.2-SNAPSHOT-jar-with-dependencies.jar $*
fi
