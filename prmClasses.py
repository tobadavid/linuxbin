# -*- coding: latin-1; -*-
# $Id: prmClasses.py 2645 2016-05-12 06:29:38Z boman $
#
#
# Classe de gestion des parametres


import sys, os, os.path, shutil, socket, platform, glob, fnmatch
import datetime, tarfile, subprocess

try:
    # enable path completion in raw_input()
    import readline
    readline.set_completer_delims(' \t\n`~!@#$%^&*()-=+[{]}\\|;:\'",<>?') # enleve le "/" qui empeche la completion de repertoires
    readline.parse_and_bind("tab: complete")    
#except ImportError:        
#    import pyreadline as readline    
#    #readline.set_completer_delims(' \t\n`~!@#$%^&*()-=+[{]}\\|;:\'",<>?') # enleve le "/" qui empeche la completion de repertoires
    readline.parse_and_bind("tab: complete")
except:
    pass  
    
# Parameters Set
class PRMSet:
    def __init__(self,cfgfile, _verb=False):    
        self.debug = _verb
        self.pars={}
        self.actions=[]
        self.cfgfile=cfgfile
        self.setDefaultPars()
        self.loadPars()
 
    def setDebug(self,_verb = True):
        self.debug = _verb      
 
    def printPars(self):
        for k,v in self.pars.items():
            print ("pars['%s'].val=%s\n" % (k,repr(v.val)) )        
    def loadPaths(self):
        return [os.path.abspath('.')]
    def savePath(self):
        return os.path.abspath('.')    
    def savePars(self, pth=None):
        if pth==None :
            pth  = self.savePath()
        fname = os.path.join(pth, self.cfgfile)
        file = open(fname,"w")        
        for k,v in self.pars.items():
            file.write("self.pars['%s'].val=%s\n" % (k,repr(v.val)) )
        file.close()            
    def loadPars(self): # lecture dans les chemins par defaut
        for pth in self.loadPaths():      
            fname = os.path.join(pth, self.cfgfile)
            if  (os.path.isfile(fname)):
                file = open(fname,"r")
                if file:                    
                    cmds = file.readlines() 
                    for cmd in cmds:
                        try:
                            exec cmd
                        except:
                            pass
                file.close()
                break                
            
    def setDefaultPars(self):
        print "PureVirtual Class PRMSet"
        
    def applyDependencies(self):
        # no dependencies
        return 
        
    def configActions(self):
        # no actions to configure
        return 
        
    def menu(self):
        msg=""
        while True:
            self.configActions()
            cls()
            print "Actions:"
            for act in self.actions:
                if act.enabled():
                    act.disp()
            print msg.rjust(78)
            print "Your choice?",  
            c = getch()
            #print c,
            if c!='':
                acts = [ a for a in self.actions if (a.key==c and a.enabled()) ]
                if len(acts)==1:
                    action = acts[0]
                    action.execute(self)
                    msg=""
                elif len(acts)==0:
                    msg="action is disabled or not found (command='%s')!"%c                    
                else:
                    msg= "%d actions found (command='%s')!" % (len(acts),c)
            self.applyDependencies()  
            
# -- Parameters Classes --
class PRM:
    def __init__(self, set, key, desc, defval):
        self.key    = key
        self.desc   = desc
        self.defval = self.typecheck(defval)
        self.val    = self.typecheck(defval)
        set[key]    = self
        self.enabled = True
    def typecheck(self, val): pass 
    def enable(self, cond):
        self.enabled = cond  
    def updateDepend(self): pass
        
class TextPRM(PRM):
    def __init__(self, set, key, desc, defval):
        PRM.__init__(self, set, key, desc, defval)
    def input(self):
        cls()
        #print "%s [def=%s]:" % (self.desc, self.defval)
        self.val = self.typecheck(raw_input())
        self.updateDepend()
    def typecheck(self, val):
        if type(val)!=str:
            return ""
        return val    

class YesNoPRM(PRM):
    def __init__(self, set, key, desc, defval):
        PRM.__init__(self, set, key, desc, defval)
    def input(self):
        self.val = not self.val 
        self.updateDepend()
    def typecheck(self, val):
        if type(val)==bool:
            return val
        elif val in ["yes", "on", "true"]:
            return True
        else:
            return False

class MultiPRM(PRM):
    def __init__(self, set, key, desc, vals, defval):
        self.vals = vals
        PRM.__init__(self, set, key, desc, defval)
    def input(self):
        i = self.vals.index(self.val)
        i = i+1
        if i>=len(self.vals): i=0
        self.val = self.vals[i] 
        self.updateDepend()
    def typecheck(self, val):
        if val in self.vals:
            return val
        return self.vals[0]

# -- Actions Classes (shell interface) --
class Action:
    def __init__(self, set, key):
        set.append(self) # add itself to the set
        self.key = key
    def disp(self): pass
    def execute(self,job): pass
    def enabled(self): return True
      
class PRMAction(Action):
    def __init__(self, set, key, prm):
        Action.__init__(self, set, key)
        self.prm = prm
        self.key = key
    def execute(self,job):
        self.prm.input()
    def disp(self):
        if not self.prm.enabled:
            ext = "[DISABLED]"
        else:
            ext = repr(self.prm.val)
        print " %s/ %s : %s" % (self.key, self.prm.desc.ljust(35,' '), ext)
    def enabled(self): return self.prm.enabled
        
class NoAction(Action):
    def __init__(self, set):
        Action.__init__(self, set, '')
    def disp(self):
        print
        
class QuitAction(Action):
    def __init__(self, set, key):
        Action.__init__(self, set, key)
    def execute(self,job):
        sys.exit()
    def disp(self):
        print " %s/ QUIT" % self.key
        
class GoAction(Action):
    def __init__(self, set, key):
        Action.__init__(self, set, key)
    def execute(self,job):
        job.go()
        sys.exit()
    def disp(self):
        print " %s/ GO" % self.key
        
class SaveAction(Action):
    def __init__(self, set, key):
        Action.__init__(self, set, key)
    def execute(self,job):
        job.savePars()
    def disp(self):
        print " %s/ SAVE" % self.key
        

        
# ----- from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/134892
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt
    def __call__(self):
        import msvcrt
        return msvcrt.getch()
# -- variables globales --
getch = _Getch()
#------------------------------------------------------------------------------  
# copied from oo_meta/toolbox/pyutils.py    
def isUnix():
    uname = platform.uname()
    return not (uname[0] == 'Windows' or uname[2] == 'Windows')

# copied from linuxbin/parametricJob.py  
def cls():
    uname = platform.uname()
    if uname[0] == 'Windows':
        os.system("CLS")
    else:
        os.system("clear")
        
def sigbreak(sig, arg):
    print "SIG-BREAK!"
    sys.exit()

def quit():
    sys.exit()
                 