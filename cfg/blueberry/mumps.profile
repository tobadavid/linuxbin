# $Id$
#
# configuration to allow CMake to automatically find mumps 
#
LIB=$LIB:/opt/mumps-4.10.0-TbbIcc/lib
export LIB
INCLUDE=$INCLUDE:/opt/mumps-4.10.0-TbbIcc/include
export INCLUDE
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mumps-4.10.0-TbbIcc/lib
export LD_LIBRARY_PATH
