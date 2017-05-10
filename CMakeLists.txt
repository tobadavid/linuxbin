#
# $Id: CMakeLists.txt 2645 2016-05-12 06:29:38Z boman $
#

SET(PYMODULES parametricJob.py 
              prmClasses.py
              prmClassesGui.py
              Metafor.png
)

SET(PYSCRIPTS externalProgramPath.py
              externalProgramPathGui.pyw
              launch.py
              launchGui.pyw
              postProLoop.py
              postProLoopGui.pyw
)

INSTALL(FILES ${PYMODULES} DESTINATION .)
INSTALL(PROGRAMS ${PYSCRIPTS} DESTINATION .)

