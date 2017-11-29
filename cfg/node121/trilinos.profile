# trilinos compile en local par RB 

if [ -d /home/ulg/nlcm/rboman/local/trilinos-12.6.1 ] ; then
    if [ -z "${CMAKE_PREFIX_PATH}" ] ; then
        export CMAKE_PREFIX_PATH=/home/ulg/nlcm/rboman/local/trilinos-12.6.1
    else
        CMAKE_PREFIX_PATH=/home/ulg/nlcm/rboman/local/trilinos-12.6.1:${CMAKE_PREFIX_PATH}
    fi
fi

