This is the ~/bin directory of a linux account
----------------------------------------------
RoBo


INSTALL:

Please, add the following calls to the end of the .bashrc/.profile cfg files

.profile: (PATH and other env vars)
    . $HOME/bin/cfg/loop.sh ; fct_loop profile $* ; unset fct_loop

.bashrc: (interactive stuffs)
    . ~/bin/cfg/loop.sh ; fct_loop bashrc $* ; unset fct_loop


