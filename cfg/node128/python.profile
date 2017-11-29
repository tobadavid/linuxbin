
module load python/2.7.10

# trucs qui manquent dans le modulefile de David

if [ -d /cm/shared/apps/python/2.7.10 ] ; then
    if [ -z "${CMAKE_PREFIX_PATH}" ] ; then
        export CMAKE_PREFIX_PATH=/cm/shared/apps/python/2.7.10
    else
        CMAKE_PREFIX_PATH=/cm/shared/apps/python/2.7.10:${CMAKE_PREFIX_PATH}
    fi
fi

