#!/usr/bin/env python
# -*- coding: latin-1; -*-
#
# GUI de launch.py - version Qt

import os,sys
from prmClassesGui import *
from launch import *

#========================================================================================     
#========================================================================================     
#========================================================================================     
class LaunchGui(QtGui.QWidget):
    app = QtGui.QApplication(sys.argv)
    def __init__(self, launch, parent = None):    
        # association du launcher avec ici
        launch.setLaunchGui(self)  
        # parent constructor
        QtGui.QWidget.__init__(self, parent)
        # -----------guis datas ----------------       
        self.guiPRM={}
        self.sf={}
        # --------- redirection Stream to console ------------------
        self.process = None
        #self.outFile = None
        # ---------- load launch options ---------------------        
        self.launch = launch         
        self.launch.configActions()
        self.launch.applyDependencies()
        # ---------- draw frames -------------------------------
        #   |---------------------------------------------|
        #   |                BaseDir                      |
        #   |---------------------------------------------|
        #   |            |  Options :                     |
        #   |            |       - Launch                 |
        #   |            |       - runOptions             |
        #   |  Console   |       - Batch                  |
        #   |            |       - SGE                    |        
        #   |            |       - FTP                    |        
        #   |            |       - Email                  |        
        #   |            | Run Buttons                    |
        #   |---------------------------------------------|
        #        
        # main division (Vertical Layout)
        mainVBox = QtGui.QVBoxLayout()
        mainVBox.setContentsMargins(2,2,2,2)  
        self.setLayout(mainVBox)     
        # baseDir GroupBox
        self.baseDirGrpBox  = QtGui.QGroupBox("Base Dir")
        mainVBox.addWidget(self.baseDirGrpBox)
        baseDirGridLayout = QtGui.QGridLayout()
        self.baseDirGrpBox.setLayout(baseDirGridLayout)
        #grp0.setHeight(1)
        # gui is not starter from base dir => ...
        self.baseDir   = BaseDirMultiPRM(self.guiPRM, 'launchGui.cfg')
        self.gBaseDir  = BaseMultiDirPathLine(self, baseDirGridLayout, self.baseDir,  0, 0)    
        # cadre commun : console + Options 
        coFrame = QtGui.QFrame()                            
        mainVBox.addWidget(coFrame)        
        # division console/options (Horizontal Layout)
        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(2,2,2,2)
        coFrame.setLayout(hbox)
        # Ajout de la console
        #hbox.addWidget(self.myStream.console) 
        self.buildConsole()
        hbox.addWidget(self.console)                        
        # Ajout du frame d'options
        optFrame = QtGui.QFrame()
        optFrame.setMaximumSize(QtCore.QSize(500,999999))
        hbox.addWidget(optFrame)
        optVBox = QtGui.QVBoxLayout()
        optFrame.setLayout(optVBox)        
        #Ajout des Widgets d'options           
        self.buildParametersFrame(optVBox)
        #Ajout des Widgets d'action           
        self.buildButtonFrame(optVBox)      
        # --------------------------------
        self.resize(1100, 600)
        # --------------------------------            
        self.setWindowTitle('%s for Metafor' % sys.argv[0])
        #print "window defined"
        try:
            iconFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./Metafor.png")
            self.setWindowIcon(QtGui.QIcon(iconFile))
            #print "icon added"
        except:        
            pass

    def buildParametersFrame(self, vbox): 
        ''' rappel : 
        CheckBoxLine(_win, _grpLayout, _prm, nrow, ncol)
        TextLine(_win, _grpLayout, _prm, nrow, ncol, ncolSpan=1, validator = None)
        PathLine(_win, _grpLayout, _prm, nrow, ncol, ncolSpan=1)
        FileLine(_win, _grpLayout, _prm, _fileType, nrow, ncol, ncolSpan=1)
        MultiPMRLine(_win, _grpLayout, _prm, nrow, ncol, ncolSpan=1)
        MultiPathLine(_win, _grpLayout, _prm, nrow, ncol, ncolSpan=1)
        '''
        self.launchGrpBox  = QtGui.QGroupBox("Launch")
        vbox.addWidget(self.launchGrpBox)
        grplay1 = QtGui.QGridLayout()
        self.launchGrpBox.setLayout(grplay1)
        grplay1.setColumnStretch(2,1)
        if isUnix():
            self.sf['EXEC_NAME']    = FileLine(self, grplay1, self.launch.pars['EXEC_NAME'], "Exe files (*)", 0, 0, 4)
        else:
            self.sf['EXEC_NAME']    = FileLine(self, grplay1, self.launch.pars['EXEC_NAME'], "Exe files (*.exe)", 0, 0, 4)
        self.sf['TEST_NAME']    = FileLine(self, grplay1, self.launch.pars['TEST_NAME'], "Py files (*.py)", 1, 0, 4)      
        self.sf['TEST_DIR']     = PathLine(self, grplay1, self.launch.pars['TEST_DIR'], 2, 0, 4)      
        self.sf['ALGORITHM']    = MultiPMRLine(self, grplay1, self.launch.pars['ALGORITHM'],3,0)
        self.sf['MULTITEST']    = CheckBoxLine(self, grplay1, self.launch.pars['MULTITEST'], 3, 3)
        self.sf['RESTART_STEP'] = TextLine(self, grplay1, self.launch.pars['RESTART_STEP'], 4, 3, 1, QtGui.QIntValidator(-1,100000))
        self.sf['OUTFILE']      = TextLine(self, grplay1, self.launch.pars['OUTFILE'], 4, 0)
        
        # RUN OPTIONS        
        self.runOptGrpBox  = QtGui.QGroupBox("Run Options")
        vbox.addWidget(self.runOptGrpBox)
        grplay2 = QtGui.QGridLayout()
        self.runOptGrpBox.setLayout(grplay2) 
        grplay2.setColumnStretch(2,1)
        
        import multiprocessing        
        nbProcs = multiprocessing.cpu_count()
        self.sf['NB_TASKS']     = TextLine(self, grplay2, self.launch.pars['NB_TASKS'], 0, 0, 1, QtGui.QIntValidator(1,nbProcs))
        self.sf['NB_THREADS']   = TextLine(self, grplay2, self.launch.pars['NB_THREADS'], 0, 3, 1, QtGui.QIntValidator(1,nbProcs))
        self.sf['NICE_VALUE']   = TextLine(self, grplay2, self.launch.pars['NICE_VALUE'], 1, 0, 1, QtGui.QIntValidator(1,19))
        self.sf['AFFINITY']     = TextLine(self, grplay2, self.launch.pars['AFFINITY'], 1, 3, 1)                
        
        self.sf['RUNMETHOD']   = MultiPMRLine(self, grplay2, self.launch.pars['RUNMETHOD'],2,0)
        # BATCH OPTION
        
        self.batchOptGrpBox  = QtGui.QGroupBox("Batch Option")
        vbox.addWidget(self.batchOptGrpBox)
        grplay6 = QtGui.QGridLayout()
        self.batchOptGrpBox.setLayout(grplay6) 
        grplay6.setColumnStretch(2,1)
        self.sf['AT_TIME']     = TextLine(self, grplay6, self.launch.pars['AT_TIME'], 0, 0, 1)
        
        # SGE OPTIONS
        self.sgeOptGrpBox  = QtGui.QGroupBox("Sge Options")
        vbox.addWidget(self.sgeOptGrpBox)
        grplay4 = QtGui.QGridLayout()
        self.sgeOptGrpBox.setLayout(grplay4) 
        grplay4.setColumnStretch(2,1)
        
        self.sf['SGEQUEUE']     = TextLine(self, grplay4, self.launch.pars['SGEQUEUE'], 0, 0, 1)
        self.sf['SGELOCALDISK'] = CheckBoxLine(self, grplay4, self.launch.pars['SGELOCALDISK'], 0, 3)
        self.sf['SGEARGS']      = TextLine(self, grplay4, self.launch.pars['SGEARGS'], 1, 0, 4)
        
        # FTP OPTIONS
        self.ftpOptGrpBox  = QtGui.QGroupBox("FTP Options")
        vbox.addWidget(self.ftpOptGrpBox)
        grplay5 = QtGui.QGridLayout()
        self.ftpOptGrpBox.setLayout(grplay5) 
        grplay5.setColumnStretch(2,1)
        
        self.sf['ENABLE_FTP']  = CheckBoxLine(self, grplay5, self.launch.pars['ENABLE_FTP'], 0, 1)
        self.sf['FTP_HOST']    = TextLine(self, grplay5, self.launch.pars['FTP_HOST'], 1, 0, 1)
        self.sf['FTP_PORT']    = TextLine(self, grplay5, self.launch.pars['FTP_PORT'], 1, 3, 1, QtGui.QIntValidator(0,1023))
        self.sf['FTP_USER']    = TextLine(self, grplay5, self.launch.pars['FTP_USER'], 2, 0, 1)
        self.sf['FTP_PASS']    = TextLine(self, grplay5, self.launch.pars['FTP_PASS'], 2, 3, 1)
        self.sf['FTP_DIR']     = TextLine(self, grplay5, self.launch.pars['FTP_DIR'], 3, 0, 1)
                
        # MAIL OPTIONS
        self.mailOptGrpBox  = QtGui.QGroupBox("Mail Options")
        vbox.addWidget(self.mailOptGrpBox)
        grplay3 = QtGui.QGridLayout()
        self.mailOptGrpBox.setLayout(grplay3)         
        self.sf['SEND_MAIL']   = CheckBoxLine(self, grplay3, self.launch.pars['SEND_MAIL'], 0, 1)
        self.sf['MAIL_ADDR']   = TextLine(self, grplay3, self.launch.pars['MAIL_ADDR'], 1, 0, 1)
        grplay3.setColumnStretch(2,1)
        self.sf['SMTP_SERV']   = TextLine(self, grplay3, self.launch.pars['SMTP_SERV'], 1, 3, 1)
        
    def buildButtonFrame(self, vbox):      
        # == Buttons Frame ==
        butframe = QtGui.QFrame()
        vbox.addWidget(butframe)
        butlayout = QtGui.QHBoxLayout(); butlayout.setContentsMargins(0,0,0,0)
        butframe.setLayout(butlayout)
        
        self.goButton = QtGui.QPushButton(self.tr("Go !!!"))
        butlayout.addWidget(self.goButton)
        self.connect(self.goButton, QtCore.SIGNAL("pressed()"), self.go)        
        
        self.stopButton = QtGui.QPushButton(self.tr("Stop !!!"))
        butlayout.addWidget(self.stopButton)
        self.connect(self.stopButton, QtCore.SIGNAL("pressed()"), self.interrupt)
        self.stopButton.setEnabled(False)
        #button = QtGui.QPushButton(self.tr("Pause ")); butlayout.addWidget(button)
        #self.connect(button, QtCore.SIGNAL("pressed()"), self.pause)
        butlayout.addStretch(1)
        
        '''
        button = QtGui.QPushButton(self.tr("LoadDefaults")) ; butlayout.addWidget(button)
        self.connect(button, QtCore.SIGNAL("pressed()"), self.loadDef)
        butlayout.addStretch(1)
        '''
        
        self.saveButton = QtGui.QPushButton(self.tr("Save")) 
        butlayout.addWidget(self.saveButton)
        self.connect(self.saveButton, QtCore.SIGNAL("pressed()"), self.save)
        
        self.quitButton = QtGui.QPushButton(self.tr("Quit")) 
        butlayout.addWidget(self.quitButton)
        self.connect(self.quitButton, QtCore.SIGNAL("pressed()"), self.quit)
        
    def guiEnable(self,boolVal):
        
        self.baseDirGrpBox.setEnabled(boolVal)
        self.launchGrpBox.setEnabled(boolVal)
        self.runOptGrpBox.setEnabled(boolVal)
        self.sgeOptGrpBox.setEnabled(boolVal)
        self.ftpOptGrpBox.setEnabled(boolVal)
        self.mailOptGrpBox.setEnabled(boolVal)
        
        self.goButton.setEnabled(boolVal)
        self.stopButton.setEnabled(not boolVal)
        self.saveButton.setEnabled(boolVal)
        self.quitButton.setEnabled(boolVal)
    #
    # ----------------------------------------------------------------------------------    
    
    def go(self):    
        print "Go pressed"
        
        # disable the gui modifications during run
        self.guiEnable(False)
        try:
            self.baseDir.savePars()     
            self.launch.savePars()  
            if self.launch.debug :
                self.launch.printPars()    
                                    
            self.process = QtCore.QProcess(self)
            self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
            self.process.setWorkingDirectory(self.baseDir.val)
            # evite de chercher a charger .pythonrc
            #env = self.process.processEnvironment()
            env = QtCore.QProcessEnvironment.systemEnvironment()
            env.remove('PYTHONSTARTUP')            
            # add mtfdir in the LD_LIBRARY_PATH (to allow process to find mt*.so...)
            if isUnix():
                mtfdir, mtfexe = os.path.split(self.launch.pars['EXEC_NAME'].val)          
                ldlp = mtfdir+':'+env.value('LD_LIBRARY_PATH','')
                #print "old LD_LIBRARY_PATH = ", env.value('LD_LIBRARY_PATH','')
                env.insert('LD_LIBRARY_PATH',ldlp)
                #print "new LD_LIBRARY_PATH = ", env.value('LD_LIBRARY_PATH','')

            self.process.setProcessEnvironment(env)   
            # gestion du nice sur le QProcess : pas arrive a faire marcher !!!
            #self.process.setPriority (self.launch.pars['NICE_VALUE'].val)  
            #pid = self.process.pid()  
            #print "QProcess pid : ",self.process.pid()  
            # 
            QtCore.QObject.connect(self.process, QtCore.SIGNAL("readyReadStandardOutput()"), self, QtCore.SLOT("readStdOutput()"))
            # launch.go() ...
            self.launch.go()    
            
        except Exception, e:
            #print e
            QtGui.QMessageBox.information(self, 'Error', str(e))     
        
        # re enable the gui modifications
        self.guiEnable(True)
        
    def interrupt(self):
        print "interrupt pressed"
        self.process.kill()
        print "interrupt done"
        
    # Boucle d'execution du Qprocess avec recuperation des events 
    def waitQProcessForFinish(self):
        while self.process.waitForFinished(1000):
            self.app.processEvents()                                
        self.process.waitForFinished(-1)
        self.app.processEvents()
            
        retcode = self.process.ExitStatus()
        
        print("Finished: " + str(retcode))            
        self.process.close()        
        return retcode                                
    
    def save(self):     
        print "Save pressed"
        self.baseDir.savePars()
        #self.launch.printPars()
        self.launch.savePars()   

    def quit(self):
        print "Quit pressed"   
        sys.exit()    
                  
    def updateWidgetsValues(self):
        self.launch.applyDependencies()
        if self.launch.debug :
            print "updateWidgetsValues"
        for var in self.sf:
            self.sf[var].setParamValue()
                
    def updateWidgetsVisibility(self):
        if self.launch.debug :
            print "updateWidgetsVisibility"
        # update enabled/disabled of options  
        self.launch.configActions()
        for var in self.sf:
            self.sf[var].setEnabled(self.launch.pars[var].enabled)       
        
    @QtCore.pyqtSlot()
    def readStdOutput(self): 
        out =    self.process.readAllStandardOutput()        
        '''
        if self.launch.outFile :
            self.launch.outFile.write(repr(out)) 
            self.launch.outFile.write("\n")                 
        '''
        out =  QtCore.QString(out)  
        '''
        if self.launch.outFile :
            self.launch.outFile.write(repr(out)) 
            self.launch.outFile.write("\n")                 
        ''' 
        out = out.replace('>>> >>> ... ... ... ... ... >>>','')        
        out = out.replace('>>> ','')
        out = out.replace('\r\n','\n')
        self.write(out)
        #self.console.append(QtCore.QString(out))
        '''
        self.console.moveCursor (QtGui.QTextCursor.End)
        self.console.insertPlainText (QtCore.QString(out))
        self.console.moveCursor (QtGui.QTextCursor.End)
        '''
        if self.launch.outFile :
            self.launch.outFile.write(out)
            
    def buildConsole(self):
        self.stdout, sys.stdout = sys.stdout, self
        self.buf=''
        self.console = QtGui.QTextEdit()
        self.console.setReadOnly(True)
        font = QtGui.QFont("Lucida", 9)
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self.console.setFont(font)
        self.console.setLineWrapMode(QtGui.QTextEdit.NoWrap)  
        self.console.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                
    def write(self, stuff):
        if '\n' in stuff:
            map( self.writeLine, stuff.split("\n") )
        else:
            self.buf += stuff 
        self.app.processEvents()
        
    def writeLine(self, stuff):
        if len(self.buf):
            stuff = self.buf + stuff
            self.buf=''
            self.console.append(stuff)
        else:
            if stuff != '':
                self.console.append(stuff)
        

def main():
    #define launcher
    launch = LaunchJob()
    if launch.debug :
        print "launch defined"
    # create gui    
    launchGui = LaunchGui(launch) 
    # opening Gui 
    launchGui.show()    
    # signal pour cloturer proprement l'application PyQt quand on ferme la fenetre
    launchGui.app.connect(launchGui.app, QtCore.SIGNAL("lastWindowClosed()"),launchGui.app,QtCore.SLOT("quit()"))
    print "ready."
    sys.exit(launchGui.app.exec_())

if __name__=="__main__":
    main()
