module load sge

module load cmake samcef swig python qt vtk
module load isosurf gmsh tetgen triangle matlab
module load scilab git
module load gcc
module load mumps gmm trilinos parasolid

# old intel-cluster-studio
#module load intel-tbb
#module load intel-cl-st/compiler/64/12.0/084
#module load intel-cl-st/mkl/64/10.3/084

module load abaqus
module load subversion/1.8.9

# new intel-cluster-studio
. /cm/shared/apps/ics/2013sp1/ics/2013.1.046/ictvars.sh intel64
#. /cm/shared/apps/ics/2013sp1/mkl/bin/mklvars.sh intel64
#. /cm/shared/apps/ics/2013sp1/tbb/bin/tbbvars.sh intel64


# sinon cmake prend /usr/bin/cc même si gcc est dans le PATH!
#export CC=gcc
#export CXX=g++
#export FC=gfortran


export CC=$(which icc)
export CXX=$(which icpc)
export FC=$(which ifort)


