# $Id: loop.sh 1755 2013-05-30 12:18:36Z boman $
# 
# usage: 
#   add the following calls to the end of the .bashrc/.profile cfg files
#   .profile: (PATH and other env vars)
#      . $HOME/bin/cfg/loop.sh ; fct_loop profile $* ; unset fct_loop
#   .bashrc: (interactive stuffs)
#      . $HOME/bin/cfg/loop.sh ; fct_loop bashrc $* ; unset fct_loop
#
# arg1 is the extension of the files to be loaded
# arg2 is the name of the master node if needed (clusters)
#
# if this script is sometimes run with dash (not bash!)
# (by gnome on ubuntu for the .profile)
#  => avoid bashisms (e.g. ~ becomes $HOME)
#
# RoBo 2013


function add2env()
{
    if [ $# -lt 2 ] || [ $# -gt 3 ] ; then
        echo "add2env VARNAME folder [front]"
        return
    fi
    if [ -d $2 ] ; then          # if the second arg is an existing folder
        if [ -z ${!1} ] ; then   # if the first arg is an empty variable
            #echo $1 is empty
            eval export $1="$2"
        else
            #echo $1 is not empty
            if [ "$3" == "front" ] ; then
                eval export $1="$2:\$$1"  # add folder to the front
            else
                eval export $1="\$$1:$2"  # add folder to the end
            fi
        fi
    fi   
}

function fct_loop()
{
    umask 007

    #echo "Execute loop.sh"
    #echo "script=$0"
    #echo "nargs=$#"
    #echo "arguments=$*"
    #for var in "$@"; do
    #	echo "var=$var"
    #done
    
    if [ "x$2" != "x" ] && [ -d "$thisdir/$2" ]; then
        myhost=$2
    else
        myhost=`hostname -s`
    fi
    #echo "myhost=" $myhost
    
    thisdir="$HOME/bin/cfg"
    
    # default cfg
    
    for i in $thisdir/default/*.$1 ; do
    #echo "testing script $i ..."
    if [ -r $i ]; then
        # do not read file if a file with the same name exists in the "myhost" folder
        if [ ! -f $thisdir/$myhost/`basename $i` ] ; then
            #echo "  =>loading script $i ..."
            . $i
        fi
    fi
    done
    
    # machine-dependent cfg
    
    for i in $thisdir/$myhost/*.$1 ; do
        #echo "testing script $i ..."
        if [ -r $i ]; then
            #echo "  =>loading script $i ..."
            . $i
        fi
    done
    unset i
}
