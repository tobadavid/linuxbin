#!/usr/bin/env python
# -*- coding: latin-1; -*-
# $Id: externalProgramPathGui.pyw 2384 2015-09-22 10:07:54Z papeleux $
#
#
# Gui to configure externals program path according to local configuration
# 
#execfile('.pythonrc.py')
from PyQt4 import QtCore, QtGui
from externalProgramPath import *
from prmClassesGui import *

import sys
# avec pythonw : pas de console => les prints sont interdits => redirection des sorties stdout et stderr vers os.devnull !!!
if (sys.executable.split( '\\' )[-1] == 'pythonw.exe'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

class ExtProgsConfGui(QtGui.QWidget):
    app = QtGui.QApplication(sys.argv)
    def __init__(self, parent=None):        
        # parent constructor
        QtGui.QWidget.__init__(self, parent)
        # -----------guis datas ----------------       
        self.guiPRM={}
        self.sf={}
        # ----------- externalProgramPath ----------------       
        self.extProgPath = ExtProgs(False)
        # ---------- draw frames -------------------------------        
        #   |--------------------------------|
        #   |  Applications :                |
        #   |       - Meshers                |
        #   |       - curvePlotter           |
        #   |       - image/text             |
        #   |--------------------------------|
        #   |  Buttons                       |
        #   |--------------------------------|
        mainBox = QtGui.QVBoxLayout()
        mainBox.setContentsMargins(2,2,2,2)        
        self.setLayout(mainBox)
        #  Application Frame   
        self.buildApplicationFrame(mainBox)
        # Button Box
        self.buildButtonFrame(mainBox)
        self.resize(500, 450)
        self.setWindowTitle('External Program Configurator for Metafor')      
        try:
            iconFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./Metafor.png")
            self.setWindowIcon(QtGui.QIcon(iconFile))
        except:        
            pass
        
    def buildApplicationFrame(self, box):
        appFrame = QtGui.QFrame()                            
        box.addWidget(appFrame)                          
        if isUnix():
            exeFileType ="Exe files (*)"
        else:
            exeFileType ="Exe files (*.exe)"
        
        #Mesher box
        self.mesherGrpBox  = QtGui.QGroupBox("Meshers")
        box.addWidget(self.mesherGrpBox)
        grplay1 = QtGui.QGridLayout()
        grplay1.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay1)
        
        if isUnix():
            self.sf['SAMCEF']    = ExeFileLine(self, grplay1, self.extProgPath.pars['SAMCEF'], exeFileType, 0, 0, 4)
        else:
            self.sf['SAMCEF']    = ExeFileLine(self, grplay1, self.extProgPath.pars['SAMCEF'], "cmd files (*.cmd)", 0, 0, 4)

        self.sf['GMSH']        = ExeFileLine(self, grplay1, self.extProgPath.pars['GMSH'],     exeFileType, 1, 0, 4)
        self.sf['TRIANGLE']    = ExeFileLine(self, grplay1, self.extProgPath.pars['TRIANGLE'], exeFileType, 2, 0, 4)
        self.sf['TETGEN']      = ExeFileLine(self, grplay1, self.extProgPath.pars['TETGEN'],   exeFileType, 3, 0, 4)
        self.sf['ISOSURF']     = ExeFileLine(self, grplay1, self.extProgPath.pars['ISOSURF'],  exeFileType, 4, 0, 4)
   
        #CurvePlotter box        
        self.mesherGrpBox  = QtGui.QGroupBox("Post Pro")
        box.addWidget(self.mesherGrpBox)
        grplay2 = QtGui.QGridLayout()
        grplay2.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay2)
        self.sf['MATLAB']        = ExeFileLine(self, grplay2, self.extProgPath.pars['MATLAB'],     exeFileType, 0, 0, 4)
        self.sf['SCILAB']        = ExeFileLine(self, grplay2, self.extProgPath.pars['SCILAB'],     exeFileType, 1, 0, 4)
        self.sf['GNUPLOT']       = ExeFileLine(self, grplay2, self.extProgPath.pars['GNUPLOT'],    exeFileType, 2, 0, 4)
        
        #Text & image 
        self.mesherGrpBox  = QtGui.QGroupBox("Text & Image")
        box.addWidget(self.mesherGrpBox)
        grplay3 = QtGui.QGridLayout()
        grplay3.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay3)
        self.sf['LATEX']             = ExeFileLine(self, grplay3, self.extProgPath.pars['LATEX'],     exeFileType, 0, 0, 4)
        self.sf['GHOSTSCRIPT']       = ExeFileLine(self, grplay3, self.extProgPath.pars['GHOSTSCRIPT'],     exeFileType, 1, 0, 4)
        self.sf['IMAGEMAGICK']       = ExeFileLine(self, grplay3, self.extProgPath.pars['IMAGEMAGICK'],    exeFileType, 2, 0, 4)
        
    def buildButtonFrame(self, box):      
        # == Buttons Frame ==
        butframe = QtGui.QFrame()
        box.addWidget(butframe)
        butlayout = QtGui.QHBoxLayout(); 
        butlayout.setContentsMargins(0,0,0,0)
        butframe.setLayout(butlayout)
        # buttons        
        self.saveButton1 = QtGui.QPushButton(self.tr("Local User Save")) 
        butlayout.addWidget(self.saveButton1)
        self.connect(self.saveButton1, QtCore.SIGNAL("pressed()"), self.userSave)
        
        self.saveButton2 = QtGui.QPushButton(self.tr("All Users Save")) 
        butlayout.addWidget(self.saveButton2)
        self.connect(self.saveButton2, QtCore.SIGNAL("pressed()"), self.progSave)
        
        self.quitButton = QtGui.QPushButton(self.tr("Quit")) 
        butlayout.addWidget(self.quitButton)
        self.connect(self.quitButton, QtCore.SIGNAL("pressed()"), self.quit)            
                  
    def updateWidgetsValues(self):
        self.extProgPath.applyDependencies()
        if self.extProgPath.debug :
            print "updateWidgetsValues"
        for var in self.sf:
            self.sf[var].setParamValue()
             
    def updateWidgetsVisibility(self):
        if self.extProgPath.debug :
            print "updateWidgetsVisibility"
        # update enabled/disabled of options  
        self.extProgPath.configActions()
        for var in self.sf:
            self.sf[var].setEnabled(self.extProgPath.pars[var].enabled)           
    def updateWidgetsValues(self):
        if self.extProgPath.debug :
            print "updateWidgetsVisibility"
        # update enabled/disabled of options  
        self.extProgPath.configActions()
        for var in self.sf:
            self.sf[var].setEnabled(self.extProgPath.pars[var].enabled)       
    def userSave(self):     
        if self.extProgPath.debug :
            print "Save pressed"
        self.extProgPath.savePars()   
    def progSave(self):   
        if self.extProgPath.debug :  
            print "Save pressed"
        self.extProgPath.savePars('.')

    def quit(self):
        if self.extProgPath.debug :
            print "Quit pressed"   
        sys.exit()     
        
# ============== Main ========================        
def main():    
    # create gui    
    confGui = ExtProgsConfGui()    
    # opening Gui 
    confGui.show()    
    # signal pour cloturer proprement l'application PyQt quand on ferme la fenetre
    confGui.app.connect(confGui.app, QtCore.SIGNAL("lastWindowClosed()"),confGui.app,QtCore.SLOT("quit()"))
    #print "ready."
    sys.exit(confGui.app.exec_())
    
if __name__ == "__main__":
    try:
        import signal  
        signal.signal(signal.SIGBREAK, sigbreak);
    except:
        pass
    main()
