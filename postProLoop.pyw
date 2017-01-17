#!/usr/bin/env python
# -*- coding: latin-1; -*-
# $Id: externalProgramPathGui.pyw 2384 2015-09-22 10:07:54Z papeleux $
#
#
# Gui to configure externals program path according to local configuration
# 
#execfile('.pythonrc.py')
from PyQt4 import QtCore, QtGui
from prmClassesGui import *
from postProLoop import *

import sys
# avec pythonw : pas de console => les prints sont interdits => redirection des sorties stdout et stderr vers os.devnull !!!
if (sys.executable.split( '\\' )[-1] == 'pythonw.exe'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

class PostProLoopGui(QtGui.QWidget):
    app = QtGui.QApplication(sys.argv)
    def __init__(self, parent=None):        
        # parent constructor
        QtGui.QWidget.__init__(self, parent)
        # -----------guis datas ----------------       
        self.guiPRM={}
        self.sf={}
        # ----------- externalProgramPath ----------------       
        self.postProLoop = PostProLoop(False)
        # ---------- draw frames -------------------------------        
        #   |--------------------------------|
        #   |  BaseDir :                     |
        #   |       - options                |
        #   |--------------------------------|
        #   |  Matlab :                      |
        #   |       - options                |
        #   |--------------------------------|
        #   |  GhostScript :                 |
        #   |       - options                |
        #   |--------------------------------|
        #   |  Python :                      |
        #   |       - options                |
        #   |--------------------------------|
        #   |  Latex :                       |
        #   |       - options                |
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
        self.setWindowTitle('PostPro Loop Utilities')      
        try:
            iconFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./Metafor.png")
            self.setWindowIcon(QtGui.QIcon(iconFile))
        except:        
            pass
        
    def buildApplicationFrame(self, box):
        appFrame = QtGui.QFrame()                            
        box.addWidget(appFrame)        
        
        #Dir box
        self.mesherGrpBox  = QtGui.QGroupBox("Base Directories of post processing")
        box.addWidget(self.mesherGrpBox)
        grplay1 = QtGui.QGridLayout()
        grplay1.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay1)
            
        self.sf['DIRNAME']      = PathLine    (self, grplay1, self.postProLoop.pars['DIRNAME'], 0, 0, 4)              
        self.sf['MULTITEST']    = CheckBoxLine(self, grplay1, self.postProLoop.pars['MULTITEST'], 1, 0)          
        self.sf['DIRWILDCARD']  = TextLine    (self, grplay1, self.postProLoop.pars['DIRWILDCARD'], 1, 3, 1) #, QtGui.QIntValidator(-1,100000))


                    
        if isUnix():
            exeFileType ="Exe files (*)"
        else:
            exeFileType ="Exe files (*.exe)"
            
        #Matlab box
        self.mesherGrpBox  = QtGui.QGroupBox("Matlab")
        box.addWidget(self.mesherGrpBox)
        grplay2 = QtGui.QGridLayout()
        grplay2.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay2)
                    
        self.sf['MATLABRUN']       = CheckBoxLine(self, grplay2, self.postProLoop.pars['MATLABRUN'], 0, 0)    
        self.sf['MATLABEXE']       = ExeFileLine (self, grplay2, self.postProLoop.pars['MATLABEXE'], exeFileType, 1, 0, 4)
        self.sf['MATLABCMD']       = TextLine    (self, grplay2, self.postProLoop.pars['MATLABCMD'], 2, 0, 4)   
        self.sf['MATLABPATH']      = PathLine    (self, grplay2, self.postProLoop.pars['MATLABPATH'], 3, 0, 4)
        self.sf['MATLABREQUEST']   = TextLine    (self, grplay2, self.postProLoop.pars['MATLABREQUEST'], 4, 0, 4)
        
        #GhostScript box
        self.mesherGrpBox  = QtGui.QGroupBox("GhostScript (eps -> png)")
        box.addWidget(self.mesherGrpBox)
        grplay3 = QtGui.QGridLayout()
        grplay3.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay3)
                    
        self.sf['GSRUN']           = CheckBoxLine(self, grplay3, self.postProLoop.pars['GSRUN'], 0, 0)     
        self.sf['GSEXE']           = ExeFileLine (self, grplay3, self.postProLoop.pars['GSEXE'], exeFileType, 1, 0, 4)
        self.sf['GSFILTER']        = TextLine    (self, grplay3, self.postProLoop.pars['GSFILTER'], 2, 0, 1)
        self.sf['GSOUTPUTFORMAT']  = MultiPMRLine(self, grplay3, self.postProLoop.pars['GSOUTPUTFORMAT'],3, 0)
        self.sf['GSDEFINITION']    = TextLine    (self, grplay3, self.postProLoop.pars['GSDEFINITION'], 3, 3, 1, QtGui.QIntValidator(72,1800))
        self.sf['GSREQUEST']       = TextLine    (self, grplay3, self.postProLoop.pars['GSREQUEST'], 4, 0, 1)

        #build Latex box
        self.mesherGrpBox  = QtGui.QGroupBox("Python")
        box.addWidget(self.mesherGrpBox)
        grplay4 = QtGui.QGridLayout()
        grplay4.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay4)
                    
        self.sf['PYTHONRUN']           = CheckBoxLine(self, grplay4, self.postProLoop.pars['PYTHONRUN'], 0, 0)     
        self.sf['PYTHONMODULE']        = FileLine    (self, grplay4, self.postProLoop.pars['PYTHONMODULE'], '*.py', 1, 0, 4)
        self.sf['PYTHONSCRIPT']        = TextLine    (self, grplay4, self.postProLoop.pars['PYTHONSCRIPT'], 2, 0, 4)
        self.sf['PYTHONREQUEST']       = TextLine    (self, grplay4, self.postProLoop.pars['PYTHONREQUEST'], 3, 0, 4)
        '''
        #build Latex box
        self.mesherGrpBox  = QtGui.QGroupBox("Latex")
        box.addWidget(self.mesherGrpBox)
        grplay5 = QtGui.QGridLayout()
        grplay5.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay5)
                    
        self.sf['LATEXRUN']           = CheckBoxLine(self, grplay5, self.postProLoop.pars['LATEXRUN'], 0, 0)     
        self.sf['LATEXCMD']           = TextLine    (self, grplay5, self.postProLoop.pars['LATEXCMD'], 1, 0, 4)
        self.sf['LATEXREQUEST']       = TextLine    (self, grplay5, self.postProLoop.pars['LATEXREQUEST'], 2, 0, 4)
        '''        
        
    def buildButtonFrame(self, box):      
        # == Buttons Frame ==
        butframe = QtGui.QFrame()
        box.addWidget(butframe)
        butlayout = QtGui.QHBoxLayout(); 
        butlayout.setContentsMargins(0,0,0,0)
        butframe.setLayout(butlayout)
        # buttons        
        self.goButton = QtGui.QPushButton(self.tr("Go")) 
        butlayout.addWidget(self.goButton)
        self.connect(self.goButton, QtCore.SIGNAL("pressed()"), self.go)
        '''
        self.stopButton = QtGui.QPushButton(self.tr("Stop !!!"))
        butlayout.addWidget(self.stopButton)
        self.connect(self.stopButton, QtCore.SIGNAL("pressed()"), self.interrupt)
        '''
        self.saveButton = QtGui.QPushButton(self.tr("Save")) 
        butlayout.addWidget(self.saveButton)
        self.connect(self.saveButton, QtCore.SIGNAL("pressed()"), self.save)
        
        self.quitButton = QtGui.QPushButton(self.tr("Quit")) 
        butlayout.addWidget(self.quitButton)
        self.connect(self.quitButton, QtCore.SIGNAL("pressed()"), self.quit)            
         
                  
    def updateWidgetsValues(self):
        self.postProLoop.applyDependencies()
        if self.postProLoop.debug :
            print "updateWidgetsValues"
        for var in self.sf:
            self.sf[var].setParamValue()             
    def updateWidgetsVisibility(self):
        if self.postProLoop.debug :
            print "updateWidgetsVisibility"
        # update enabled/disabled of options  
        self.postProLoop.configActions()
        for var in self.sf:
            self.sf[var].setEnabled(self.postProLoop.pars[var].enabled)           
    def updateWidgetsValues(self):
        if self.postProLoop.debug :
            print "updateWidgetsVisibility"
        # update enabled/disabled of options  
        self.postProLoop.configActions()
        for var in self.sf:
            self.sf[var].setEnabled(self.postProLoop.pars[var].enabled)       
            
    def go(self):     
        if self.postProLoop.debug :
            print "Go pressed"
        self.postProLoop.go()
    def save(self):     
        if self.postProLoop.debug :
            print "Save pressed"
        self.postProLoop.savePars('.')   

    def quit(self):
        if self.postProLoop.debug :
            print "Quit pressed"   
        sys.exit()     
        
# ============== Main ========================        
def main():    
    # create gui    
    confGui = PostProLoopGui()    
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
