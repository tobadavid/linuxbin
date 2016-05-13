# permet d'installer un metafor compilé
# (plus très utile depuis scripts Luc?)

if [ -d ~/MetaforBIN ] ; then
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/MetaforBIN
    export PATH=$PATH:~/MetaforBIN  
fi


