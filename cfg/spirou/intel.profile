
. /opt/intel/compilers_and_libraries/mac/mkl/bin/mklvars.sh intel64
. /opt/intel/compilers_and_libraries/mac/tbb/bin/tbbvars.sh intel64

add2env DYLD_LIBRARY_PATH "/opt/intel/tbb/lib"
add2env DYLD_LIBRARY_PATH "/opt/intel/mkl/lib"
