# In order for python to find the ucilib module (without installing in a
# system python location) it is necessary to add this directory to the
# PYTHONPATH environment variable.  To do that one can source this
# script from the ucilib root directory.  This shell script is for bash
# users.
#
# If LOCATION_OF_THIS_FILE is the location of this file one can do that
# as follows:
#
# > cd ${LOCATION_OF_THIS_FILE}
# > source ./addThisDirToPythonPath.sh
# > cd -

export PYTHONPATH=${PYTHONPATH}:`pwd`
