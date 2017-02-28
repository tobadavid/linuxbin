# $id$
#
# configuration to allow CMake to automatically find mumps 
#
export LIB=$LIB:/opt/mumps-4.10.0/lib
export INCLUDE=$INCLUDE:/opt/mumps-4.10.0/include

# not necessary while cmake link with absolute path to libs
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mumps-4.10.0/lib
