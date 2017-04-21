#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# Script "comp.py": 
#  - compilation de Metafor
#  - lancement automatique de la batterie

from parametricJob import *

# -- repository classes --------------------------------------------------------

class Repo(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

class GitRepo(Repo):
    def __init__(self, name, url):
        super(GitRepo, self).__init__(name, url)
    def co_cmd(self):
        cmd = "git clone --quiet %s %s" % (self.url, self.name)
        return cmd
        
class SVNRepo(Repo):
    def __init__(self, name, url):
        super(SVNRepo, self).__init__(name, url)
    def co_cmd(self):
        cmd = "svn co --quiet %s %s" % (self.url, self.name)
        return cmd
                 
# -- CompJob class -------------------------------------------------------------

class CompJob(ParametricJob):
    """ Manage a compilation + battery.py
    """
    def __init__(self,  _jobId=''):
        # init base class
        self.jobId = _jobId
        cfgfile = "comp%s.cfg" % self.jobId            
        ParametricJob.__init__(self, cfgfile)
        
        # list of required repositories
        self.repos = []
        self.repos.append(SVNRepo('oo_meta', 'svn+ssh://blueberry.ltas.ulg.ac.be/home/metafor/SVN/oo_meta/trunk'))
        self.repos.append(SVNRepo('oo_nda', 'svn+ssh://blueberry.ltas.ulg.ac.be/home/metafor/SVN/oo_nda/trunk'))
        self.repos.append(GitRepo('linuxbin', 'https://github.com/ulgltas/linuxbin.git'))
        self.repos.append(GitRepo('parasolid', 'blueberry.ltas.ulg.ac.be:/home/metafor/GIT/parasolid.git'))    
              
        self.loadPars() # RB: semble inutile: deja fait dans classe de base PRMSet??

    def setDefaultPars(self):
        if len(self.pars)!=0:
            return
        TextPRM(self.pars,  'MAIL_ADDR',  'e-mail address (reports)', os.getenv('USER'))
        TextPRM(self.pars,  'SMTP_SERV',  'SMTP email server',       'smtp.ulg.ac.be')
        TextPRM(self.pars,  'ARC_NAME',   'archive name',            '~/dev.zip')
        TextPRM(self.pars,  'CMAKELIST',  'build options',           "%s.cmake" % socket.gethostbyaddr(socket.gethostname())[0].split('.')[0])
        YesNoPRM(self.pars, 'DEBUG_MODE', 'debug mode',              False)

        TextPRM(self.pars,  'NICE_VALUE',   'nice value', "0")   
        TextPRM(self.pars,  'NB_TASKS',     'nb of task launched in parallel', "1")
        TextPRM(self.pars,  'NB_THREADS',   'nb of threads by task', "1")     

        MultiPRM(self.pars, 'RUNMETHOD',    'Run Method', ["interactive", "batch", "sge"], "batch")
        TextPRM(self.pars,  'AT_TIME' ,     'Delay for at launch (no syntax check, use with care)', "now")    
        TextPRM(self.pars,  'SGEARGS',      'additional SGE args', "")
        TextPRM(self.pars,  'SGEQUEUE',     'SGE queue', "lomem.q")   
        YesNoPRM(self.pars, 'SGELOCALDISK', 'SGE run on local disk', True)
                
        MultiPRM(self.pars, 'UNZIP',     'source', ["zip", "checkout", "present"], "zip")
        YesNoPRM(self.pars, 'COMPILE',   'compile', True)
        MultiPRM(self.pars, 'BATTERY',   'battery', [True, False, "continue"], True)
        
        PRMAction(self.actions, 'a', self.pars['MAIL_ADDR']) 
        PRMAction(self.actions, 'b', self.pars['ARC_NAME']) 
        PRMAction(self.actions, 'c', self.pars['CMAKELIST']) 
        PRMAction(self.actions, 'd', self.pars['DEBUG_MODE'])

        PRMAction(self.actions, 'h', self.pars['NICE_VALUE'])
        PRMAction(self.actions, 'j', self.pars['NB_TASKS'])
        PRMAction(self.actions, 'k', self.pars['NB_THREADS'])
        
        PRMAction(self.actions, 'm', self.pars['RUNMETHOD'])
        # Batch paramters
        PRMAction(self.actions, 'n', self.pars['AT_TIME'])
        #sge parameters
        PRMAction(self.actions, 'n', self.pars['SGEQUEUE'])
        PRMAction(self.actions, 'o', self.pars['SGELOCALDISK'])
        PRMAction(self.actions, 'p', self.pars['SGEARGS'])
                
        NoAction(self.actions)
        PRMAction(self.actions, '1', self.pars['UNZIP']) 
        PRMAction(self.actions, '2', self.pars['COMPILE']) 
        PRMAction(self.actions, '3', self.pars['BATTERY']) 
        
        NoAction  (self.actions) 
        GoAction  (self.actions, 'G') 
        SaveAction(self.actions, 'S') 
        QuitAction(self.actions, 'Q')
        
    def configActions(self):
        self.pars['ARC_NAME'].enable(self.pars['UNZIP'].val=="zip")
        self.pars['NB_TASKS'].enable(self.pars['COMPILE'].val==True or self.pars['BATTERY'].val!=False)
        self.pars['NB_THREADS'].enable(self.pars['COMPILE'].val==True or self.pars['BATTERY'].val!=False)
        self.pars['CMAKELIST'].enable(self.pars['COMPILE'].val==True)
        self.pars['DEBUG_MODE'].enable(self.pars['COMPILE'].val==True)
        self.pars['NICE_VALUE'].enable(self.pars['BATTERY'].val!=False and self.pars['RUNMETHOD'].val!='sge')        
        # Batch        
        self.pars['AT_TIME'].enable(self.pars['RUNMETHOD'].val=='batch')
        # sge
        self.pars['SGEQUEUE'].enable(self.pars['RUNMETHOD'].val=='sge')
        self.pars['SGEARGS'].enable(self.pars['RUNMETHOD'].val=='sge')
        self.pars['SGELOCALDISK'].enable(self.pars['RUNMETHOD'].val=='sge')

    def touchFiles(self):
        for repo in self.repos:
            print "touching %s" % repo.name
            for path, dirs, files in os.walk(repo.name):
                for file in files:
                    os.utime(os.path.join(path,file), None) # touch file

    def checkOut(self):
        for repo in self.repos:
            if not os.path.isdir(repo.name):
                print 'checking out "%s" from %s...' % (repo.name, repo.url)
                cmd = repo.co_cmd()
                # embed "cmd" in a ssh call if a cluster local disk is used               
                if self.pars['RUNMETHOD'].val == 'sge' and \
                   self.pars['SGELOCALDISK'].val == True :             
                    cmd = 'ssh %s ". %s; cd %s; %s"' % (self.masterNode, 
                          self.guessProfile(), os.getcwd(), cmd)                    
                os.system(cmd)
                                
    def doClean(self):
        dirs = [ repo.name for repo in self.repos ]
        dirs.append('oo_metaB')
        for dir in dirs:
            if os.path.isdir(dir):
                print "removing old %s directory" % dir
                shutil.rmtree(dir)

    def doUnzip(self):
        print "unzipping files..."
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
            dos2unix([ repo.name for repo in self.repos ], '*.txt;*.CPE;*.CRE;*.stp;*.l;*.y;*.dat')

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
            print 'removing old %s directory' % 'oo_metaB'
            shutil.rmtree('oo_metaB')
        os.mkdir('oo_metaB')
        os.chdir('oo_metaB')
        # configure
        print "configuring oo_meta"
        cmfile = '../oo_meta/CMake/%s' % self.pars['CMAKELIST'].val
        #print cmfile
        if not os.path.isfile(cmfile):
            msg = '%s not found!' % cmfile
            print msg
            self.mailmsg(msg)
        cmd = 'cmake -C %s %s ../oo_meta >autocf.log 2>&1' % (cmfile, dflag)
        #print cmd
        os.system(cmd)
        # compile
        ncpu = int(self.pars['NB_TASKS'].val) * int(self.pars['NB_THREADS'].val)
        print 'compiling %s using %s cpu(s) (have a coffee)' % (exe, ncpu)
        os.system('make -j %d %s >compile.log 2>&1' % (ncpu, dflag))
        # check exe 
        if os.path.isfile(exe) and os.access(exe, os.X_OK):
            msg='compilation of %s OK' % exe
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

    def startBat(self):
        now = datetime.datetime.now()
        print "starting battery at %s (come back tomorrow)" % now.ctime()
        os.chdir('oo_metaB/bin')
        if (self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True):
            self.cpNodeResultsScript(self.jobId)
            self.rmNodeResultsScript(self.jobId)
            cmd="nice -%s python battery.py -j %s -k %s -wdroot %s >battery.log 2>&1" % (self.pars['NICE_VALUE'].val, self.pars['NB_TASKS'].val, self.pars['NB_THREADS'].val, 
            self.getSGELocalDiskDir(self.jobId))
        else :
            cmd="nice -%s python battery.py -j %s -k %s >battery.log 2>&1" % (self.pars['NICE_VALUE'].val, self.pars['NB_TASKS'].val, self.pars['NB_THREADS'].val)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()        
        # get results back from local disk
        if (self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True):            
            print "Trying to get back local workspace to home"
            self.moveSGELocalDir2Home(self.jobId)
            if not os.path.isdir(self.getSGELocalDiskDir(self.jobId)) : # si la copie a \E9t\E9 bien faite => le local dir a \E9t\E9 nettoy\E9 => on peut virer les scripts
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
        if self.pars['RUNMETHOD'].val == 'sge' and self.pars['SGELOCALDISK'].val == True:      
            cmd = 'ssh %s ". %s ; cd %s ; %s "' % (self.masterNode, self.guessProfile(), os.getcwd(), cmd)
        print "checkResults: cmd = %s" % cmd
        os.system(cmd)
        file='verif/%s-diffs.html' % machineid()
        print "verif file name = %s" % file
        #self.mailhtml(file, "html report")
        self.mailHtmlAsAttachement(file, "html report")
        print "file %s sent as attachement ..." % file
        os.chdir('../..')
        
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
            self.checkOut() # only missing folders
            self.touchFiles()
            
        if self.pars['COMPILE'].val:
            self.compile()

        if self.pars['BATTERY'].val==True:
            self.cleanBattery()

        if not self.pars['BATTERY'].val==False:
            self.startBat()
            self.checkResults()

        if self.pars['RUNMETHOD'].val == 'sge':
            if os.path.isfile("qDel%s.py" % self.jobId):
                os.remove("qDel%s.py" % self.jobId)    
            if os.path.isfile(self.cfgfile):
                os.remove(self.cfgfile)
        elif self.pars['RUNMETHOD'].val == 'batch':
            if os.path.isfile("kill%s.py" % self.jobId):
                os.remove("kill%s.py" % self.jobId)
            if os.path.isfile("atrm%s.py" % self.jobId):
                os.remove("atrm%s.py" % self.jobId)
            if os.path.isfile(self.cfgfile):
                os.remove(self.cfgfile)              
        else:
            if os.path.isfile("kill%s.py" % self.jobId):
                os.remove("kill%s.py" % self.jobId)
                
        print "done."


# -- main ----------------------------------------------------------------------

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
    parser.add_option("-i", "--jobId", dest="jobId", type="str", default='',
                       help="job id")
    parser.add_option("-m", "--masternode", dest="masterNode", type="str", default='',
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
    job.setMasterNode(options.masterNode) # le defaut valant '' => ok
    
    if options.usegui:
        job.menu()
    else:
        job.run()
        


            
            
