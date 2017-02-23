# Parasolid

# adds pskernel.so to the PATH

if [ -d /opt/parasolid-28.1/shared_object ] ; then
    if [ -z "${PATH}" ] ; then
       export PATH="/opt/parasolid-28.1/shared_object"
    else
       export PATH="/opt/parasolid-28.1/shared_object:${PATH}"
    fi
    if [ -z "${LD_LIBRARY_PATH}" ] ; then
       export LD_LIBRARY_PATH="/opt/parasolid-28.1/shared_object"
    else
       export LD_LIBRARY_PATH="/opt/parasolid-28.1/shared_object:${LD_LIBRARY_PATH}"
    fi

fi

# adds parasolid INCLUDE dir

if [ -d /opt/parasolid-28.1 ] ; then
    if [ -z "${INCLUDE}" ] ; then
       export INCLUDE="/opt/parasolid-28.1"
    else
       export INCLUDE="/opt/parasolid-28.1:${INCLUDE}"
    fi
fi

export P_SCHEMA=/opt/parasolid-28.1/schema

