# the .profile is sometimes read by "dash" and we cannot provide 
# a sourced script with some parameters (it is a "bashism")

if [ -n "$BASH_VERSION" ]; then
   #if [ -z "$MKLROOT" ]; then  # pas suffisant! (MKLROOT transmis au "at" mais pas LD_LIBRARY_PATH)
      . /opt/intel/bin/compilervars.sh intel64 # mets intel mpi par defaut!
      #. /opt/intel/mkl/bin/mklvars.sh intel64
      #. /opt/intel/tbb/bin/tbbvars.sh intel64
   #fi
fi
