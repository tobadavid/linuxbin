module load slurm

module load git subversion
module load gcc cmake swig
module load python qt vtk parasolid mumps
#module load gmm trilinos

module load samcef gmsh 
#module load isosurf tetgen triangle
module load matlab scilab


# intel community 
#. /cm/shared/apps/intel-community/2017.2/bin/compilervars.sh intel64
. /cm/shared/apps/intel-community/2017.2/mkl/bin/mklvars.sh intel64
. /cm/shared/apps/intel-community/2017.2/tbb/bin/tbbvars.sh intel64

# new intel-cluster-studio
#. /cm/shared/apps/ics/2013sp1/ics/2013.1.046/ictvars.sh intel64
#. /cm/shared/apps/ics/2013sp1/mkl/bin/mklvars.sh intel64
#. /cm/shared/apps/ics/2013sp1/tbb/bin/tbbvars.sh intel64


# sinon cmake prend /usr/bin/cc meme si gcc est dans le PATH!
export CC=gcc
export CXX=g++
export FC=gfortran

#icc
#export CC=$(which icc)
#export CXX=$(which icpc)
#export FC=$(which ifort)


