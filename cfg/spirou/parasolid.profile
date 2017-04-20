# Parasolid

# adds pskernel.so to the PATH

if [ -d /usr/local/parasolid/shared_object ] ; then
    if [ -z "${PATH}" ] ; then
       export PATH="/usr/local/parasolid/shared_object"
    else
       export PATH="/usr/local/parasolid/shared_object:${PATH}"
    fi
fi

# adds parasolid INCLUDE dir

if [ -d /usr/local/parasolid ] ; then
    if [ -z "${INCLUDE}" ] ; then
       export INCLUDE="/usr/local/parasolid"
    else
       export INCLUDE="/usr/local/parasolid:${INCLUDE}"
    fi
fi

export P_SCHEMA=/usr/local/parasolid/schema

export DYLD_LIBRARY_PATH=/usr/local/parasolid/shared_object/:$DYLD_LIBRARY_PATH

