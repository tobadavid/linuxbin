# PETSc compile en local par David Thomas

if [ -d /home/ulg/mtfc/dthomas/InstalledSoftwares/petsc-3.7.5 ] ; then
    if [ -z "${PETSC_DIR}" ] ; then
        export PETSC_DIR=/home/ulg/mtfc/dthomas/InstalledSoftwares/petsc-3.7.5
    else
        PETSC_DIR=${PETSC_DIR}:/home/ulg/mtfc/dthomas/InstalledSoftwares/petsc-3.7.5
    fi
fi

if [ -d /home/ulg/mtfc/dthomas/InstalledSoftwares/petsc-3.7.5/arch-python-linux-x86_64 ] ; then
    if [ -z "${PETSC_ARCH}" ] ; then
        export PETSC_ARCH=arch-python-linux-x86_64
    else
        PETSC_ARCH=${PETSC_ARCH}:arch-python-linux-x86_64
    fi
fi

