# Parasolid

# adds pskernel.so to the PATH

if [ -d ~/local/parasolid-28.1/shared_object ] ; then
    if [ -z "${PATH}" ] ; then
       export PATH="~/local/parasolid-28.1/shared_object"
    else
       export PATH="~/local/parasolid-28.1/shared_object:${PATH}"
    fi
fi

# adds parasolid INCLUDE dir

if [ -d ~/local/parasolid-28.1 ] ; then
    if [ -z "${INCLUDE}" ] ; then
       export INCLUDE="~/local/parasolid-28.1"
    else
       export INCLUDE="~/local/parasolid-28.1:${INCLUDE}"
    fi
fi

export P_SCHEMA=~/local/parasolid-28.1/schema

