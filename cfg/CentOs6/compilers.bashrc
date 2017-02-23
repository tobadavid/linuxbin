# this should be done in the .profile but if the shell is dash
# it does not work.
# => we call intel cf file  in both places (bashrc & profile)

# recompiled gcc
export PATH=/opt/gcc-4.8.2/bin:$PATH
export LD_LIBRARY_PATH=/opt/gcc-4.8.2/lib64:$LD_LIBRARY_PATH

# icc
#if [ -z "$MKLROOT" ]; then
#   . /opt/intel/bin/compilervars.sh intel64
#fi

