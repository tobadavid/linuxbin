# gmm compile localement par RB

if [ -d /home/ulg/nlcm/rboman/local/gmm-4.2.1/include ] ; then
    if [ -z "${INCLUDE}" ] ; then
        export INCLUDE=/home/ulg/nlcm/rboman/local/gmm-4.2.1/include
    else
        INCLUDE=$INCLUDE:/home/ulg/nlcm/rboman/local/gmm-4.2.1/include
    fi
fi

