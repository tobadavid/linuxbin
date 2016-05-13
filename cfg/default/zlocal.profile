# this script adds ~/local 
# in several env variables as a local software directory

if [ -d ~/local/bin ] ; then
    if [ -z "${PATH}" ] ; then
       export PATH="~/local/bin"
    else
       export PATH="~/local/bin:${PATH}"
    fi
fi

if [ -d ~/local/lib ] ; then
    if [ -z "${LD_LIBRARY_PATH}" ] ; then
       export LD_LIBRARY_PATH="~/local/lib"
    else
       export LD_LIBRARY_PATH="~/local/lib:${LD_LIBRARY_PATH}"
    fi
    if [ -z "${LIB}" ] ; then
       export LIB="~/local/lib"
    else
       export LIB="~/local/lib:${LIB}"
    fi
fi

if [ -d ~/local/include ] ; then
    if [ -z "${LIB}" ] ; then
       export INCLUDE="~/local/include"
    else
       export INCLUDE="~/local/include:${INCLUDE}"
    fi
fi

