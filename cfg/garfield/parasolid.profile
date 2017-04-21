# Parasolid

# adds pskernel.so to the PATH

if [ -d ~/local/parasolid/shared_object ] ; then
    if [ -z "${PATH}" ] ; then
       export PATH="~/local/parasolid/shared_object"
    else
       export PATH="~/local/parasolid/shared_object:${PATH}"
    fi
fi

# adds parasolid INCLUDE dir

if [ -d ~/local/parasolid ] ; then
    if [ -z "${INCLUDE}" ] ; then
       export INCLUDE="~/local/parasolid"
    else
       export INCLUDE="~/local/parasolid:${INCLUDE}"
    fi
fi

export P_SCHEMA=~/local/parasolid/schema

