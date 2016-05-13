
function mtfconfig
{
    cmake -G"Eclipse CDT4 - Unix Makefiles" -D_ECLIPSE_VERSION=4.4  -DCMAKE_ECLIPSE_GENERATE_SOURCE_PROJECT=TRUE -C ../oo_meta/CMake/ubuntu.cmake ../oo_meta
}

function mtfauto
{
    export PYTHONSTARTUP=/home/boman/dev/Metafor/oo_metaB/bin/.pythonrc.py
}

function zipdev
{
    zip -1 -r dev.zip oo_meta oo_nda
}
