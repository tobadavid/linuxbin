# the .profile is sometimes read by "dash" and we cannot provide 
# a sourced script with some parameters (it is a "bashism")
#
#
# recompiled gcc
export PATH=/opt/gcc-4.8.2/bin:$PATH
export LD_LIBRARY_PATH=/opt/gcc-4.8.2/lib64:$LD_LIBRARY_PATH
# icc
#if [ -n "$BASH_VERSION" ]; then
   #if [ -z "$MKLROOT" ]; then  # pas suffisant! (MKLROOT transmis au "at" mais pas LD_LIBRARY_PATH)
#      . /opt/intel/bin/compilervars.sh intel64
   #fi
#fi
