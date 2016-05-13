# Trilinos custom compilé localement


# (permet le FIND_PACKAGE(Trilinos) dans CMake)

if [ -z "${CMAKE_PREFIX_PATH}" ] ; then
   export CMAKE_PREFIX_PATH="/home/boman/local/trilinos"
else
   export CMAKE_PREFIX_PATH="/home/boman/local/trilinos:${CMAKE_PREFIX_PATH}"
fi

