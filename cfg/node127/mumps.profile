# mumps compile localement par RB

if [ -d /home/ulg/nlcm/rboman/local/mumps-4.10.0/lib ] ; then
    if [ -z "${LIB}" ] ; then
        export LIB=/home/ulg/nlcm/rboman/local/mumps-4.10.0/lib
    else
        LIB=$LIB:/home/ulg/nlcm/rboman/local/mumps-4.10.0/lib
    fi
fi

if [ -d /home/ulg/nlcm/rboman/local/mumps-4.10.0/include ] ; then
    if [ -z "${INCLUDE}" ] ; then
        export INCLUDE=/home/ulg/nlcm/rboman/local/mumps-4.10.0/include
    else
        INCLUDE=$INCLUDE:/home/ulg/nlcm/rboman/local/mumps-4.10.0/include
    fi
fi

