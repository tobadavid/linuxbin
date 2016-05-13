
module load cmake
module load gcc/4.9.2
#module load openmpi/1.8.4/gcc-4.9.2
module load openmpi/1.6.4/gcc-4.9.2

#module load openmpi/1.7.5/intel2013_sp1.1.106
#module load intel/compiler/64/14.0/2013_sp1.1.106
module load intel/tbb
module load intel/mkl

# sinon cmake build avec /usr/bin/c++...
export CC=gcc
export CXX=g++
export FC=gfortran


