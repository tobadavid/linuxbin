#!/usr/bin/env python
# -*- coding: latin-1; -*-
# $Id: comp.py 2667 2016-06-15 15:16:28Z papeleux $

#
# Script "comp.py": lancement automatique de la batterie Metafor
# ==============================================================
# RoBo juin 2007-...
#
# conversion a partir du script bash "comp.sh"
#  new: - possibilité de lancer un checkout sous windows
#       - utilisation du tar et email python
#       - utilisation de battery.py pour la creation du rapport html
#       - tmpdir est créé récursivement si nécessaire (os.makedirs)
#       - gestion objet du menu.

# notes:
#   config svn (windows): ! repository doit corresp avec le profil putty 
#   (blueberry, pas blueberry.ltas.ulg... p expl)
#   [tunnels]
#   ssh = C:/Program Files/putty/plink.exe

from parametricJob import *
                  
# -- CompJob class --

class CompJob(ParametricJob):
    def __init__(self,  _jobId=''):
        self.jobId=_jobId
        cfgfile="comp%s.cfg"%self.jobId            
        ParametricJob.__init__(self, cfgfile)
        self.loadPars()
            
    def setDefaultPars(self):
        if len(self.pars)!=0:
            return
        TextPRM(self.pars, 'MAIL_ADDR',  'e-mail address (reports)', os.getenv('USER'))
        TextPRM(self.pars, 'SMTP_SERV',  'SMTP email server',       'smtp.ulg.ac.be')
        TextPRM(self.pars, 'ARC_NAME',   'archive name',            '~/dev.zip')
        TextPRM(self.pars, 'SVNREP',     'SVN repository',          "svn+ssh://blueberry.ltas.ulg.ac.be/home/metafor/SVN")
        TextPRM(self.pars, 'GITREP',     'GIT repository',          "blueberry.ltas.ulg.ac.be:/home/metafor/GIT")        
        TextPRM(self.pars, 'SVNBRANCH',  'SVN branch',              "trunk")        
        TextPRM(self.pars, 'BUILD_OPT',  'build options',           "%s.cmake" % socket.gethostbyaddr(socket.gethostname())[0].split('.')[0])
        YesNoPRM(self.pars,'DEBUG_MODE', 'debug mode',              False)

        TextPRM(self.pars,  'NICE_VALUE',    'nice value', "0")      
        #TextPRM(self.pars, 'AFFINITY',     'affinity (cores list)', "")   
        TextPRM(self.pars,  'NB_TASKS',     'nb of task launched in parallel', "1")
        TextPRM(self.pars,  'NB_THREADS',   'nb of threads by task', "1")     

        MultiPRM(self.pars, 'RUNMETHOD',    'Run Method', ["interactif", "batch", "sge"], "batch")
        TextPRM(self.pars,  'SGEARGS',      'additional SGE args', "")
        TextPRM(self.pars,  'SGEQUEUE',     'SGE queue', "lomem.q")   
        YesNoPRM(self.pars, 'SGELOCALDISK', 'SGE run on local disk', True)

        # not possible to retrieve jobId if launch time is differed
        #TextPRM(self.pars,  'BATCHTIME',    'Batch Start Time', "now")   
        
        YesNoPRM(self.pars, 'HASBACON', 'is bacon present?', True)
        TextPRM(self.pars,  'ZHOST', 'hostname for bacon', "blueberry.ltas.ulg.ac.be")
        TextPRM(self.pars,  'ZUSER', 'username for bacon', getUsername())
        TextPRM(self.pars,  'ZDIR', 'tmp directory', "/home/%s/Tmp/%s" % ( getUsername(), socket.gethostbyaddr(socket.gethostname())[0]))
        TextPRM(self.pars,  'SSH_OPT', 'options for ssh', "-2")
                
        MultiPRM(self.pars, 'UNZIP', 'source', ["zip","checkout","present"],"zip")
        YesNoPRM(self.pars, 'COMPILE', 'compile', True)
        MultiPRM(self.pars, 'BATTERY', 'battery', [True, False, "continue"], True)
        YesNoPRM(self.pars, 'INSTALLER', 'installer', False)                        
        
        PRMAction(self.actions, 'a', self.pars['MAIL_ADDR']) 
        PRMAction(self.actions, 'b', self.pars['ARC_NAME'])
        PRMAction(self.actions, 'c', self.pars['SVNREP']) 
        PRMAction(self.actions, 'd', self.pars['SVNBRANCH'])
        PRMAction(self.actions, 'e', self.pars['GITREP']) 
        PRMAction(self.actions, 'f', self.pars['BUILD_OPT']) 
        PRMAction(self.actions, 'g', self.pars['DEBUG_MODE'])

        PRMAction(self.actions, 'h', self.pars['NICE_VALUE'])
        #PRMAction(self.actions, 'k', self.pars['AFFINITY'])
        PRMAction(self.actions, 'j', self.pars['NB_TASKS'])
        PRMAction(self.actions, 'k', self.pars['NB_THREADS'])
        #PRMAction(self.actions, 'l', self.pars['XXXXXXXXXXX'])               
        
        PRMAction(self.actions, 'm', self.pars['RUNMETHOD'])
        PRMAction(self.actions, 'n', self.pars['SGEQUEUE'])
        PRMAction(self.actions, 'o', self.pars['SGELOCALDISK'])
        PRMAction(self.actions, 'p', self.pars['SGEARGS'])
        
        #PRMAction(self.actions, 'n', self.pars['BATCHTIME'])

        PRMAction(self.actions, 'q', self.pars['HASBACON']) 
        PRMAction(self.actions, 'r', self.pars['ZHOST']) 
        PRMAction(self.actions, 's', self.pars['ZUSER']) 
        PRMAction(self.actions, 't', self.pars['ZDIR']) 
        PRMAction(self.actions, 'u', self.pars['SSH_OPT']) 
                
                
        NoAction(self.actions)
        PRMAction(self.actions, '1', self.pars['UNZIP']) 
        PRMAction(self.actions, '2', self.pars['COMPILE']) 
        PRMAction(self.actions, '3', self.pars['BATTERY']) 
        PRMAction(self.actions, '4', self.pars['INSTALLER'])
        
        NoAction  (self.actions) 
        GoAction  (self.actions, 'G') 
        SaveAction(self.actions, 'S') 
        QuitAction(self.actions, 'Q')
        
    def configActions(self):
        self.pars['ARC_NAME'].enable(self.pars['UNZIP'].val=="zip")
        self.pars['NB_TASKS'].enable(self.pars['COMPILE'].val==True or self.pars['BATTERY'].val!=False)
        self.pars['HASBACON'].enable(self.pars['BATTERY'].val==True)
        self.pars['ZHOST'].enable(self.pars['BATTERY'].val==True and self.pars['HASBACON'].val!=True)
        self.pars['ZUSER'].enable(self.pars['BATTERY'].val==True and self.pars['HASBACON'].val!=True)
        self.pars['ZDIR'].enable(self.pars['BATTERY'].val==True and self.pars['HASBACON'].val!=True)
        self.pars['SSH_OPT'].enable(self.pars['BATTERY'].val==True and self.pars['HASBACON'].val!=True)
        self.pars['BUILD_OPT'].enable(self.pars['COMPILE'].val==True)
        self.pars['DEBUG_MODE'].enable(self.pars['COMPILE'].val==True)
        self.pars['NICE_VALUE'].enable(self.pars['BATTERY'].val!=False and self.pars['RUNMETHOD'].val!='sge')
        self.pars['SVNREP'].enable(self.pars['UNZIP'].val=="checkout")
        self.pars['GITREP'].enable(self.pars['UNZIP'].val=="checkout")
        self.pars['SVNBRANCH'].enable(self.pars['UNZIP'].val=="checkout")
        self.pars['SGEQUEUE'].enable(self.pars['RUNMETHOD'].val=='sge')
        self.pars['SGEARGS'].enable(self.pars['RUNMETHOD'].val=='sge')
        self.pars['SGELOCALDISK'].enable(self.pars['RUNMETHOD'].val=='sge')
        #self.pars['BATCHTIME'].enable(self.pars['RUNMETHOD'].val=='batch')

    def touchFiles(self):
        for module in ['oo_meta', 'oo_nda', 'parasolid']:
            print "touching %s" % module
            for path, dirs, files in os.walk(module):
                for file in files:
                    os.utime(os.path.join(path,file),None) # touch file

    def checkOut(self):
        for mod in ['linuxbin', 'oo_meta', 'oo_nda', 'parasolid.git']:
            module, ext = os.path.splitext(mod)
            if not os.path.isdir(module):
                if ext=='.git':
                    print "cloning %s..." % module
                    cmd = "git clone --quiet %s/%s.git" % (self.pars['GITREP'].val, 
                            module)                     
                else:
                    if module == 'linuxbin' : # lpx : patch pas beau temporaire vu que linuxbin n'a pas de "trunk"
                        print "checking-out %s/%s..." % (module, self.pars['SVNBRANCH'].val)
                        cmd = "svn co --quiet %s/%s %s" % (self.pars['SVNREP'].val, 
                              module, module)                
                    else :
                    print "checking-out %s/%s..." % (module, self.pars['SVNBRANCH'].val)
                    cmd = "svn co --quiet %s/%s/%s %s" % (self.pars['SVNREP'].val, 
                          module, self.pars['SVNBRANCH'].val, module)                
                if self.pars['RUNMETHOD'].val == 'sge' and \
                   self.pars['SGELOCALDISK'].val == True :             
                    cmd = 'ssh %s ". %s; cd %s; %s"' % (self.masterNode, 
                          self.guessProfile(), os.getcwd(), cmd)                    
                os.system(cmd)
                                
    def doClean(self):
        for dir in ['linuxbin','oo_meta', 'oo_metaB', 'oo_nda', 'parasolid']:
            if os.path.isdir(dir):
                print "removing old %s directory" % dir
                shutil.rmtree(dir)

    def doUnzip(self):
        print "unzipping files"
        file = self.pars['ARC_NAME'].val
        if not os.path.isfile(os.path.expanduser(file)):
            self.error("archive %s is not here!" % file)
        ext = os.path.splitext(file)[1]
        if ext==".zip":
            # unzip the source and try to convert text files
            cmd = 'unzip -a %s -x "*/.svn/*" >/dev/null' % file
            sysOutput = os.system(cmd)
            if (sysOutput != 0):
                self.error("unable to unzip archive %s !" % file)
            # no conversion for ".svn" database
            cmd = 'unzip %s "*/.svn/*" >/dev/null' % file
            sysOutput = os.system(cmd)
            if (sysOutput != 0):
                self.error("unable to unzip archive %s !" % file)
            # convert some text files (if zip "text compression" was disabled)
            dos2unix([ 'linuxbin', 'oo_meta', 'oo_nda', 'parasolid' ], '*.txt;*.CPE;*.CRE;*.stp;*.l;*.y;*.dat')

        elif ext==".tgz" or ext==".tar.gz":
            tar = tarfile.open(os.path.expanduser(file),'r:gz')
            for tarinfo in tar:
                tar.extract(tarinfo)
            tar.close()          
        else:
            self.error("archive %s of unknown extension!" % file)

    def compileMETAFOR(self):
        # release or debug names/flags
        exe='bin/Metafor'
        dflag=''
        if self.pars['DEBUG_MODE'].val:
            dflag='-DCMAKE_BUILD_TYPE=Debug'
        # first check
        if not os.path.isdir('oo_meta'):
            self.error('oo_meta not here!')
        # create bin dir
        if os.path.isdir('oo_metaB'):
            print "removing old %s directory" % 'oo_metaB'
            shutil.rmtree('oo_metaB')
        os.mkdir('oo_metaB')
        os.chdir('oo_metaB')
        # configure
        print "configuring oo_meta"
        cmfile='../oo_meta/CMake/%s' % self.pars['BUILD_OPT'].val
        #print cmfile
        if not os.path.isfile(cmfile):
            msg="%s not found!" % cmfile
            print msg
            self.mailmsg(msg)
        cmd = 'cmake -C %s %s ../oo_meta >autocf.log 2>&1' % (cmfile, dflag)
        #print cmd
        os.system(cmd)
        # compile
        ncpu = int(self.pars['NB_TASKS'].val) * int(self.pars['NB_THREADS'].val)
        #ncpu=int(self.pars['NB_TASKS'].val)
        print "compiling %s using %s cpu(s) (have a coffee)" % (exe, ncpu)
        os.system('make -j %d %s >compile.log 2>&1' % (ncpu, dflag))
        # check exe 
        if os.path.isfile(exe) and os.access(exe, os.X_OK):
            msg="compilation of %s OK" % exe
            print msg
            self.mailmsg(msg, 'compile.log')
        else:
            msg='compilation of %s FAILED' % exe
            self.error(msg, 'compile.log')
        os.chdir('..')
   
    def compile(self):
        self.compileMETAFOR()

    def cleanBattery(self):
        os.chdir('oo_metaB/bin')
        print "cleaning old results"
        os.system("python battery.py clean >/dev/null 2>&1")
        os.chdir('../..')


    def remoteBacon(self):
        # create a tarball
        tarname='apps.tar.gz'
        fdbname='fdb.tar.gz'
        if os.path.isfile(tarname):
            os.remove(tarname)
        print "creating %s" % tarname
        tar = tarfile.open(tarname,'w:gz')
        for pydir in ['oo_meta', 'oo_nda']:
            if os.path.isdir(pydir):    
                for path, dirs, files in os.walk(pydir):
                    for file in files:
                        for ext in ['*.py','*.dat']:
                            if fnmatch.fnmatch(file,ext):
                                #print "adding", os.path.join(path,file)
                                tar.add(os.path.join(path,file))
        tar.close()
    
        print "creating remote tmp directory %s" % self.pars['ZDIR'].val
        cmd1='ssh %s %s@%s ' % (self.pars['SSH_OPT'].val, self.pars['ZUSER'].val, self.pars['ZHOST'].val)
        cmd2='"python -c \'import os,os.path; os.path.isdir(\\"%s\\") or os.makedirs(\\"%s\\")\'"' % (self.pars['ZDIR'].val, self.pars['ZDIR'].val)
        #print cmd1+cmd2
        os.system(cmd1+cmd2)
        
        print "copying %s on %s" %(tarname, self.pars['ZHOST'].val)
        cmd3='scp %s %s %s@%s:%s' %(self.pars['SSH_OPT'].val, tarname, self.pars['ZUSER'].val, self.pars['ZHOST'].val, self.pars['ZDIR'].val)
        os.system(cmd3)
        os.remove(tarname)

        print "copying %s on %s" %(sys.argv[0], self.pars['ZHOST'].val)
        cmd3b='scp %s %s %s@%s:%s' %(self.pars['SSH_OPT'].val, sys.argv[0], self.pars['ZUSER'].val, self.pars['ZHOST'].val, self.pars['ZDIR'].val)
        os.system(cmd3b)
       
        print "exec'ing remote script (%s)" % os.path.basename(sys.argv[0])
        cmd4='"cd %s ; ./%s --bacon"' %  (self.pars['ZDIR'].val, os.path.basename(sys.argv[0]))
        os.system(cmd1+cmd4)
    
        print "retrieving results"
        cmd5='scp %s %s@%s:%s/%s .' %(self.pars['SSH_OPT'].val, self.pars['ZUSER'].val, self.pars['ZHOST'].val, self.pars['ZDIR'].val, fdbname)
        os.system(cmd5)
    
        print "cleaning remote side"
        cmd6='"cd %s ; rm -f %s %s"' % (self.pars['ZDIR'].val, fdbname, os.path.basename(sys.argv[0]))
        os.system(cmd1+cmd6)
    
        if not os.path.isfile(fdbname):
            self.error("archive %s not found" % fdbname)
        print "extracting %s" % fdbname
        tar = tarfile.open(fdbname,'r:gz')
        for tarinfo in tar:
            tar.extract(tarinfo)
            os.utime(tarinfo.name, None) # touch fdb
        tar.close()
        os.remove(fdbname)


    def baconize(self):              # called remotely
        tarname='apps.tar.gz'
        fdbname='fdb.tar.gz'
        if not os.path.isfile(tarname):
            self.error('%s not here' % tarname)
        tar = tarfile.open(tarname,'r:gz')
        #tar.extractall() # python2.5 only
        for tarinfo in tar:
            #print "extracting", tarinfo.name
            tar.extract(tarinfo)
        tar.close()
        os.remove(tarname)
        print "[%s] building fdb's from dat" % socket.gethostbyaddr(socket.gethostname())[0]
        os.chdir('oo_meta')
        cmd="python battery.py buildfdb >/dev/null"
        os.system(cmd)
        os.chdir('..')
        print "[%s] creating %s" % (socket.gethostbyaddr(socket.gethostname())[0],fdbname)
        tar = tarfile.open(fdbname,'w:gz')    
        for pydir in ['oo_meta','oo_nda']:
            if os.path.isdir(pydir):    
                for path, dirs, files in os.walk(pydir):
                    for file in files:
                        if fnmatch.fnmatch(file,'*.fdb'):
                            tar.add(os.path.join(path,file))
        tar.close()
        print "[%s] job done; cleaning" % socket.gethostbyaddr(socket.gethostname())[0]
        shutil.rmtree('oo_meta')

    def startBat(self):
        now = datetime.datetime.now()
        print "starting battery at %s (come back tomorrow)" % now.ctime()
        os.chdir('oo_metaB/bin')
        if (self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True) :
            self.cpNodeResultsScript(self.jobId)
            self.rmNodeResultsScript(self.jobId)
            cmd="nice -%s python battery.py -j %s -k %s -wdroot %s >battery.log 2>&1" % (self.pars['NICE_VALUE'].val, self.pars['NB_TASKS'].val, self.pars['NB_THREADS'].val, 
            self.getSGELocalDiskDir(self.jobId))
        else :
            cmd="nice -%s python battery.py -j %s -k %s >battery.log 2>&1" % (self.pars['NICE_VALUE'].val, self.pars['NB_TASKS'].val, self.pars['NB_THREADS'].val)
        #os.system(cmd)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()        
        # get results back from local disk
        if (self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True) :            
            print "Trying to get back local workspace to home"
            self.moveSGELocalDir2Home(self.jobId)
            if not os.path.isdir(self.getSGELocalDiskDir(self.jobId)) : # si la copie a été bien faite => le local dir a été nettoyé => on peut virer les scripts
                if os.path.isfile(self.cpNodeResultsScriptName(self.jobId)):
                    os.remove(self.cpNodeResultsScriptName(self.jobId))
                if os.path.isfile(self.rmNodeResultsScriptName(self.jobId)):
                    os.remove(self.rmNodeResultsScriptName(self.jobId))
         # finish script   
        now = datetime.datetime.now()
        print "battery completed at %s" % now.ctime()
        self.mailmsg("battery complete", file='battery.log')
        os.chdir('../..')

    def checkResults(self):             # pars indep
        os.chdir('oo_metaB/bin')
        print "diff'ing results"
        cmd="python battery.py diff"
        if self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True :      
            cmd = 'ssh %s ". %s ; cd %s ; %s "' % (self.masterNode, self.guessProfile(), os.getcwd(), cmd)
        print "checkResults: cmd = %s"%cmd
        os.system(cmd)
        file='verif/%s-diffs.html' % machineid()
        print "verif file name = %s"%file
        #self.mailhtml(file, "html report")
        self.mailHtmlAsAttachement(file, "html report")
        print "file %s sent as attachement ..."%file
        os.chdir('../..')

    def createInstaller(self):
        # check if compilation has been done
        if not os.path.isdir('oo_metaB/bin') or not os.path.isfile('oo_metaB/bin/Metafor'):             
            msg='Metafor not present'
            self.error(msg)
        # make install => everything in ./Metafor/...
        os.chdir('oo_metaB')        
        os.system('make install >install.log 2>&1')
        os.chdir('..')
        # check make install worked                
        if not os.path.isdir('Metafor'):
            self.error('./Metafor/ dir not found : compilation may have not worked')
        if not os.path.isfile('Metafor/Metafor'):
            self.error('./Metafor/Metafor file not found : compilation may have not worked')
        
        now = datetime.datetime.now()
        instname='metafor-%s-%d-%02d-%02d.tar.gz' % (socket.gethostname(), now.year, now.month, now.day)
        print "creating installer %s" % instname
        if os.path.isfile(instname):
            os.remove(instname)
        tar = tarfile.open(instname,'w:gz')    
        for path, dirs, files in os.walk('Metafor'):
            for file in files:
                tar.add(os.path.join(path,file))
        tar.close()

    def getJobName(self):
        return os.path.basename(os.getcwd())+".battery"

    def run(self):        
        # kill script that kills running tree
        if self.pars['RUNMETHOD'].val != "sge":
            self.killScript(self.jobId, os.getpgrp()) 
        
        if self.pars['UNZIP'].val=="checkout":
            self.doClean()
            self.checkOut()
        elif self.pars['UNZIP'].val=="zip":
            self.doClean()
            self.doUnzip()
            self.checkOut() # ce qui manque seulement
            self.touchFiles()
            
        if self.pars['COMPILE'].val:
            self.compile()

        if self.pars['BATTERY'].val==True:
            self.cleanBattery()
            if not self.pars['HASBACON'].val:
                self.remoteBacon()

        if not self.pars['BATTERY'].val==False:
            self.startBat()
            self.checkResults()

        if self.pars['INSTALLER'].val==True:
            self.createInstaller()

        if self.pars['RUNMETHOD'].val == 'sge':
            if os.path.isfile("qDel%s.py"%self.jobId):
                os.remove("qDel%s.py"%self.jobId)    
            if os.path.isfile(self.cfgfile):
                os.remove(self.cfgfile)
        elif self.pars['RUNMETHOD'].val == 'batch':
            if os.path.isfile("kill%s.py"%self.jobId):
                os.remove("kill%s.py"%self.jobId)
            if os.path.isfile("atrm%s.py"%self.jobId):
                os.remove("atrm%s.py"%self.jobId)
            if os.path.isfile(self.cfgfile):
                os.remove(self.cfgfile)              
        else: #self.pars['RUNMETHOD'].val == 'interactif'
            if os.path.isfile("kill%s.py"%self.jobId):
                os.remove("kill%s.py"%self.jobId)
                
        print "done."


# -- main --

if __name__ == "__main__":

    try:
        import signal  
        signal.signal(signal.SIGBREAK, sigbreak);
    except:
        pass

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="rundir",
                      metavar="DIR", help="specify run directory (batch mode)")
    parser.add_option("-x", "--nogui", action="store_false",
                      dest="usegui",default=True, help="disable menu")
    parser.add_option("-b", "--bacon", action="store_true",
                      dest="bacon", help="baconize (remote script)")
    parser.add_option("-i", "--jobId", dest="jobId", type="str",default='',
                       help="job id")
    parser.add_option("-m", "--masternode", dest="masterNode", type="str",default='',
                       help="master node name")
    (options, args) = parser.parse_args()
    #print "options = ", options
    #print "args = ", args

    if len(args)!=0:
        parser.error("too many arguments")

    if options.rundir:
        os.chdir(options.rundir)
        
    #print "options.jobId = %s"% options.jobId
    job = CompJob(options.jobId)    
    job.setMasterNode(options.masterNode) #le defaut valant '' => ok
    
    if options.bacon:
        job.baconize()
        sys.exit()

    if options.usegui:
        job.menu()
    else:
        job.run()
        


            
            
