# -*- coding: latin-1; -*-
# $Id: prmClassesGui.py 2645 2016-05-12 06:29:38Z boman $
#
#
# Classe d'interface PyQt des prmClasses

import os,sys

## Qt ##
foundQt=0
coding='latin-1'
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

import distutils.spawn
from prmClasses import *

#========================================================================================

class PRMLine():
    def __init__(self, _win, _grpLayout, _prm):
        self.win        = _win
        self.grpLayout  = _grpLayout
        self.param      = _prm
        

#========================================================================================
class CheckBoxLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        self.checkBox = QCheckBox(self.param.key)
        self.checkBox.setToolTip(self.param.desc)       
        self.grpLayout.addWidget(self.checkBox,nrow,ncol) 

        self.checkBox.stateChanged.connect(self.action)

        self.setParamValue()  
        self.setEnabled(self.param.enabled)
       
    def action(self):
        self.param.val = self.checkBox.isChecked()
        self.win.updateWidgetsVisibility()        
        self.win.updateWidgetsValues()               

    def setParamValue(self):
        self.checkBox.setChecked(self.param.val)

    def setEnabled(self, enable):
        self.checkBox.setEnabled(enable) 
        
                        
#========================================================================================
class TextLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol, ncolSpan=1, validator = None):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)

        self.label = QLabel(self.win.tr(self.param.key)) 
        self.grpLayout.addWidget(self.label,nrow,ncol)
        self.lineEdt = QLineEdit()
        self.lineEdt.setToolTip(self.param.desc)  
        self.lineEdt.setValidator(validator)   
        self.grpLayout.addWidget(self.lineEdt,nrow,ncol+1, 1, ncol+ncolSpan)

        self.lineEdt.editingFinished.connect(self.action)

        self.setParamValue()
        self.setEnabled(self.param.enabled)

    def action(self):
        if foundQt==4:
            self.param.val = self.lineEdt.text().toLatin1().data()
        else:
            self.param.val = self.lineEdt.text().encode(coding)
        #print opt.key,'=',opt.val
        # update widgets visibility according to enable/disable        
        self.win.updateWidgetsVisibility()        
        self.win.updateWidgetsValues()       
        
    def setParamValue(self):
        self.lineEdt.setText(self.win.tr(self.param.val))

    def setEnabled(self, enable):
        self.lineEdt.setEnabled(enable) 
        
               
#========================================================================================
class PathLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol, ncolSpan=1):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        #label
        self.label = QLabel(self.win.tr(self.param.key)) 
        self.grpLayout.addWidget(self.label,nrow,ncol)
        #LineEdt
        self.lineEdt = QLineEdit()
        self.lineEdt.setToolTip(self.param.desc) 
        self.grpLayout.addWidget(self.lineEdt,nrow,ncol+1, 1, ncol+ncolSpan)  
        self.lineEdt.editingFinished.connect(self.edtAction)  
        #Button
        self.button = QPushButton(self.win.tr("...")) 
        self.button.setMaximumSize(QSize(20,999999))
        self.grpLayout.addWidget(self.button,nrow,ncol+ncolSpan+1)
        self.button.pressed.connect(self.btAction)
      
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
        self.checkValidity()

    def edtAction(self):
        file = self.lineEdt.text()
        self.action(file)   

    def btAction(self):
        dir = QFileDialog.getExistingDirectory(self.win, "Choose %s directory" % self.param.key, self.param.val)
        self.action(dir)

    def action(self, dir):
        if dir:            
            if foundQt==4:
                self.param.val = dir.toLatin1().data().replace('/',os.sep)
                self.lineEdt.setText(dir)
            else:
                #print "PathLine.action:dir=", dir
                self.param.val = dir.encode(coding).replace('/',os.sep)
                self.lineEdt.setText(self.param.val.decode(coding))
        #print self.param.key,'=',self.param.val   
        # update widgets visibility according to enable/disable
        self.checkValidity()
        self.win.updateWidgetsVisibility()
        self.win.updateWidgetsValues()       

    def checkValidity(self):
        palette = self.lineEdt.palette()
        if os.path.isdir(self.param.val):                        
            #palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.Active, QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.Inactive, QPalette.Base, QColor(255, 255, 255))
            #self.palette.setColor(QPalette.Active, QPalette.Base, QColor(50, 50, 50))
        else:    
            #palette.setColor(QPalette.Base, QColor(255, 0, 0))
            palette.setColor(QPalette.Active, QPalette.Base, QColor(255, 0, 0))
            palette.setColor(QPalette.Inactive, QPalette.Base, QColor(255, 0, 0))
        self.lineEdt.setPalette(palette)

    def setParamValue(self):
        self.lineEdt.setText(self.win.tr(self.param.val))

    def setEnabled(self, enable):
        self.lineEdt.setEnabled(enable)
        self.button.setEnabled(enable)
        
        
#========================================================================================               
class FileLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, _fileType, nrow, ncol, ncolSpan=1):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        
        self.fileType   = _fileType  
        self.label      = QLabel(self.win.tr(self.param.key))
        self.grpLayout.addWidget(self.label,nrow,ncol)
        # lineEdt
        self.lineEdt    = QLineEdit()
        self.lineEdt.setToolTip(self.param.desc)  
        self.grpLayout.addWidget(self.lineEdt, nrow, ncol+1, 1, ncol+ncolSpan)
        self.lineEdt.editingFinished.connect(self.edtAction)               
        # button
        self.button     = QPushButton(self.win.tr("..."))                 
        self.button.setMaximumSize(QSize(20,999999))
        self.grpLayout.addWidget(self.button,nrow,ncol+5)
        self.button.pressed.connect(self.btAction)
     
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
        self.checkValidity()
   
    def edtAction(self):
        file = self.lineEdt.text()
        self.action(file)   
        
    def btAction(self):
        file = QFileDialog.getOpenFileName(self.win, "Choose %s file" % self.param.key, self.param.val, self.fileType)
        if foundQt>4: file=file[0] # en PyQt5 retourne (filename, filter)
        self.action(file)
        
    def action(self, file):
        if file: 
            if foundQt==4:
                self.param.val = file.toLatin1().data().replace('/', os.sep)
                self.lineEdt.setText(file)
            else:                
                self.param.val = file.encode(coding).replace('/', os.sep)
                self.lineEdt.setText(self.param.val.decode(coding))
        #print "FileLine.action:", self.param.key,'=',self.param.val
        self.checkValidity()
        # update widgets visibility according to enable/disable
        self.win.updateWidgetsVisibility()    
        self.win.updateWidgetsValues()
                                   
    def checkValidity(self):
        #print "FileLine:checkValidity : ",self.param.val        
        if os.path.isfile(self.param.val):  # White bg              
            bgCol  =   QColor(255, 255, 255)    
        else:  #redBg       
            bgCol  =   QColor(255, 0, 0)    
        # Apply the new color in palette    
        palette = self.lineEdt.palette()
        palette.setColor(QPalette.Base, bgCol)
        self.lineEdt.setPalette(palette) 
              
    def setParamValue(self):
        self.lineEdt.setText(self.win.tr(self.param.val))
        
    def setEnabled(self, enable):
        self.lineEdt.setEnabled(enable)
        self.button.setEnabled(enable)
        
        
#========================================================================================               
class ExeFileLine(FileLine):   
    def checkValidity(self):
        #print "ExeFileLine:checkValidity : ",self.param.val  
        f     = self.param.val
        if os.path.isfile(f):  # White bg    
            #print "isFile"          
            bgCol  =   QColor(255, 255, 255)                   
        elif distutils.spawn.find_executable(os.path.splitext(f)[0]):  # *.cmd pas reconnu comme exe !!!
            #print "find_executable in path"          
            bgCol  =   QColor(0, 255, 0)               
        else:  #redBg                   
            #print "not found"          
            bgCol  =   QColor(255, 0, 0)    
            
        palette = self.lineEdt.palette()
        palette.setColor(QPalette.Base, bgCol)    
        self.lineEdt.setPalette(palette)
        
        
#========================================================================================        
class MultiPMRLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol, ncolSpan=1):    
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        # label
        self.label = QLabel(self.win.tr(self.param.key))         
        self.grpLayout.addWidget(self.label,nrow,ncol) 
        # comboBox       
        self.comboBox = QComboBox()
        for choice in self.param.vals: 
            self.comboBox.addItem(choice)  
        self.comboBox.setToolTip(self.param.desc)
        self.grpLayout.addWidget(self.comboBox, nrow, ncol+1, 1, ncolSpan)
        self.comboBox.currentIndexChanged.connect(self.action)
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
   
    def action(self):
        if foundQt==4:
            self.param.val = self.comboBox.currentText().toLatin1().data()
        else:
            self.param.val = self.comboBox.currentText().encode(coding)
        #print self.param.val
        self.win.updateWidgetsVisibility()
        self.win.updateWidgetsValues()       

    def setParamValue(self):    
        idx = self.comboBox.findText(self.param.val)
        self.comboBox.setCurrentIndex(idx)        

    def setEnabled(self, enable):
        self.comboBox.setEnabled(enable)
        
#========================================================================================                
class MultiPathLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol, ncolSpan=1):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        #label
        self.label = QLabel(self.win.tr(self.param.key)) 
        self.grpLayout.addWidget(self.label,nrow,ncol)        
        # comboBox       
        self.comboBox = QComboBox()
        for choice in self.param.vals: 
            self.comboBox.addItem(choice)  
        self.comboBox.setToolTip(self.param.desc)
        self.comboBox.setEditable(True)
        self.comboBox.setInsertPolicy(QComboBox.InsertAtTop)
        self.comboBox.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred) #Expanding)
        self.grpLayout.addWidget(self.comboBox, nrow, ncol+1, 1, ncolSpan)        
    
        self.comboBox.currentIndexChanged.connect(self.cbIndexChangeAction)            
        #self.comboBox.editingFinished.connect(self.cbIndexChangeAction) 
                
        #Button
        self.button = QPushButton(self.win.tr("...")) 
        self.button.setMaximumSize(QSize(20,999999))
        self.grpLayout.addWidget(self.button,nrow,ncol+ncolSpan+1)
        self.button.pressed.connect(self.buttonAction)
    
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
        self.checkValidity()

    def cbIndexChangeAction(self):       
        dir = self.comboBox.currentText()
        if foundQt==4:
            val = dir.toLatin1().data().replace('/',os.sep)
        else:
            #print "cbIndexChangeAction:dir=",dir
            val = dir.encode(coding).replace('/',os.sep)
        self.param.val = val
        if val in self.param.vals: # bidouille pour que la nouvelle valeur soit unique et toujours en premiere position
            self.param.vals.remove(val)
        self.param.vals.insert(0,val)    
        self.postAction()
    
    ''' trop sensible : le signal est envoye a chaque lettre modifiee & currentIndex change active seulement au return
    def cbEditTextAction(self, ddir):        
        dir = self.comboBox.currentText()                
        print "cbEditTextAction :  ddir = %s"%ddir
        print "cbEditTextAction : new dir = %s"%dir
        self.setDir(dir)    
    '''
    
    def buttonAction(self):   
        dir = QFileDialog.getExistingDirectory(self.win, "Choose %s directory" % self.param.key, self.param.val)
        #self.setDir(dir)
        if dir: 
            # managing comboBox
            idx = self.comboBox.findData(dir)
            if idx != -1:
                self.comboBox.removeItem(idx)
            self.comboBox.insertItem(0,dir) # : fait appel au signal currentIndexChanged => le reste est dans cbIndexChanged
            self.comboBox.setCurrentIndex(0)   
            # managing parametricJob parameters
        self.postAction()        

    def checkValidity(self):
        palette = self.comboBox.palette()
        if os.path.isdir(self.param.val):                        
            palette.setColor(QPalette.Active, QPalette.Base, QColor(255, 255, 255))
            #self.palette.setColor(QPalette.Active, QPalette.Base, QColor(50, 50, 50))
        else:    
            palette.setColor(QPalette.Active, QPalette.Base, QColor(255, 0, 0))
        self.comboBox.setPalette(palette)
                
    def postAction(self): # necessary for derivation
        self.checkValidity()
        # update widgets visibility according to enable/disable
        self.win.updateWidgetsVisibility()
        self.win.updateWidgetsValues()       
        
    def setParamValue(self):    
        idx = self.comboBox.findText(self.param.val.decode(coding))
        self.comboBox.setCurrentIndex(idx)   
             
    def setEnabled(self, enable):
        self.comboBox.setEnabled(enable)   
        
          
#========================================================================================        
class BaseMultiDirPathLine(MultiPathLine): 
    def postAction(self):
        self.checkValidity()
        # specific changeBaseDir                
        print "new base dir =",self.param.val   
        try:
            #self.win.launch.printPars()
            os.chdir(self.param.val)
            self.win.launch.loadPars()
            #self.win.launch.printPars()
        except Exception, e:
            print "change of base dir failed on error : "
            print e
        # update enabled/disabled of options     
        self.win.updateWidgetsVisibility()
        self.win.updateWidgetsValues()                 


#========================================================================================        
class BaseDirMultiPRM(MultiPRM):
    def __init__(self, set, cfgfile):
        self.homeDir = os.getcwd()
        set = {}
        self.cfgfile = cfgfile
        key, desc, vals, defval = self.getDefaultValues()
        MultiPRM.__init__(self, set, key, desc, vals, defval)
        self.loadPars()
   
    def getDefaultValues(self):        
        key  = 'BASE_DIR'
        desc = 'Base Directory'
        vals = [os.getcwd()]
        defval = os.getcwd()
        return key, desc, vals, defval
        
    def printPars(self):
        for k,v in self.pars.items():
            print ("pars['%s'].val=%s\n" % (k,repr(v.val)) )
            
    def savePars(self):
        fname = os.path.join(self.homeDir, self.cfgfile)
        file = open(fname,"w")
        for val in self.vals:
            file.write("if %s not in self.vals: " % repr(val) ) 
            file.write("\tself.vals.append(%s)\n" % repr(val) )                    
        file.write("self.val=%s\n" % repr(self.val))
        file.close()
            
    def loadPars(self):
        try:
            fname = os.path.join(self.homeDir, self.cfgfile)
            file = open(fname,"r")
            if file:
                cmds = file.readlines()
                for cmd in cmds:
                    try:
                        exec cmd
                    except:
                        pass
                file.close()
        except:
            pass    
     