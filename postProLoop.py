#!/usr/bin/env python
# -*- coding: latin-1; -*-
# $Id: externalProgramPath.py 2645 2016-05-12 06:29:38Z boman $
#
#
# Define externals program path according to local configuration
# 
from prmClasses import *
import os, os.path, distutils.spawn, time, sys
import externalProgramPath
# Variable globale
import threading
matlock = threading.Lock()  # un seul matlab a la fois (merdouille avec le R2009a sous windows)

#------------------------------------------------------------------------------------
    
'''
try:
    import toolbox.matlab as matlab    
    import toolbox.latex as latex
    import toolbox.ghostScript as ghostScript
except:
    oo_meta_path = os.path.abspath('..'+os.sep+'oo_meta')
    sys.path.append(oo_meta_path)
    import toolbox.matlab as matlab    
    import toolbox.latex as latex
    import toolbox.ghostScript as ghostScript
'''    
    

class PostProLoop(PRMSet):  
    def __init__(self,_verb=False):                     
        fname = 'postProLoop.cfg'
        PRMSet.__init__(self, fname, _verb)
        
    def __getitem__(self, key):
        return self.pars[key].val
        
    def loadPaths(self):   
        home = os.path.expanduser("~")
        loc=os.path.abspath('.')
        return  [home,loc]
        
    def savePath(self):    
        home = os.path.expanduser("~")
        return home                
    
    def setDefaultPars(self):
        if len(self.pars)!=0:
            return     
        # load progs 
        progs = externalProgramPath.ExtProgs()
        # 
        TextPRM (self.pars, 'DIRNAME',            'BaseDir on wich running Post-Operation', './workspace/MyTestDir')        
        YesNoPRM(self.pars, 'MULTITEST',          'Loop on all existing subDirectories', False)
        TextPRM (self.pars, 'DIRWILDCARD',        'WildCard on subDirs Name',              '*')
        # Matlab
        YesNoPRM(self.pars, 'MATLABRUN',          'Run Matlab post-pro',                 False)
        TextPRM (self.pars, 'MATLABEXE',          'Path To Matlab Exe',                  progs['MATLAB'])
        TextPRM (self.pars, 'MATLABCMD',          'Matlab Command (script called)',         '')
        TextPRM (self.pars, 'MATLABPATH',         'Path to Matlab scripts',                 '')
        TextPRM (self.pars, 'MATLABREQUEST',     'Requested file to run Matlab script',    'parameters.m') #'result.mat', ...
        # GS
        YesNoPRM(self.pars, 'GSRUN',              'Run GS on Eps Files',                     False)        
        TextPRM (self.pars, 'GSEXE',              'Path To Matlab Exe',                  progs['GHOSTSCRIPT'])
        MultiPRM(self.pars, 'GSOUTPUTFORMAT',     'GS Output format', ["png256", "bmp256"], "png256")
        TextPRM (self.pars, 'GSDEFINITION',       'GS Output definition',      "300")   
        TextPRM (self.pars, 'GSREQUEST',          'Requested file to run GhostScript',      "*.eps")   
        # Latex
        YesNoPRM(self.pars, 'LATEXRUN',           'Run the build latex file post-pro',        False)
        TextPRM(self.pars,  'LATEXCMD',           'Script to call to build latex file',       '')       
        #TextPRM(self.pars,  'LATEXCMD',           'Script to call to build latex file',       '')       
        TextPRM(self.pars,  'LATEXREQUEST',       'Script to call to build latex file',       '')                
        # 
        PRMAction(self.actions, 'a', self.pars['DIRNAME']) 
        PRMAction(self.actions, 'b', self.pars['MULTITEST']) 
        PRMAction(self.actions, 'c', self.pars['DIRWILDCARD']) 
        #
        NoAction(self.actions)
        PRMAction(self.actions, 'f', self.pars['MATLABRUN']) 
        PRMAction(self.actions, 'g', self.pars['MATLABEXE']) 
        PRMAction(self.actions, 'h', self.pars['MATLABCMD']) 
        PRMAction(self.actions, 'i', self.pars['MATLABPATH']) 
        PRMAction(self.actions, 'j', self.pars['MATLABREQUEST']) 
        NoAction(self.actions)
        PRMAction(self.actions, 'k', self.pars['GSRUN']) 
        PRMAction(self.actions, 'l', self.pars['GSEXE']) 
        PRMAction(self.actions, 'm', self.pars['GSOUTPUTFORMAT']) 
        PRMAction(self.actions, 'n', self.pars['GSDEFINITION']) 
        PRMAction(self.actions, 'o', self.pars['GSREQUEST']) 
        NoAction(self.actions)
        PRMAction(self.actions, 'p', self.pars['LATEXRUN']) 
        PRMAction(self.actions, 'q', self.pars['LATEXCMD']) 
        PRMAction(self.actions, 'r', self.pars['LATEXREQUEST']) 
        NoAction  (self.actions) 
        GoAction  (self.actions, 'G') 
        SaveAction(self.actions, 'S') 
        QuitAction(self.actions, 'Q')
                        
    def configActions(self):        
        self.pars['DIRWILDCARD'].enable(self.pars['MULTITEST'].val==True)
        self.pars['MATLABCMD'].enable(self.pars['MATLABRUN'].val==True)
        self.pars['MATLABEXE'].enable(self.pars['MATLABRUN'].val==True)
        self.pars['MATLABPATH'].enable(self.pars['MATLABRUN'].val==True)
        self.pars['MATLABREQUEST'].enable(self.pars['MATLABRUN'].val==True)
        self.pars['GSEXE'].enable(self.pars['GSRUN'].val==True)
        self.pars['GSOUTPUTFORMAT'].enable(self.pars['GSRUN'].val==True)
        self.pars['GSDEFINITION'].enable(self.pars['GSRUN'].val==True)
        self.pars['GSREQUEST'].enable(self.pars['GSRUN'].val==True)
        self.pars['LATEXCMD'].enable(self.pars['LATEXRUN'].val==True)          
        self.pars['LATEXREQUEST'].enable(self.pars['LATEXRUN'].val==True)          
            
            
    def checkValidity(self, key):
        '''
        if distutils.spawn.find_executable(os.path.splitext(self.pars[key].val)[0]) :
            return True
        else :
            print "%s is not found (%s)...."%self.pars[key].val
            print "\t Check installation and accessibility..."        
            print "\t Use 'externalProgramPathGui' to define the full program path (recommanded)" 
            print "\t or add %s in your user path (not recommanded)"%key
            return False        
        '''
        return true
    
    def go(self):                  
        # change to workingDirectory
        baseDir = os.getcwd()
        os.chdir(self.pars['DIRNAME'].val)
        
        if self.pars['MULTITEST'].val == True:
            self.loopOnDirTree(os.path.abspath('.'))
        else:
            self.execInDir()        
        # back to source directory
        os.chdir(baseDir)
        
    def loopOnDirTree(self, wDir):
        # change to workingDirectory
        print "loopOnDirTree running on ", wDir
        oldDir = os.getcwd()
        os.chdir(wDir)
        # loop on dir 
        ld = glob.glob(self.pars['DIRWILDCARD'].val)
        for file in ld :
            if os.path.isdir(file) :
                self.loopOnDirTree(file)
                
        # finished loop on dir => execute ...
        self.execInDir()
    
        # back to source directory
        os.chdir(oldDir)

    def execInDir(self):
        print "execInDir running in ", os.path.abspath('.')
        if self.pars['MATLABRUN'].val and os.path.exists(self.pars['MATLABREQUEST'].val):
            print "launch matlab..."
            out = execMatlabScript(self.pars['MATLABEXE'].val, self.pars['MATLABCMD'].val , self.pars['MATLABPATH'].val)
            #out = matlab.execMatlabScript(self.pars['MATLABCMD'].val , self.pars['MATLABPATH'].val)
            print "matlab done"
            
        #print "os.path.exists(self.pars['GSREQUEST'].val) = ", os.path.exists(self.pars['GSREQUEST'].val)
        #print "glob.glob(self.pars['GSREQUEST'].val) = ", glob.glob(self.pars['GSREQUEST'].val)
        #print "len(glob.glob(self.pars['GSREQUEST'].val)) = ", len(glob.glob(self.pars['GSREQUEST'].val))
        if self.pars['GSRUN'].val and len(glob.glob(self.pars['GSREQUEST'].val)) > 0:
            print "launch Ghostscript translation of eps files..."
            #execGhostScriptPostPro(device='png256', outExt='png',res=300)
            out = execGhostScriptPostPro(self.pars['GSEXE'].val ,self.pars['GSOUTPUTFORMAT'].val , 'png', int(self.pars['GSDEFINITION'].val))
            #out = ghostScript.execGhostScriptPostPro(self.pars['GSOUTPUTFORMAT'].val , 'png', int(self.pars['GSDEFINITION'].val))
            print "Ghostscript  done "
            
        if self.pars['LATEXRUN'].val and os.path.exists(self.pars['LATEXREQUEST'].val):
            print "launch latex building file ..."            
            print "NOT IMPLEMENTED YIET "
            #out = latex.execMatlabScript(self.pars['MATLABCMD'].val , self.pars['MATLABPATH'].val)
            print "latex building file done "
              
#=================================================================================
#================================================================================= 
def execMatlabScript(matlabExe, matlabCmd, mFilePath=None):
    tim0 = time.time()
    print "entering MatlabPostPro compute"                       
    inirep = os.getcwd()
    print "inirep = ", inirep
    moutfile = os.path.abspath(os.path.join("matlab.log"))
    print "moutfile = ",moutfile
    
    mCmd = ""
    if mFilePath:
        print "mFilePath = ",mFilePath
        mCmd = mCmd + "addpath('%s'); " %mFilePath        
    mCmd = mCmd + "cd '%s'; "%inirep
    mCmd = mCmd + matlabCmd
    print "mCmd = ", mCmd
    if isUnix():
        cmd = '"%s" -nodisplay -logfile "%s" -r "%s; quit" > pipo 2>&1' % (matlabExe, moutfile, mCmd)
    else:
        cmd = '"%s"  -automation -noFigureWindows -nodesktop -wait  -logfile "%s" -r "%s; quit"' % (matlabExe, moutfile, mCmd) # work
    print 'complete Matlab subprocess command : ', cmd

    # acquire matlock
    matlock.acquire()
    try :
        print "Running Matlab..."                       
        import subprocess  
        matlabProcess = subprocess.call(cmd, shell=True)                
        print "Running Matlab... Done" 
        a = 1.0
    except :
        # fonction objectif doit retourner un double
        print "problem during matlab run"
        a = 0.0        
    # release matlock    
    matlock.release()                
    print " matlab time = %d sec" %(time.time()-tim0)         
    return a
#=================================================================================
#=================================================================================

def execGhostScriptPostPro(gsExe, device='png256', outExt='png',res=300):        
    import subprocess, os, time
    tim0 = time.time()    
    fileOut = open('gsOut.txt', 'w')
    # fonction objectif doit retourner un double
    a = 0
    try:    
        ld = glob.glob('*.eps')       
        for file in ld:
            [base,ext] = os.path.splitext(file)
            cmd = '"%s" -dSAFER -dBATCH -dNOPAUSE -dEPSCrop -r%d -sDEVICE=%s -sOutputFile=%s.%s %s'%(gsExe, res, device, base, outExt, file)
            subprocess.call(cmd, stdout=fileOut, stderr=subprocess.STDOUT, shell=True)       
            a = a+1                       
    except:
        print "problem during ghostScript run"
        a = 0.0                                
    fileOut.write("\nexecGhostScriptPostPro done in %d sec\n"%(time.time()-tim0))
    fileOut.close()         
    print "execGhostScriptPostPro : %d files translated in %d sec"%(a, (time.time()-tim0))                                               
    return a
    
#------------------------------------------------------------------------------------

#=================================================================================
#=================================================================================

#=================================================================================
#=================================================================================


def main():
    postProLoop = PostProLoop() #verb=True)
    postProLoop.configActions()
    postProLoop.menu()


if __name__ == "__main__":

    try:
        import signal  
        signal.signal(signal.SIGBREAK, sigbreak);
    except:
        pass
    main()
