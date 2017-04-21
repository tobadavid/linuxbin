# Samcef v15.01-3

if [ -d /opt/SamcefField/V8.5-01/Samcef-V151i8/lin/bin ] ; then
    export SAM_ZONE=200000000
    add2env PATH "/opt/SamcefField/V8.5-01/Samcef-V151i8/lin/bin"
    export SAM_USE_FLEXLM=1
    export SAMTECH_LICENSE_FILE=@pegase.ltas.ulg.ac.be
    #export SAMTECH_LICENSE_FILE=/opt/SamcefField/V8.5-01/SAMTECH.lic
fi

