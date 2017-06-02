#!/usr/bin/env python
# -*- coding: latin-1; -*-
#
# Gui to configure externals program path according to local configuration

## Qt ##
foundQt=0
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui  import *
    foundQt=4
except:
    pass  
    
try:
    from PyQt5.QtCore    import *
    from PyQt5.QtGui     import *
    from PyQt5.QtWidgets import *
    foundQt=5
except:
    pass     
if not foundQt:
    raise Exception("PyQt4/5 not found!") 
#print "PyQt%d (Qt %s) loaded!" % (foundQt, QT_VERSION_STR)


from externalProgramPath import *
from prmClassesGui import *
import sys

# avec pythonw : pas de console => les prints sont interdits => redirection des sorties stdout et stderr vers os.devnull !!!
if (sys.executable.split( '\\' )[-1] == 'pythonw.exe'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')


class ExtProgsConfGui(QWidget):
    app = QApplication(sys.argv)
    
    def __init__(self, parent=None):        
        # parent constructor
        QWidget.__init__(self, parent)
        # -----------guis datas ----------------       
        self.guiPRM={}
        self.sf={}
        # ----------- externalProgramPath ----------------       
        self.extProgPath = ExtProgs(verb=False)
        # ---------- draw frames -------------------------------        
        #   |--------------------------------|
        #   |  Applications :                |
        #   |       - Meshers                |
        #   |       - curvePlotter           |
        #   |       - image/text             |
        #   |--------------------------------|
        #   |  Buttons                       |
        #   |--------------------------------|
        mainBox = QVBoxLayout()
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
            self.setWindowIcon(QIcon(iconFile))
        except:        
            pass
        
    def buildApplicationFrame(self, box):
        appFrame = QFrame()                            
        box.addWidget(appFrame)                          
        if isUnix():
            exeFileType ="Exe files (*)"
        else:
            exeFileType ="Exe files (*.exe)"
        
        #Mesher box
        self.mesherGrpBox  = QGroupBox("Meshers")
        box.addWidget(self.mesherGrpBox)
        grplay1 = QGridLayout()
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
        self.mesherGrpBox  = QGroupBox("Post Pro")
        box.addWidget(self.mesherGrpBox)
        grplay2 = QGridLayout()
        grplay2.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay2)
        self.sf['MATLAB']        = ExeFileLine(self, grplay2, self.extProgPath.pars['MATLAB'],     exeFileType, 0, 0, 4)
        self.sf['SCILAB']        = ExeFileLine(self, grplay2, self.extProgPath.pars['SCILAB'],     exeFileType, 1, 0, 4)
        self.sf['GNUPLOT']       = ExeFileLine(self, grplay2, self.extProgPath.pars['GNUPLOT'],    exeFileType, 2, 0, 4)
        
        #Text & image 
        self.mesherGrpBox  = QGroupBox("Text & Image")
        box.addWidget(self.mesherGrpBox)
        grplay3 = QGridLayout()
        grplay3.setColumnStretch(2,1)
        self.mesherGrpBox.setLayout(grplay3)
        self.sf['LATEX']             = ExeFileLine(self, grplay3, self.extProgPath.pars['LATEX'],     exeFileType, 0, 0, 4)
        self.sf['GHOSTSCRIPT']       = ExeFileLine(self, grplay3, self.extProgPath.pars['GHOSTSCRIPT'],     exeFileType, 1, 0, 4)
        self.sf['IMAGEMAGICK']       = ExeFileLine(self, grplay3, self.extProgPath.pars['IMAGEMAGICK'],    exeFileType, 2, 0, 4)
        
    def buildButtonFrame(self, box):      
        # == Buttons Frame ==
        butframe = QFrame()
        box.addWidget(butframe)
        butlayout = QHBoxLayout(); 
        butlayout.setContentsMargins(0,0,0,0)
        butframe.setLayout(butlayout)
        # buttons        
        self.saveButton1 = QPushButton(self.tr("Local User Save")) 
        butlayout.addWidget(self.saveButton1)
        self.saveButton1.pressed.connect(self.userSave)
        
        self.saveButton2 = QPushButton(self.tr("All Users Save")) 
        butlayout.addWidget(self.saveButton2)
        self.saveButton2.pressed.connect(self.progSave)
        
        self.quitButton = QPushButton(self.tr("Quit")) 
        butlayout.addWidget(self.quitButton)
        self.quitButton.pressed.connect(self.quit)           
                  
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
    confGui.app.lastWindowClosed.connect(confGui.app.quit)
    #print "ready."
    sys.exit(confGui.app.exec_())
    
if __name__ == "__main__":
    try:
        import signal  
        signal.signal(signal.SIGBREAK, sigbreak);
    except:
        pass
    main()
