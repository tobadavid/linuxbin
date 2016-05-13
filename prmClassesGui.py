# -*- coding: latin-1; -*-
# $Id: prmClassesGui.py 2645 2016-05-12 06:29:38Z boman $
#
#
# Classe d'interface PyQt des prmClasses

import os,sys
from PyQt4 import QtCore, QtGui
import distutils.spawn
from prmClasses import *

#========================================================================================
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
        self.checkBox = QtGui.QCheckBox(self.param.key)
        self.checkBox.setToolTip(self.param.desc)       
        self.grpLayout.addWidget(self.checkBox,nrow,ncol) 
        #
        self.win.connect(self.checkBox, QtCore.SIGNAL("stateChanged(int)"), self.action)
        #
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
    #        
    def action(self):
        self.param.val = self.checkBox.isChecked()
        self.win.updateWidgetsVisibility()        
        self.win.updateWidgetsValues()               
    #
    def setParamValue(self):
        self.checkBox.setChecked(self.param.val)
    #
    def setEnabled(self, enable):
        self.checkBox.setEnabled(enable)                 
#========================================================================================
class TextLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol, ncolSpan=1, validator = None):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        #
        self.label = QtGui.QLabel(self.win.tr(self.param.key)) 
        self.grpLayout.addWidget(self.label,nrow,ncol)
        self.lineEdt = QtGui.QLineEdit()
        self.lineEdt.setToolTip(self.param.desc)  
        self.lineEdt.setValidator(validator)   
        self.grpLayout.addWidget(self.lineEdt,nrow,ncol+1, 1, ncol+ncolSpan)
        #
        self.win.connect(self.lineEdt, QtCore.SIGNAL("editingFinished()"), self.action)
        # 
        self.setParamValue()
        self.setEnabled(self.param.enabled)
    #
    def action(self):
        #opt.val=line.text().data() # je ne comprend pas pourquoi une QString n'a pas de data ???
        self.param.val = self.lineEdt.text().toLatin1().data()
        #print opt.key,'=',opt.val
        # update widgets visibility according to enable/disable        
        self.win.updateWidgetsVisibility()        
        self.win.updateWidgetsValues()       
    #         
    def setParamValue(self):
        self.lineEdt.setText(self.win.tr(self.param.val))
    #
    def setEnabled(self, enable):
        self.lineEdt.setEnabled(enable)        
#========================================================================================
class PathLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol, ncolSpan=1):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        #label
        self.label = QtGui.QLabel(self.win.tr(self.param.key)) 
        self.grpLayout.addWidget(self.label,nrow,ncol)
        #LineEdt
        self.lineEdt = QtGui.QLineEdit()
        self.lineEdt.setToolTip(self.param.desc) 
        self.grpLayout.addWidget(self.lineEdt,nrow,ncol+1, 1, ncol+ncolSpan)  
        self.win.connect(self.lineEdt, QtCore.SIGNAL("editingFinished()"), self.edtAction)    
        #Button
        self.button = QtGui.QPushButton(self.win.tr("...")) 
        self.button.setMaximumSize(QtCore.QSize(20,999999))
        self.grpLayout.addWidget(self.button,nrow,ncol+ncolSpan+1)
        self.win.connect(self.button, QtCore.SIGNAL("pressed()"), self.btAction)
        #        
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
        self.checkValidity()
    #
    def edtAction(self):
        file = self.lineEdt.text()
        self.action(file)   
    #
    def btAction(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self.win, "Choose %s directory" % self.param.key, self.param.val)
        self.action(dir)
    #
    def action(self, dir):
        if dir: 
            self.param.val = dir.toLatin1().data().replace('/',os.sep)
            self.lineEdt.setText(dir)
        #print self.param.key,'=',self.param.val   
        # update widgets visibility according to enable/disable
        self.checkValidity()
        self.win.updateWidgetsVisibility()
        self.win.updateWidgetsValues()       
    #    
    def checkValidity(self):
        palette = self.lineEdt.palette()
        if os.path.isdir(self.param.val):                        
            #palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
            palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
            #self.palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(50, 50, 50))
        else :    
            #palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 0, 0))
            palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(255, 0, 0))
            palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, QtGui.QColor(255, 0, 0))
        self.lineEdt.setPalette(palette)
    #
    def setParamValue(self):
        self.lineEdt.setText(self.win.tr(self.param.val))
    #
    def setEnabled(self, enable):
        self.lineEdt.setEnabled(enable)
        self.button.setEnabled(enable)
#========================================================================================               
class FileLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, _fileType, nrow, ncol, ncolSpan=1):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        
        self.fileType   = _fileType  
        self.label      = QtGui.QLabel(self.win.tr(self.param.key))
        self.grpLayout.addWidget(self.label,nrow,ncol)
        # lineEdt
        self.lineEdt    = QtGui.QLineEdit()
        self.lineEdt.setToolTip(self.param.desc)  
        self.grpLayout.addWidget(self.lineEdt, nrow, ncol+1, 1, ncol+ncolSpan)
        self.win.connect(self.lineEdt, QtCore.SIGNAL("editingFinished()"), self.edtAction)                  
        # button
        self.button     = QtGui.QPushButton(self.win.tr("..."))                 
        self.button.setMaximumSize(QtCore.QSize(20,999999))
        self.grpLayout.addWidget(self.button,nrow,ncol+5)
        self.win.connect(self.button, QtCore.SIGNAL("pressed()"), self.btAction)
        #        
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
        self.checkValidity()
        #         
    def edtAction(self):
        file = self.lineEdt.text()
        self.action(file)   
    def btAction(self):
        file = QtGui.QFileDialog.getOpenFileName(self.win, "Choose %s file" % self.param.key, self.param.val, self.fileType)
        self.action(file)
    def action(self, file):
        if file: 
            self.param.val = file.toLatin1().data().replace('/',os.sep)
            self.lineEdt.setText(file)
        print self.param.key,'=',self.param.val
        self.checkValidity()
        # update widgets visibility according to enable/disable
        self.win.updateWidgetsVisibility()    
        self.win.updateWidgetsValues()                           
    def checkValidity(self):
        #print "FileLine:checkValidity : ",self.param.val        
        if os.path.isfile(self.param.val):  # White bg              
            bgCol  =   QtGui.QColor(255, 255, 255)    
        else :  #redBg       
            bgCol  =   QtGui.QColor(255, 0, 0)    
        # Apply the new color in palette    
        palette = self.lineEdt.palette()
        palette.setColor(QtGui.QPalette.Base, bgCol)
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
            bgCol  =   QtGui.QColor(255, 255, 255)                   
        elif distutils.spawn.find_executable(os.path.splitext(f)[0]):  # *.cmd pas reconnu comme exe !!!
            #print "find_executable in path"          
            bgCol  =   QtGui.QColor(0, 255, 0)               
        else :  #redBg                   
            #print "not found"          
            bgCol  =   QtGui.QColor(255, 0, 0)    
            
        palette = self.lineEdt.palette()
        palette.setColor(QtGui.QPalette.Base, bgCol)    
        self.lineEdt.setPalette(palette)       
#========================================================================================        
class MultiPMRLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol, ncolSpan=1):    
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        # label
        self.label = QtGui.QLabel(self.win.tr(self.param.key))         
        self.grpLayout.addWidget(self.label,nrow,ncol) 
        # comboBox       
        self.comboBox = QtGui.QComboBox()
        for choice in self.param.vals: 
            self.comboBox.addItem(choice)  
        self.comboBox.setToolTip(self.param.desc)
        self.grpLayout.addWidget(self.comboBox, nrow, ncol+1, 1, ncolSpan)        
        self.win.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.action)
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
    #        
    def action(self):
        self.param.val = self.comboBox.currentText().toLatin1().data()
        print self.param.val
        self.win.updateWidgetsVisibility()
        self.win.updateWidgetsValues()       
    #
    def setParamValue(self):    
        idx = self.comboBox.findText(self.param.val)
        self.comboBox.setCurrentIndex(idx)        
    #
    def setEnabled(self, enable):
        self.comboBox.setEnabled(enable)
#========================================================================================                
class MultiPathLine(PRMLine):   
    def __init__(self, _win, _grpLayout, _prm, nrow, ncol, ncolSpan=1):        
        PRMLine.__init__(self, _win, _grpLayout, _prm)
        #label
        self.label = QtGui.QLabel(self.win.tr(self.param.key)) 
        self.grpLayout.addWidget(self.label,nrow,ncol)        
        # comboBox       
        self.comboBox = QtGui.QComboBox()
        for choice in self.param.vals: 
            self.comboBox.addItem(choice)  
        self.comboBox.setToolTip(self.param.desc)
        self.comboBox.setEditable(True)
        self.comboBox.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred) #Expanding)
        self.grpLayout.addWidget(self.comboBox, nrow, ncol+1, 1, ncolSpan)        
        #        
        self.win.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.cbIndexChangeAction) 
        self.win.connect(self.comboBox, QtCore.SIGNAL("editingFinished()"), self.cbIndexChangeAction)                   
        #self.win.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(const QString & )"), self.cbIndexChangeAction) 
        # edit text changed : trop sensible : change des 1 lettre modifiee => utilisation via currentIndexChanged
        # self.win.connect(self.comboBox, QtCore.SIGNAL("editTextChanged( const QString & )"), self.cbEditTextAction) 
        #Button
        self.button = QtGui.QPushButton(self.win.tr("...")) 
        self.button.setMaximumSize(QtCore.QSize(20,999999))
        self.grpLayout.addWidget(self.button,nrow,ncol+ncolSpan+1)
        self.win.connect(self.button, QtCore.SIGNAL("pressed()"), self.buttonAction)
        #        
        self.setParamValue()  
        self.setEnabled(self.param.enabled)
        self.checkValidity()
    #
    def cbIndexChangeAction(self):       
        dir = self.comboBox.currentText() 
        val = dir.toLatin1().data().replace('/',os.sep)
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
        dir = QtGui.QFileDialog.getExistingDirectory(self.win, "Choose %s directory" % self.param.key, self.param.val)
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
        #    
    def checkValidity(self):
        palette = self.comboBox.palette()
        if os.path.isdir(self.param.val):                        
            palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
            #self.palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(50, 50, 50))
        else :    
            palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, QtGui.QColor(255, 0, 0))
        self.comboBox.setPalette(palette)
                
    def postAction(self): # necessary for derivation
        self.checkValidity()
        # update widgets visibility according to enable/disable
        self.win.updateWidgetsVisibility()
        self.win.updateWidgetsValues()       
        
    def setParamValue(self):    
        idx = self.comboBox.findText(self.param.val)
        self.comboBox.setCurrentIndex(idx)        
    def setEnabled(self, enable):
        self.comboBox.setEnabled(enable)     
#========================================================================================        
class BaseMultiDirPathLine(MultiPathLine): 
    def postAction(self):
        self.checkValidity()
        # specific changeBaseDir                
        print "new base dir =",self.param.val   
        try :
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
            file.write("if %s not in self.vals : " % repr(val) ) 
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