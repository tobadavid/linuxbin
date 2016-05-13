# this script adds ~/dev/progs/bin in PATH 

if [ -d ~/dev/progs/bin ] ; then
    if [ -z "${PATH}" ] ; then
       export PATH="~/dev/progs/bin"
    else
       export PATH="~/dev/progs/bin:${PATH}"
    fi
fi

