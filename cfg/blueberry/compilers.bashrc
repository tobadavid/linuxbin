# this should be done in the .profile but if the shell is dash
# it does not work.
# => we call intel cf file  in both places (bashrc & profile)

#if [ -z "$MKLROOT" ]; then
   #. /opt/intel/bin/compilervars.sh intel64
    . /opt/intel/bin/iccvars2.sh intel64
#fi

