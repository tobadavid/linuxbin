module load cmake

# --- ICC ---
# Metafor ne compile plus avec ces vieux compilateurs intel
# Le probleme vient du gcc sous jacent qui est bcp trop vieux (headers foireux)
#module load intel/compiler/64/14.0/2013_sp1.3.174 

# --- GCC ---
module load gcc/4.9.2
module load openmpi/1.6.4/gcc-4.9.2 # EVITER openmpi 1.8.4!
module load intel/tbb/64/4.2/2013_sp1.3.174
module load intel/mkl/64/11.1/2013_sp1.3.174

# sinon cmake build avec /usr/bin/c++...
export CC=gcc
export CXX=g++
export FC=gfortran


