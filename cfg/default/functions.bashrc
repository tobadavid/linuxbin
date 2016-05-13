# Fonctions generales

function backup()
{
    ARC=backup-profile-bin.tar.gz
    REP=`pwd`
    cd ~
    rm -f $ARC
    tar cf - .bashrc .profile .emacs bin | gzip > $ARC
    echo "~/$ARC created."
    cd $REP
}

function bat()
{
    cd /home/$USER/dev
    comp.py
}

