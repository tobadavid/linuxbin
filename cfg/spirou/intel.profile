


. /opt/intel/compilers_and_libraries/mac/mkl/bin/mklvars.sh intel64
. /opt/intel/compilers_and_libraries/mac/tbb/bin/tbbvars.sh intel64

export DYLD_LIBRARY_PATH=/opt/intel/tbb/lib/:$DYLD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=/opt/intel/mkl/lib/:$DYLD_LIBRARY_PATH


