# adds DynELA to env variables

if [ -d /home/boman/dev/DynELA/DynELA ] ; then
    export DynELA_ROOT=/home/boman/dev/DynELA/DynELA
    export DynELA_BIN=$DynELA_ROOT/bin
    export DynELA_BASE=$DynELA_ROOT/sources
    export DynELA_SAMPLES=$DynELA_ROOT/samples
    export PATH=$PATH:$DynELA_BIN
fi


