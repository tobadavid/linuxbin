# Samcef

if [ -d /opt/Samv18i8 ] ; then
    export SAM_ZONE=200000000
    add2env PATH "/opt/samcef"
    # pas besoin de definir LMS_LICENSE
    # (deja defini dans "/opt/samcef/site" lors de l'install)
fi

