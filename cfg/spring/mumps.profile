# $Id$
#
# configuration to allow CMake to automatically find mumps 
#
LIB=$LIB:/opt/mumps-4.10.0/lib
export LIB
INCLUDE=$INCLUDE:/opt/mumps-4.10.0/include
export INCLUDE

# not necessary while cmake link with absolute path to libs
#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mumps-4.10.0/lib
#export LD_LIBRARY_PATH
