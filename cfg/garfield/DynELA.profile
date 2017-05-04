# DynELA: http://pantale.free.fr/Recherche/DynELA.html

if [ -d $HOME/dev/DynELA/DynELA ] ; then
    export DynELA_ROOT=$HOME/dev/DynELA/DynELA
    export DynELA_BIN=$DynELA_ROOT/bin
    export DynELA_BASE=$DynELA_ROOT/sources
    export DynELA_SAMPLES=$DynELA_ROOT/samples
    export PATH=$PATH:$DynELA_BIN
fi

