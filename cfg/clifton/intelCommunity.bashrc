# this should be done in the .profile but if the shell is dash
# it does not work.
# => we call intel cf file  in both places (bashrc & profile)

if [ -z "$MKLROOT" ]; then
#   . /opt/intel/bin/compilervars.sh intel64
    . /opt/intelCommunity2017/mkl/bin/mklvars.sh intel64
fi
if [ -z "$TBBROOT" ]; then
    . /opt/intelCommunity2017/tbb/bin/tbbvars.sh intel64
fi
