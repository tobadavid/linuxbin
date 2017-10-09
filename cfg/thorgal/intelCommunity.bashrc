# this should be done in the .profile but if the shell is dash
# it does not work.
# => we call intel cf file  in both places (bashrc & profile)

if [ -z "$MKLROOT" ]; then
    . /opt/intel/mkl/bin/mklvars.sh intel64
fi
if [ -z "$TBBROOT" ]; then
    . /opt/intel/tbb/bin/tbbvars.sh intel64
fi

