# -*- coding: latin-1; -*-

import sys, os, os.path, shutil, socket, platform, glob, fnmatch
import datetime, tarfile, subprocess
from prmClasses import *

# -- Base Class ----------------------------------------------------------------

class ParametricJob(PRMSet):
    def __init__(self,cfgfile, _verb=False):
        PRMSet.__init__(self, cfgfile, _verb)
        # parfois nécessaire de garder en mémoire le nom du master node
        # pour lui faire executer des cmd à travers un 'ssh "cmd"'(ex: svn sur fabulous)
        self.masterNode = ''
          
    def setMasterNode(self, mn):
        self.masterNode = mn   
                
    def getNiceCmd(self, niceValue):
        if isUnix():
            niceCmd = ['nice', '-%d'%niceValue]
        else:            
            if niceValue > 14 :
                prior = '/LOW'
            elif niceValue > 8 :
                prior = '/BELOWNORMAL'
            elif niceValue > 4 :
                prior = '/NORMAL'
            elif niceValue > 2 :
                prior = '/ABOVENORMAL'
            else:
                prior = '/HIGH'                                        
            niceCmd = ['start', prior, '/B', '/WAIT']        
        return niceCmd

    def getMailData(self):
        import re
        fromAddr = "%s@%s" % (os.path.basename(sys.argv[0]), socket.gethostbyaddr(socket.gethostname())[0])        
        toAddr   = self.pars['MAIL_ADDR'].val
        if re.match('(.+)@(.+)',toAddr) :
            smtpServ = self.pars['SMTP_SERV'].val
        else :
            toAddr = "%s@%s"%(self.pars['MAIL_ADDR'].val,socket.gethostbyaddr(socket.gethostname())[0])
            smtpServ = "localhost"
        if 0:            
            print "mailData:"
            print "\tfromAddr = %s" % fromAddr
            print "\ttoAddr   = %s" % toAddr
            print "\tsmtpServ = %s" % smtpServ
        return fromAddr, toAddr, smtpServ
        
    def mailmsg(self, msg="no subject", file=None, text=None):
        print 'mailmsg with subject "%s"' % msg
        # getting address & smtp servers
        fromA, toA, smtpServ = self.getMailData()                        
        #subject = "[%s] %s : %s" % (os.path.basename(sys.argv[0]), socket.gethostname(), msg)
        subject=msg
        head = "From: %s\nTo: %s\nSubject: %s\n\n\n" % (fromA, toA, subject)
        if text==None: text=""
        if file:
            try:
                f = open(file,'r')
                text = f.read()
                f.close()
            except:
                text="file not found"
        import smtplib
        server = smtplib.SMTP(smtpServ)
        server.sendmail(fromA, toA, head+text)
        server.quit()

    def mailhtml(self, file, subject):
        print 'mailhtml with subject "%s"' % subject
        # getting address & smtp servers
        fromA, toA, smtpServ = self.getMailData()        
        # building email
        from email.MIMEText import MIMEText
        file = open(file,'r')
        text = file.read()
        file.close()
        mail = MIMEText(text, 'html','iso-8859-1')
        #mail = MIMEText(text)
        mail['From'] = fromA
        mail['Subject'] = subject
        mail['To'] = toA
        #mail['Content-Type'] = 'text/html'
        import smtplib
        smtp = smtplib.SMTP(smtpServ)
        #smtp.set_debuglevel(1)
        smtp.sendmail(fromA, [toA], mail.as_string())
        smtp.close()
        
    def mailHtmlAsAttachement(self, fileName, subject):
        print 'mailHtmlAsAttachement with subject "%s"' % subject
        import mimetypes
        from email                import encoders
        from email.mime.multipart import MIMEMultipart
        from email.mime.base      import MIMEBase        
        # getting address & smtp servers
        fromA, toA, smtpServ = self.getMailData()      
        # building email
        mail =  MIMEMultipart()        
        mail['From']    = fromA
        mail['To']      = toA
        mail['Subject'] = subject
        #mail.preamble   = 'Battery result in attachement \n'       
        machineName = socket.gethostname() 
        from email.MIMEText import MIMEText        
        text = "Battery result on %s in attachement ...\n" % machineName        
        msg  = MIMEText(text, 'html','iso-8859-1')        
        msg['From']    = fromA
        msg['To']      = toA
        msg['Subject'] = subject
        mail.attach(msg)
        
        ctype, encoding = mimetypes.guess_type(fileName)  
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)      
        try:
            file = open(fileName,'r')
            print "file %s correctly opened for mailing" % fileName
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(file.read())
            file.close()
            print "file %s correctly closed after mailing" % fileName
        except smtplib.SMTPException:
            text="file %s not found"%fileName
        # Encode the payload using Base64
        encoders.encode_base64(msg)
        (head, tail) = os.path.split(fileName)
        newFileName = "%s-%s" %(machineName,tail)
        msg.add_header('Content-Disposition', 'attachment', filename=newFileName)
        mail.attach(msg)
        try:
            print "opening smtp"
            import smtplib
            smtp = smtplib.SMTP(smtpServ)
            #smtp.set_debuglevel(True)
            smtp.sendmail(fromA, toA, mail.as_string())
            smtp.close()
            print "closing smtp"
        except smtplib.SMTPException, e:
            print "mailHtmlAsAttachement : error during smtp sendmail !!!"
            print "smtplib.SMTPException returned : %s"%e
        
    def error(self, msg="error", file=None):
        print "**ERROR: %s" % msg
        self.mailmsg(msg, file)
        sys.exit(1)

    def guessProfile(self):
        for cfgfile in [os.path.expanduser('~/.profile'), os.path.expanduser('~/.bash_profile')]:
            if os.path.isfile(cfgfile):
                break
        else:
            self.error("bash profiles not found" % file)
        return cfgfile
        
    def hasSysCmd(self, cmd):
        import commands
        status, result = commands.getstatusoutput("which %s" % cmd)
        return status==0
        
    # BATCH SPECIFIC    
    def runBatch(self):
        # get guess profile
        cfgfile = self.guessProfile()
        # build script
        scriptname="runbatch.sh"
        file = open(scriptname,"w")
        file.write("#!/bin/bash\n")   # this avoids /bin/sh when sh=dash
        file.write(". %s\n" % cfgfile)
        file.write("echo `atq`\n")
        file.write("jobId=`atq | awk '{if ($1>jobId)jobId=$1} END {print jobId}'`\n")
        file.write("echo \"at JobId = $jobId\"\n")  
        file.write('%s -x -i $jobId -d "%s"\n' % (sys.argv[0], os.getcwd()) )
        file.close()
        os.chmod(scriptname,0700)
        print "starting script in batch mode : %s" % scriptname
        #shcmd="at %s -f %s" % (self.pars['BATCHTIME'].val, scriptname)
        shcmd="echo \"/bin/bash %s\" | at now" % (scriptname) # keep it like that else job may start in dash !!!
        #shcmd="at now + 1 minutes -f %s" % (scriptname)
        #shcmd="at now %s" % scriptname
        print "shcmd = ", shcmd
        import commands
        status, result = commands.getstatusoutput(shcmd)
        if status!=0:
            print "Job submission FAILED!"
        else:
            print "Submission SUCCESSFUL!"
            #print "result = ", result
            import re
            m = re.search('job ([0-9]+)',result)
            batchId = m.group(1)
            #print m.group
            if m:
                cfgFileName, cfgFileExtension = os.path.splitext(self.cfgfile)
                os.system("cp %s %s%s%s"%(self.cfgfile, cfgFileName, batchId, cfgFileExtension))
                self.atrmScript(batchId)
                print "\tuse 'atq' and find job number %s to check the status of your job" % batchId
                print "\t\t - 'a' means waiting in the queue" 
                print "\t\t - '=' means running"
                print "\tuse 'atrm %s to kill the job" % batchId    
                print "\t\t  or 'atrm%s.py' to kill the job" % batchId    
        sys.exit()
        
    def atrmScript(self, pid):
        filename = "atrm%s.py"%pid
        file=open(filename,"w")
        file.write("#!/usr/bin/env python\n")
        file.write("import os\n")
        file.write("os.system('atrm %s')\n" % pid)
        file.write("if os.path.isfile('kill%s.py'):\n" % pid)
        file.write("\texecfile('kill%s.py')\n" % pid) 
        file.close()
        os.chmod(filename,0700)

    def killScript(self, jobId, pid):
        filename = "kill%s.py"%jobId
        file=open(filename,"w")
        file.write("#!/usr/bin/env python\n")
        s="import os, signal; os.killpg(%d, signal.SIGKILL)\n" % pid
        file.write(s)
        file.close()
        os.chmod(filename,0700)
        
    # SGE SPECIFIC    
    def runSGE(self):  
        # get guess profile
        cfgfile = self.guessProfile()
        # do some checks specific to SGE (may change pars)
        if self.pars['NICE_VALUE'].val!='0':
            print "Warning: NICE_VALUE will be ignored (reset to 0)!!"
            self.pars['NICE_VALUE'].val='0'

        # build script
        scriptname="runsge.sh"
        file = open(scriptname,"w")
        file.write("#!/bin/bash\n")
        jobname = self.getJobName()
        file.write("#$ -N %s\n" % jobname)
        file.write("#$ -cwd\n")
        file.write("#$ -j y\n")
        file.write("#$ -S /bin/bash\n")
        file.write("#$ -m beas\n")
        file.write("#$ -M %s\n" % self.pars['MAIL_ADDR'].val)
        nbCores = (int(self.pars['NB_TASKS'].val) * int(self.pars['NB_THREADS'].val))
        file.write("#$ -pe snode %d\n" % nbCores)
        file.write("#$ -binding linear:%d\n" %  nbCores)
        #else:
        #    file.write("#$ -binding linear:1\n") # set affinity even for a single core job
        if self.pars['SGEQUEUE'].val!='':    
            file.write("#$ -q %s\n" % self.pars['SGEQUEUE'].val)
        if self.pars['SGEARGS'].val!='':
            file.write("#$ %s\n" % self.pars['SGEARGS'].val)
        import socket
        file.write(". %s %s\n" % (cfgfile,socket.gethostname()))
        cmd='%s -x -i $JOB_ID -m %s' % (sys.argv[0], socket.gethostname())
        file.write("%s\n" % cmd)
        file.close()
        # send to sge
        print "sending job '%s' to SGE" % jobname
        shcmd="qsub ./%s" % scriptname
        import commands
        status, result = commands.getstatusoutput(shcmd)
        print result
        if status!=0:
            print "Job submission FAILED!"
        else:
            print "Submission SUCCESSFUL!"
            import re
            m = re.compile('Your job ([0-9]+)').match(result)
            sgeId = m.group(1)
            if m:
                cfgFileName, cfgFileExtension = os.path.splitext(self.cfgfile)
                os.system("cp %s %s%s%s"%(self.cfgfile, cfgFileName, sgeId, cfgFileExtension))                
                self.qdelScript(sgeId)
                print "\tuse 'qstat -f -j %s' to check the status of your job" % sgeId
                print "\tuse 'qdel %s' to kill your job" % sgeId
                print "\tuse './%s' to get results from node disk" % self.cpNodeResultsScriptName(sgeId)
                print "\tuse './%s' to clean results from node disk" % self.rmNodeResultsScriptName(sgeId)
                print "\tuse './qDel%s.py' to kill your job, get results and clean node disk" % sgeId            
        sys.exit()
    def getSGELocalDiskDir(self, jobId):
        return "/local/%s_p%s"%(os.getenv('USER'), jobId)        
    def cpNodeResultsScriptName(self, jobId):        
        return "cpNodeResults%s.py"%jobId        
    def rmNodeResultsScriptName(self, jobId):        
        return "rmNodeResults%s.py"%jobId            
 
    def cpNodeResultsScript(self, jobId) :
        nodeHost = socket.gethostname()
        filename = self.cpNodeResultsScriptName(jobId)
        localNodeDir = self.getSGELocalDiskDir(jobId)
        localWSpace = localNodeDir+os.sep+'*'
        homeDir=os.getcwd()
        # write file
        file=open(filename,"w")
        file.write("#!/usr/bin/env python\n")
        file.write("import subprocess, sys\n")
        file.write("print 'Copying data from %s local disk started ...'\n"%(nodeHost))
        #cpCmd = 'ssh %s \"cp -pRvu %s %s\"' % (nodeHost, localWSpace, homeDir)  
        file.write("cpCmd = 'rsync -e ssh -abvz --delete-after %s:%s %s'" % (nodeHost, localWSpace, homeDir))
        file.write("outCp = subprocess.call(cpCmd, shell=True)\n")        
        file.write("if outCp == 0 :\n")
        file.write("\tprint 'Copy of data from %s local disk successfully done'\n"%(nodeHost))
        file.write("else :\n")
        file.write("\tprint 'Copy of data from %s local disk did NOT succeded.'\n"%(nodeHost))
        file.write("\tprint 'Check manually what went wrong before cleaning %s local disk'\n"%(nodeHost))       
        file.write("sys.exit(outCp)")
        file.close()
        os.chmod(filename,0700)

    def rmNodeResultsScript(self, jobId) :
        nodeHost = socket.gethostname()
        filename = self.rmNodeResultsScriptName(jobId)
        localNodeDir = self.getSGELocalDiskDir(jobId)
        #write file
        file=open(filename,"w")
        file.write("#!/usr/bin/env python\n")        
        #sshRmCmd = 'ssh %s "rm -rf %s"' % (nodeHost, localNodeDir)
        #s="import os; os.system('%s')\n" % sshRmCmd        
        #file.write(s)        
        file.write("import subprocess, sys\n")
        file.write("print 'Deleting data from %s local disk started ...'\n"%(nodeHost))
        file.write("outRm = subprocess.call('ssh %s \"rm -rf %s\"', shell=True)\n"%
                   (nodeHost, localNodeDir))
        file.write("if outRm == 0 :\n")
        file.write("\tprint 'Deleting of data from %s local disk successfully done'\n"%(nodeHost))
        file.write("else :\n")
        file.write("\tprint 'Deleting of data from %s local disk did NOT succeded.'\n"%(nodeHost))
        file.write("\tprint 'Check manually how to clean %s local disk'\n"%(nodeHost))       
        file.write("sys.exit(outRm)")
        file.close()
        os.chmod(filename,0700)

    def qDelScriptName(self, jobId):        
        filename = "qDel%s.py"%jobId
        return filename

    def qdelScript(self, jobId):
        filename = self.qDelScriptName(jobId)
        file=open(filename,"w")
        file.write("#!/usr/bin/env python\n")
        file.write("import subprocess, os, sys\n")
        file.write("subprocess.call('qdel %s',shell=True)\n"%jobId)
        homeDir=os.getcwd()
        nodeHost = socket.gethostname()
        localNodeDir = self.getSGELocalDiskDir(jobId)
        localWSpace = localNodeDir+os.sep+'*'
        file.write("if os.path.isfile('%s'):\n"%(self.cpNodeResultsScriptName(jobId)))
        file.write("\toutCp = subprocess.call('./%s', shell=True)\n"%(self.cpNodeResultsScriptName(jobId)))
        file.write("\tif outCp != 0 :\n")        
        file.write("\t\tprint 'Error copying files from node %s'\n"%nodeHost)        
        file.write("\t\tprint '\tget them using %s script '\n"%self.cpNodeResultsScriptName(jobId))
        file.write("\t\tprint '\tthen clean the remote disk using %s script '\n"%self.rmNodeResultsScriptName(jobId))
        file.write("\t\tsys.exit(1)\n")
        file.write("\telse :\n")     
        file.write("\t\tos.remove('./%s')\n"%(self.cpNodeResultsScriptName(jobId)))                                    
        file.write("if os.path.isfile('%s'):\n"%(self.rmNodeResultsScriptName(jobId)))
        file.write("\toutRm = subprocess.call('./%s', shell=True)\n"%(self.rmNodeResultsScriptName(jobId)))        
        file.write("\tif outCp != 0 :\n")        
        file.write("\t\tprint 'Error deleting files from node %s'\n"%nodeHost)        
        file.write("\t\tprint '\ttry cleaning them using %s script '\n"%self.rmNodeResultsScriptName(jobId))
        file.write("\t\tprint '\tand only if it do not work, clean disk by hand!!!'\n")    
        file.write("\t\tsys.exit(1)\n")   
        file.write("\telse :\n")     
        file.write("\t\tos.remove('./%s')\n"%(self.rmNodeResultsScriptName(jobId)))
        file.write("os.remove('./%s')\n"%(filename))
        file.write("sys.exit(0)\n")                            
        file.close()
        os.chmod(filename,0700)            
                
    def moveSGELocalDir2Home(self, jobId) :
        localNodeDir = self.getSGELocalDiskDir(jobId)
        homeDir=os.getcwd()
        print "trying to move %s/* to %s"%(localNodeDir,homeDir)
        #shutil.move(localNodeDir,homeDir) # do not work if dst dir exist or it exist => use of "cp -r"!!!
        try: # -R : recursif / p : preserve attribut (owner/mode/timestamp)  / u : update (copy only if source is newer than target)/ v : verbose
            ##cmd1 = "cp -Rpuv %s/* %s"%(localNodeDir, homeDir)
            #cmd1 = "cp -Rpu %s/* %s"%(localNodeDir, homeDir)          
            cmd1 = "rsync -abvz --delete-after  %s %s"%(localNodeDir, homeDir)          
            #--remove-source-files permet de nettoyer la source, mais ca risque de poser problème avec le check ci dessous 
            # qui plus est, ne supprime pas l'arborescence, juste les fichiers => nettoyage incomplet
            print "cmd1 = ", cmd1
            subprocess.call([cmd1],stderr=subprocess.STDOUT, shell=True) #use of subprocess to be able to catch errors          
            #execfile(self.cpNodeResultsScriptName(jobId))
            # check que la copie soit bonne (même fichiers des 2 cotés)                        
            import filecmp
            cmp = filecmp.dircmp(localNodeDir,homeDir)
            #print "cmp.report() = ",cmp.report()
            if recCmp(cmp) : # copie parfaite => nettoyage brutal de l'arborescence
                print "copie parfaite => nettoyage brutal de l'arborescence "
                cmd2 = "rm -rf %s"%localNodeDir
                print "cmd2 = ", cmd2            
                subprocess.call([cmd2],stderr=subprocess.STDOUT, shell=True) # 2 commands for not deleting files if copy throw an exception 
                #execfile(self.rmNodeResultsScriptName(jobId))
                os.remove(self.cpNodeResultsScriptName(jobId))
                os.remove(self.rmNodeResultsScriptName(jobId))                
                os.remove(self.qDelScriptName(jobId))
                # suppression des scripts   
            else : # on va au moins nettoyer ce qui est commun            
                print "copie imparfaite => nettoyage de ce qui est commun"
                os.path.chdir(localNodeDir)
                rmCommonFiles(cmp)
                os.path.chdir(homeDir)                            
        except OSError, e: #except OSError as e: dont work on blueberry
            print "unable to get back files from local directory"            
            print "subprocess returned error : ",e
            print "get back result files using %s "%self.cpNodeResultsScriptName(jobId)
    # END OF SGE SPECIFIC    
    #===========================================================================
    # SLURM SPECIFIC INTERFACE
    def runSlurm(self):  
        # get guess profile
        cfgfile = self.guessProfile()      
        # build script
        scriptname="runSlurm.sh"
        file = open(scriptname,"w")
        file.write("#!/bin/bash\n")
        file.write("# Metafor launch.py slurm script...\n")
        jobname = self.getJobName()
        #file.write("#SBATCH --job-name=%s\n" % jobname)
        file.write("#SBATCH --job-name=metafor\n")
        file.write("#SBATCH --mail-user=%s\n"%self.pars['MAIL_ADDR'].val)
        file.write("#SBATCH --mail-type=ALL\n")
        #file.write("#SBATCH --output=%s\n"%self.getOutFileName())        
        file.write("# Ressources needed...\n")
        file.write("#SBATCH --partition=%s\n"%self.pars['QUEUE'].val)
        file.write("#SBATCH --ntasks=1\n")
        file.write("#SBATCH --cpus-per-task=%s\n"%self.pars['NB_THREADS'].val)
        file.write("#SBATCH --time=%s\n"%self.pars['TIME'].val)
        file.write("#SBATCH --mem=%s\n"%self.pars['MEMORY'].val)
        #file.write("#SBATCH --mem-bind=verbose,local\n")
        #file.write("echo \"SLURM_JOB_ID = $SLURM_JOB_ID\"\n")
        #file.write("echo 'squeue'\n")
        import socket        
        file.write(". %s %s\n" % (cfgfile,socket.gethostname()))        
        cmd='%s -x -i $SLURM_JOB_ID -m %s' % (sys.argv[0], socket.gethostname())
        #file.write("echo 'before cmd %s'\n"%cmd)
        file.write("srun %s\n" % cmd)
        #file.write("echo 'cmd done'\n")

        file.close()
        os.chmod(scriptname,0700)
        # send to slurm
        print "sending job '%s' to Slurm" % jobname
        shcmd="sbatch ./%s" % scriptname
        import commands
        status, result = commands.getstatusoutput(shcmd)
        print result
        if status!=0:
            print "Job submission FAILED!"
        else:
            print "Submission SUCCESSFUL!"
            import re
            m = re.compile('Submitted batch job ([0-9]+)').match(result)
            slurmId = m.group(1)
            if m:
                cfgFileName, cfgFileExtension = os.path.splitext(self.cfgfile)
                os.system("cp %s %s%s%s"%(self.cfgfile, cfgFileName, slurmId, cfgFileExtension))                
                self.sCancelScript(slurmId)
                print "\tuse ' squeue -l -j %s ' to check the status of the SLURM scheduling queue of your job" % slurmId
                print "\tuse ' sprio -l -j %s ' to check the factor priority of your job" % slurmId
                print "\tuse ' sstat  -a --format=JobID,NTasks,MaxRSS,MaxVMSize -j %s ' to get information about your running job (adapt format to your needs)" % slurmId
                print "\tuse ' scancel %s ' to kill your job" % slurmId                
                print "\tuse ' sacct --format=JobID,NTasks,NCPUS,CPUTime,Elapsed,MaxRSS,MaxVMSize -j %s ' to get information about your finished job (adapt format to your needs)" % slurmId
        sys.exit()
   
    def sCancelScriptName(self, jobId):        
        filename = "sCancel%s.py"%jobId
        return filename

    def sCancelScript(self, jobId):
        filename = self.sCancelScriptName(jobId)
        file=open(filename,"w")
        file.write("#!/usr/bin/env python\n")
        file.write("import subprocess, os, sys\n")
        file.write("subprocess.call('scancel %s',shell=True)\n"%jobId)        
        file.write("os.remove('./%s')\n"%(filename))
        file.write("sys.exit(0)\n")                            
        file.close()
        os.chmod(filename,0700)           
       
    # END OF SLURM SPECIFIC INTERFACE
    
                
    # interface virtuelle...
    def run(self, sgeId=0):
        print "run : not implemented"
    def setDefaultPars(self):
        print "setDefaultPars : not implemented"
    def configActions(self):        
        print "configActions : not implemented"  
    def applyDependencies(self):   
        print "applyDependencies : not implemented"
          
    def go(self):        
        self.savePars()
        print "go in %s" % self.pars['RUNMETHOD'].val
        if self.pars['RUNMETHOD'].val == 'batch':
            self.runBatch()
        elif  self.pars['RUNMETHOD'].val == 'sge':
            self.runSGE()
        elif  self.pars['RUNMETHOD'].val == 'slurm':
            self.runSlurm()
        else:
            self.run()      
            
# fonctions utilitaires pour moveSGELocalDir2Home
def recCmp(cmp):         
    copyOk = True
    #print "cmp.left = ", cmp.left
    if len(cmp.left_only) != 0 :# on a des fichiers manquants ou différents
        print "local files only : ", cmp.left_only
        copyOk = False
    if len(cmp.diff_files) != 0: # fichiers differents
        print "files differents : ", cmp.diff_files
        copyOk =  False
    for subDirCmp in cmp.subdirs.values() :
        copyOk = recCmp(subDirCmp) # recursive function
        #if not copyOk : faire un break pour limiter le calcul
            #return copyOk
    return copyOk
    
def rmCommonFiles(cmp):     
    #print "cmp.left = ", cmp.left
    for subDir in cmp.subdirs :
        os.chdir(subdir)
        subDirCmp = cmp.subdirs[subdir]
        rmCommonFiles(subDirCmp)  # recursive function 
        print "fileToBeRemoved in %s: "%os.getcwd()
        for f in subDirCmp.common_files:
            print f
            os.remove(f)                    
        os.path.chdir('..')
        if os.path.isempty(subdir):
            os.path.rmdir(subdir)      
                  
# -- Misc Utilities --        
def getUsername():
    if os.environ.has_key('USER'):
        return os.environ['USER']
    elif os.environ.has_key('USERNAME'):
        return os.environ['USERNAME']
    else:
        return "unknown"

def machineid():
    uname = platform.uname()
    if uname[0] == 'Windows':
        return "CYGWIN"
    elif uname[0] == 'Linux':
        if uname[4] == 'x86_64':
            return "Linux64"
        else:
            return "Linux"
    else:
        return uname[0]

def all_files(root, patterns, skips, single_level, yield_folders):
    patterns = patterns.split(';')
    skips    = skips.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    fullname=os.path.join(path, name)
                    ok=True
                    for skip in skips:
                        if fnmatch.fnmatch(fullname, skip):
                            ok=False
                    if ok:        
                        yield fullname
                        break
        if single_level:
            break  

def dos2unix( roots, patterns ):
    """ example: dos2unix([ 'copra5' ], '*.CPE;*.CRE')
    """
    print "dos2unix: analysing %s" % patterns
    for root in roots:
        print "\t=> processing %s" % root
        for file in all_files(root, patterns, '.svn', 
                              single_level=False, yield_folders=False):  
            fromfile = os.path.abspath(file)
            cmd='dos2unix %s' % fromfile
            #print cmd
            os.system(cmd)
