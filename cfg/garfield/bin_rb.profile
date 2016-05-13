# this script adds ~/bin/rb in PATH 

if [ -d ~/bin/rb ] ; then
    if [ -z "${PATH}" ] ; then
       export PATH="~/bin/rb"
    else
       export PATH="~/bin/rb:${PATH}"
    fi
fi

