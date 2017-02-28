#!/usr/bin/env python
# -*- coding: latin-1; -*-
#
# Script "launch.py": aide au lancement d'un job Metafor

import sys, os, os.path, subprocess
import shutil, socket, platform, glob, fnmatch, re
import datetime, tarfile, signal 

from parametricJob import *
from subprocess import *   # RB subprocess deja importe + haut??

class LaunchJob(ParametricJob):
    def __init__(self, _jobId=''):
        self.debug = False
        self.jobId=_jobId
        cfgfile="launch%s.cfg"%self.jobId
        ParametricJob.__init__(self, cfgfile)
        self.loadPars()
        # gestion des dépendances entre paramètres (restart single => restart step no)
        self.applyDependencies()   
        # liens vers launchGui (lorsque lancé par ce biais pour interaction)
        self.launchGui = None
        self.outFile   = None

    def setLaunchGui(self, launchGui) :
        self.launchGui = launchGui
        
    def setDefaultPars(self):
        if len(self.pars)!=0:
            return
        YesNoPRM(self.pars, 'SEND_MAIL',    'send emails when simulations are over', False)
        TextPRM(self.pars,  'MAIL_ADDR',    'e-mail address (reports)', os.getenv('USER'))
        TextPRM(self.pars,  'SMTP_SERV',    'SMTP email server', 'smtp.ulg.ac.be')
        
        mtfExe = os.path.abspath(os.path.dirname(__file__))+os.sep+'Metafor'
        if (not isUnix()):
            mtfExe = mtfExe+'.exe'
        
        TextPRM(self.pars,  'EXEC_NAME',    'exec name',  mtfExe)
        TextPRM(self.pars,  'TEST_NAME',    'test filename', './mesTests/monTest.py')        
        TextPRM(self.pars,  'TEST_DIR',     'test dir for multi', './mesTests/')
        TextPRM(self.pars,  'OUTFILE',      'logfile (no ext)', 'out')
        
        YesNoPRM(self.pars, 'MULTITEST',    'Run multiple test on dir', False)
        MultiPRM(self.pars, 'ALGORITHM',    'algorithm', ["meta", "import", "execfile", "clean", "verif", "restart"], "meta")
        
        TextPRM(self.pars,  'RESTART_STEP', 'restart step', "-1")
        
        TextPRM(self.pars,  'NICE_VALUE',   'nice value', "0")     
        TextPRM(self.pars,  'AFFINITY',     'affinity (cores list)', "")    
        TextPRM(self.pars,  'NB_TASKS',     'nb of task launched in parallel', "1")
        TextPRM(self.pars,  'NB_THREADS',   'nb of threads by task', "1")  
        if isUnix():
            MultiPRM(self.pars, 'RUNMETHOD',    'Run Method', ["interactive", "batch", "sge", "slurm"], "interactive")
        else:
            MultiPRM(self.pars, 'RUNMETHOD',    'Run Method', ["interactive"], "interactive")            
        TextPRM(self.pars,  'SGEARGS',      'additional SGE args', "")
        TextPRM(self.pars,  'SGEQUEUE',     'SGE queue', "lomem.q")   
        YesNoPRM(self.pars, 'SGELOCALDISK', 'SGE run on local disk', True)    
        #YesNoPRM(self.pars, 'SLURMLOCALDISK', 'SLURM run on local disk', True)    
        TextPRM(self.pars,  'QUEUE',        'Queue name', "defq")   
        TextPRM(self.pars,  'MEMORY',       'Total Memory (Mb)', "1000")   
        TextPRM(self.pars,  'TIME',         'Time (d-hh:mm:ss) ', "0-1:00:00")   

        YesNoPRM(self.pars, 'ENABLE_FTP',   'ftp transfert', False)
        TextPRM(self.pars,  'FTP_HOST',     'ftp host', "garfield.ltas.ulg.ac.be")
        TextPRM(self.pars,  'FTP_PORT',     'ftp port', "21")
        TextPRM(self.pars,  'FTP_USER',     'ftp user', "dark")
        TextPRM(self.pars,  'FTP_PASS',     'ftp passwd', "vador")
        TextPRM(self.pars,  'FTP_DIR',      'ftp directory', "incoming")
        
        PRMAction(self.actions, 'a', self.pars['MAIL_ADDR']) 
        PRMAction(self.actions, 'b', self.pars['EXEC_NAME']) 
        PRMAction(self.actions, 'c', self.pars['TEST_NAME']) 
        PRMAction(self.actions, 'c', self.pars['TEST_DIR']) 
        PRMAction(self.actions, 'd', self.pars['OUTFILE']) 
        
        PRMAction(self.actions, 'e', self.pars['ALGORITHM']) 
        PRMAction(self.actions, 'f', self.pars['RESTART_STEP']) 
        PRMAction(self.actions, 'g', self.pars['MULTITEST']) 
        
        PRMAction(self.actions, 'h', self.pars['NICE_VALUE'])
        PRMAction(self.actions, 'i', self.pars['AFFINITY'])  
        PRMAction(self.actions, 'j', self.pars['NB_TASKS'])      
        PRMAction(self.actions, 'k', self.pars['NB_THREADS'])
        PRMAction(self.actions, 'm', self.pars['RUNMETHOD'])
        # SGE PARAMETERS
        PRMAction(self.actions, 'n', self.pars['SGEQUEUE'])
        PRMAction(self.actions, 'o', self.pars['SGELOCALDISK'])
        PRMAction(self.actions, 'p', self.pars['SGEARGS'])
        # SLURM PARAMETERS
        PRMAction(self.actions, 'n', self.pars['QUEUE'])
        PRMAction(self.actions, 'o', self.pars['MEMORY'])
        PRMAction(self.actions, 'p', self.pars['TIME'])        
        # FTP
        PRMAction(self.actions, 'u', self.pars['ENABLE_FTP']) 
        PRMAction(self.actions, 'v', self.pars['FTP_HOST']) 
        PRMAction(self.actions, 'w', self.pars['FTP_PORT'])
        PRMAction(self.actions, 'x', self.pars['FTP_USER'])
        PRMAction(self.actions, 'y', self.pars['FTP_PASS'])
        PRMAction(self.actions, 'z', self.pars['FTP_DIR'])
        
        # Actions
        NoAction(self.actions) 
        GoAction(self.actions,    'G') 
        SaveAction(self.actions,  'S') 
        QuitAction(self.actions,  'Q')
        
    def applyDependencies(self):      
        ret = False
        if self.debug :
            print "applyDependecies : " 
            print "     self.pars['ALGORITHM'].val = ", self.pars['ALGORITHM'].val
        
            
        if self.pars['ALGORITHM'].val=='restart':
            self.pars['MULTITEST'].val = False
            ret = True
            
        if self.debug :
            print "     self.pars['MULTITEST'].val = ", self.pars['MULTITEST'].val
        return ret
        
    def configActions(self):            
        self.pars['MAIL_ADDR'].enable(self.pars['SEND_MAIL'].val==True)
        self.pars['SMTP_SERV'].enable(self.pars['SEND_MAIL'].val==True)
        
        self.pars['TEST_NAME'].enable(self.pars['MULTITEST'].val==False)
        self.pars['TEST_DIR'].enable(self.pars['MULTITEST'].val==True)
                                 
        self.pars['RESTART_STEP'].enable(self.pars['ALGORITHM'].val=='restart' and
                                         self.pars['MULTITEST'].val==False)   
        
        self.pars['FTP_HOST'].enable(self.pars['ENABLE_FTP'].val==True)
        self.pars['FTP_PORT'].enable(self.pars['ENABLE_FTP'].val==True)
        self.pars['FTP_USER'].enable(self.pars['ENABLE_FTP'].val==True)
        self.pars['FTP_PASS'].enable(self.pars['ENABLE_FTP'].val==True)
        self.pars['FTP_DIR'].enable(self.pars['ENABLE_FTP'].val==True)
        
        self.pars['NICE_VALUE'].enable(self.pars['RUNMETHOD'].val!='sge' and
                                       self.pars['RUNMETHOD'].val!='slurm')
        
        self.pars['AFFINITY'].enable(self.pars['RUNMETHOD'].val!='sge' and 
                                     self.pars['RUNMETHOD'].val!='slurm' and 
                                     self.pars['MULTITEST'].val==False)
        # SGE                             
        self.pars['SGEQUEUE'].enable(self.pars['RUNMETHOD'].val=='sge')
        self.pars['SGELOCALDISK'].enable(self.pars['RUNMETHOD'].val=='sge' and
                                         self.pars['ALGORITHM'].val!='restart' )
        self.pars['SGEARGS'].enable(self.pars['RUNMETHOD'].val=='sge')        
        # SLURM
        self.pars['QUEUE'].enable(self.pars['RUNMETHOD'].val=='slurm')
        self.pars['TIME'].enable(self.pars['RUNMETHOD'].val=='slurm')
        self.pars['MEMORY'].enable(self.pars['RUNMETHOD'].val=='slurm')
        
        # force 
        #self.pars['TEST_NAME'].val = self.pars['TEST_NAME'].val
    
    def getJobName(self):
        if (self.pars['MULTITEST'].val==False) :
            jobname=os.path.basename(os.getcwd())+"."+self.pars['TEST_NAME'].val
        else :
            jobname=os.path.basename(os.getcwd())+"."+self.pars['TEST_DIR'].val
            
        jobname=jobname.replace(os.sep,'.')
        jobname=jobname.replace('.py','')
        jobname=jobname.replace('...','.')
        jobname=jobname.replace('..','.')
        if jobname.endswith('.'):
            jobname=jobname[:-1]
        return jobname
        
    def getOutFileName(self):
        outFileName  = "%s.%s.txt" % (self.pars['OUTFILE'].val, self.pars['ALGORITHM'].val)                
        if self.debug :
            print "outFileName = ", outFileName
        return outFileName
                    
    # RUN Functions 
    def run(self):
        # write kill scripts        
        if isUnix():
            if self.pars['RUNMETHOD'].val == 'interactive' or self.pars['RUNMETHOD'].val == 'batch':
                self.killScript(self.jobId, os.getpgrp())
            elif self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True:
                self.cpNodeResultsScript(self.jobId)
                self.rmNodeResultsScript(self.jobId)
        # check exec
        if not os.path.isfile(self.pars['EXEC_NAME'].val):
            self.error("Metafor executable not found at %s" % self.pars['EXEC_NAME'].val) 
        # add __init__.py
        if not os.path.isfile("__init__.py"):
            file = open("__init__.py","w")
            file.close()        
        
        # starts  tests
        if (self.pars['MULTITEST'].val==True) :                   
            #check 
            if not os.path.isdir(self.pars['TEST_DIR'].val) :
                print "Error : 'TEST_DIR' non existant directory"
                return           
            outRun = self.startMultipleTests(self.pars['TEST_DIR'].val)
        else :  
            #check 
            if not os.path.isfile(self.pars['TEST_NAME'].val) :
                print "Error : 'TEST_NAME' non existant file"
                return           
            #run            
            outRun = self.startMultipleTests(self.pars['TEST_NAME'].val)
            '''
            if (self.pars['ALGORITHM'].val == "restart" && self.pars['RESTART_STEP'].val > 0) :            
                outRun = self.startSingleTest()
            else:
                outRun = self.startMultipleTests(self.pars['TEST_NAME'].val)
            '''                
        if self.pars['ENABLE_FTP'].val==True:
            #tar facs
            cdir=os.path.basename(os.getcwd())
            tarname="%s.tar.gz" % cdir
            print "creating %s" % tarname
            os.chdir('..')
            tar = tarfile.open(tarname,'w:gz')
            for path, dirs, files in os.walk(cdir):
                for file in files:
                    tar.add(os.path.join(path,file))
            tar.close()

            #ftp
            print "sending results to %s" % self.pars['FTP_HOST'].val
            import ftplib
            ftp = ftplib.FTP()
            ftp.connect(self.pars['FTP_HOST'].val, self.pars['FTP_PORT'].val)
            ftp.login(self.pars['FTP_USER'].val, self.pars['FTP_PASS'].val)
            ftp.cwd(self.pars['FTP_DIR'].val)
            file = open(tarname,'r')
            ftp.storbinary('STOR %s' %tarname, file)
            file.close()
            ftp.quit()
            
            #clean
            os.remove(tarname)                        
            
        # remove kill scripts        
        if isUnix():
            fNames = []
            if self.pars['RUNMETHOD'].val == 'sge':
                fNames.append(self.qDelScriptName(self.jobId))
                fNames.append(self.cfgfile)
            elif self.pars['RUNMETHOD'].val == 'slurm' : 
                fNames.append(self.sCancelScriptName(self.jobId))
                fNames.append(self.cfgfile)     
            elif self.pars['RUNMETHOD'].val == 'batch' :    
                fNames.append("kill%s.py"%self.jobId)   
                fNames.append("atrm%s.py"%self.jobId)   
                fNames.append(self.cfgfile)     
            else:
                fNames.append("kill%s.py"%self.jobId)   
            for fil in fNames:
                if os.path.isfile(fil):
                    os.remove(fil)
        print "done."

    def startMultipleTests(self, tests):  
        print "startMultipleTests"    
        # writing recovery scripts    
        #if self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True :
        #    self.cpNodeResultsScript(self.jobId)
        #    self.rmNodeResultsScript(self.jobId)
        # starting timer
        now = datetime.datetime.now()
        print "starting Multiple test at %s (come back later)" % now.ctime()
        
        # opening outfile
        self.outFile   = open(self.getOutFileName(),"w") 
        mtfdir, mtfexe = os.path.split(self.pars['EXEC_NAME'].val)    
        mtfdir = os.path.abspath(mtfdir) # necessaire pour sge sinon, en local disk, soucis pour trouver libGen4.so
        # starting python battery
        if self.launchGui :                   
            #self.launchGui.outFile=outfile            
            # starting process (unable to renice it => nice in battery)
            prog = 'python'
            # python args -u : unbuffered output (to have output synchronized to output)
            #             -i : force a prompt event even if stdin is not a terminal (else it is not possible to write cmds to python)
            arg = ['-u', '-i']
            self.launchGui.process.start(prog, arg)
            self.launchGui.process.waitForStarted(-1)
            # defining the input flux
            pin = self.launchGui.process                           
        else :    
            #cmd = self.getNiceCmd(int(self.pars['NICE_VALUE'].val))  
            #cmd = cmd + ['python']        
            cmd = ['python']            
            if isUnix(): # shell=False  && sans close_fds = True (ca freeze)
                #Add mtfdir to LD_LIBRARY_PATH to allow launch to find mt*.so
                if 'LD_LIBRARY_PATH' in os.environ :
                    os.environ['LD_LIBRARY_PATH'] = mtfdir+':'+os.environ['LD_LIBRARY_PATH']
                else:
                    os.environ['LD_LIBRARY_PATH'] = mtfdir
                #self.outFile.write("LD_LIBRARY_PATH = %s"%os.environ['LD_LIBRARY_PATH'])
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=self.outFile, stderr=self.outFile, env=os.environ, shell=False, close_fds=True)            
            else: # si nice+Windows => "shell=True" (pour "start")       
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=self.outFile, stderr=self.outFile, env=os.environ, shell=True)                        
            # defining the input flux
            pin = p.stdin
            
        # filling command to battery    
        pin.write('import sys, os, os.path\n')
        if self.debug :    
            pin.write('print "sys.path = ", sys.path\n')
            pin.write('print "os.getcwd() = ", os.getcwd()\n')
        #pin.write("raw_input()\n")
        pin.write('if os.path.isdir(r"%s"):\n'%mtfdir)
        pin.write('\tsys.path.append(r"%s")\n'%mtfdir) # mtfdir est dorenavant un abspath
        #pin.write('\tsys.path.append(os.path.abspath(r"%s"))\n'%mtfdir)
        pin.write('else:\n')
        pin.write('\tprint "metafor dir %s not found!"\n'%mtfdir)
        pin.write('\tsys.exit()\n\n')
        pin.write('execfile(r"%s")\n'%os.path.join(mtfdir,'.pythonrc.py'))
        pin.write('import toolbox.battery as b\n')
        pin.write('battery = b.Battery() \n')        
        pin.write('battery.keepFacs = True\n')
        pin.write('battery.dirs = [r"%s"]\n'%tests)    
        
        if (self.pars['ALGORITHM'].val == "execfile") :
            reg1=r"(.+)_0*([1-9][0-9]*)\.py"
            exp1= re.compile(reg1)
            m = exp1.match(os.path.basename(tests))
            if m: # chaining tests
                pin.write('battery.addCplxExecPath(r"%s_*")\n'%os.path.join(os.path.dirname(tests), m.group(1)))
                print 'battery.cplx_exec = [r"%s_*"]\n'%os.path.join(os.path.dirname(tests), m.group(1))
            else:
                pin.write('battery.addCplxExecPath(r"%s")\n'%tests)       
                print 'battery.cplx_exec = [r"%s"]\n'%tests
        elif (self.pars['ALGORITHM'].val == "import" ):
            pin.write('battery.addCplxImportPath(r"%s")\n'%tests)       
            print 'battery.cplx_import = [r"%s"]\n'%tests
        elif (self.pars['ALGORITHM'].val == "restart" ):
            pin.write('battery.addRestartPath(r"%s")\n'%tests)       
            print 'battery.restart = [r"%s"]\n'%tests
            
        pin.write('battery.verifsrc  = "verif"\n')
        pin.write('battery.codes = [ "FAILED", "STP", "ITE", "INW", "EXT", "EXW", "LKS", "CPU", "MEM" ]\n')     
            
        if (self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True) :
            pin.write('battery.setWDRoot("%s")\n'%self.getSGELocalDiskDir(self.jobId))
            
        if self.pars['RUNMETHOD'].val != 'sge':
            if self.pars['AFFINITY'].val != '' :
                pin.write('battery.setAffinity("%s")\n'%self.pars['AFFINITY'].val)
            if self.pars['NICE_VALUE'].val != '0':
                #print 'battery.setNice(%s)\n'%self.pars['NICE_VALUE'].val
                pin.write('battery.setNice(%s)\n'%self.pars['NICE_VALUE'].val)
        
        pin.write('battery.setNumTasks(%s)\n'%self.pars['NB_TASKS'].val)
        pin.write('battery.setNumThreads(%s)\n'%self.pars['NB_THREADS'].val)
        pin.write('battery.mtfdir = r"%s"\n'%mtfdir)
        if self.pars['ALGORITHM'].val == 'clean' :            
            pin.write('battery.start("clean")\n')
        elif self.pars['ALGORITHM'].val == 'verif' :            
            pin.write('battery.verif()\n')
        else :
            pin.write('battery.start("run")\n')
        #pin.write('battery.verif()\n') # pas très utile dans le cadre de launch ou faudrait faire un verif + malin)
        # write to exit python at the end of job
        pin.write('quit()\n')
        
        # wait for process to finish
        if self.launchGui :
            retcode = self.launchGui.waitQProcessForFinish()
            #print "Qprocess finished with retcode : ",retcode
        else :  
            #close pin flux
            pin.close()
            # waiting execution time
            retcode = p.wait()

        # closing file
        self.outFile.flush()        
        self.outFile.close()
        self.outFile = None
                
        # post pro cmd
        if (self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True) :            
            print "Trying to get back local workspace to home"
            self.moveSGELocalDir2Home(self.jobId)
        
        now = datetime.datetime.now()
        print "battery completed at %s" % now.ctime()
        if self.pars['SEND_MAIL'].val == True :
            self.mailmsg("multipleTests complete", file=self.getOutFileName())
        return retcode
'''        
    def startSingleTest(self):
        # affinity/numa stuffs
        affinitycmd=[]
        if self.pars['AFFINITY'].val!='' and self.pars['RUNMETHOD'].val != 'sge':
            if self.hasSysCmd('numactl'):
                affinitycmd=[ "numactl", "--physcpubind", self.pars['AFFINITY'].val ] #, "--localalloc" ]
            elif self.hasSysCmd('taskset'):
                affinitycmd=[ "taskset", "-c", self.pars['AFFINITY'].val ]

        # set lib path
        libpath = os.path.dirname(os.path.abspath(self.pars['EXEC_NAME'].val))
        libpath = os.path.join(libpath,"lib")
        print "adding extra libpath =",libpath
        newenv=dict(os.environ)
        #newenv['PATH'] = newenv['PATH']+':'+libpath
        if newenv.has_key('LD_LIBRARY_PATH'):
            newenv['LD_LIBRARY_PATH'] = newenv['LD_LIBRARY_PATH']+':'+libpath
        else:
            newenv['LD_LIBRARY_PATH'] = libpath

        # spawn algo
        outFileName = self.getOutFileName()
        self.outFile=open(outFileName,"w")

        nicecmd=[]
        if platform.uname()[0]!='Windows':
            if self.pars['NICE_VALUE'].val!='0':
                nicecmd = [ "nice", "-%s" %self.pars['NICE_VALUE'].val]
            
        print "starting \"%s\" on %s" % (self.pars['ALGORITHM'].val, self.pars['TEST_NAME'].val)  
        #cmd = [ self.pars['EXEC_NAME'].val, "-nogui", "-j", "%s"%self.pars['NB_THREADS'].val]       
        cmd = [ self.pars['EXEC_NAME'].val, "-nogui"]
        p = Popen(nicecmd+affinitycmd+cmd, stdout=self.outFile, stderr=self.outFile, stdin=PIPE, env=newenv)     
        
        if self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True and self.pars['ALGORITHM'].val != "restart":
            # writing recovery scripts and running on local hdd
            self.cpNodeResultsScript(self.jobId)
            self.rmNodeResultsScript(self.jobId)
            p.stdin.write("setTheWDirRoot('%s')\n" %  self.getSGELocalDiskDir(self.jobId))                
        
        p.stdin.write("setNumTasks(%s)\n"%self.pars['NB_TASKS'].val)
        p.stdin.write("wrap.Blas.setNumThreads(%s)\n"%self.pars['NB_THREADS'].val)
        p.stdin.write("wrap.IntelTBB.setNumThreads(%s)\n"%self.pars['NB_THREADS'].val)
        if self.pars['ALGORITHM'].val=="meta":
            p.stdin.write("load(r'%s')\n" % (self.pars['TEST_NAME'].val))
            p.stdin.write("meta()\n")
        elif self.pars['ALGORITHM'].val=="execfile":
            p.stdin.write("__file__=r'%s'\n" % (self.pars['TEST_NAME'].val)) # needed by .pythonrc.py     
            p.stdin.write("execfile(r'%s')\n" % (self.pars['TEST_NAME'].val))
        elif self.pars['ALGORITHM'].val=="restart":
            p.stdin.write("load(r'%s')\n" % self.pars['TEST_NAME'].val)
            p.stdin.write("restart(%s)\n" % self.pars['RESTART_STEP'].val)
        elif self.pars['ALGORITHM'].val=="import":
            p.stdin.write("import os ; print os.environ\n")
            p.stdin.write("import %s\n" % self.pars['TEST_NAME'].val)

        p.stdin.write("quit()\n")            
        p.stdin.close()
        # waiting execution time
        retcode = p.wait()
        # recovering results and removing scripts
        if self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True and self.pars['ALGORITHM'].val != "restart":
            print "Getting back local disk workspace to home disk"
            self.moveSGELocalDir2Home(self.jobId)
            if os.path.isdir(self.getSGELocalDiskDir(self.jobId)) : # si la copie a été bien faite => le local dir a été nettoyé => on peut virer les scripts
                if os.path.isfile(self.cpNodeResultsScriptName(self.jobId)):
                    os.remove(self.cpNodeResultsScriptName(self.jobId))
                if os.path.isfile(self.rmNodeResultsScriptName(self.jobId)):
                    os.remove(self.rmNodeResultsScriptName(self.jobId))                    
        self.outFile.close()

        # grep results + e-mail
        import StringIO
        res=StringIO.StringIO()
        res.write("cwd=%s\n" % os.getcwd())
        for file in glob.glob('%s.*.txt'%self.pars['OUTFILE'].val):
            res.write("result file : %s\n"%file)
            for line in open(file,'r'):
                for txt in ["ERROR", "Error", "error", "TSC-", "Successful", "Problem at time"]:
                    if line.find(txt)!=-1:
                        res.write(line)
                        
        if self.pars['SEND_MAIL'].val == True :
            self.mailmsg("job %s done" % self.pars['TEST_NAME'].val, text=res.getvalue()) 
        res.close()
'''
if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser(description="Metafor's Launcher")      
    
    # definition of arguments 
    parser.add_argument('-d', '--directory', dest='rundir',
                      metavar='DIR', help='specify run directory (batch mode)')
    parser.add_argument('-x', '--nogui', action='store_false',
                      dest='usegui',default=True, help='disable menu')
    parser.add_argument('-i', '--jobId', dest='jobId', type=str, default='',
                       help='job id')
    parser.add_argument('-m', '--masternode', dest='masterNode', type=str,default='',
                       help='master node name')

    # Parsing arguments 
    args = parser.parse_args()    
    #if len(args)!=0:
    #    parser.error("too many arguments")      

    # starting launch
    if args.rundir:
        os.chdir(args.rundir)

    job = LaunchJob(args.jobId)
    job.setMasterNode(args.masterNode) #le defaut valant '' => ok
    
    if args.usegui:
        job.menu()
    else:
        job.run()
            
