# pcre (swig) compile localement par RB

if [ -d /home/ulg/nlcm/rboman/local/pcre-8.33/lib ] ; then
    if [ -z "${LIB}" ] ; then
        export LIB=/home/ulg/nlcm/rboman/local/pcre-8.33/lib
    else
        LIB=$LIB:/home/ulg/nlcm/rboman/local/pcre-8.33/lib
    fi
fi

if [ -d /home/ulg/nlcm/rboman/local/pcre-8.33/include ] ; then
    if [ -z "${INCLUDE}" ] ; then
        export INCLUDE=/home/ulg/nlcm/rboman/local/pcre-8.33/include
    else
        INCLUDE=$INCLUDE:/home/ulg/nlcm/rboman/local/pcre-8.33/include
    fi
fi

if [ -d /home/ulg/nlcm/rboman/local/pcre-8.33/lib ] ; then
    if [ -z "${LD_LIBRARY_PATH}" ] ; then
        export LD_LIBRARY_PATH=/home/ulg/nlcm/rboman/local/pcre-8.33/lib
    else
        LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/ulg/nlcm/rboman/local/pcre-8.33/lib
    fi
fi



