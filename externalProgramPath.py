#!/usr/bin/env python
# -*- coding: latin-1; -*-
# $Id: externalProgramPath.py 2645 2016-05-12 06:29:38Z boman $
#
#
# Define externals program path according to local configuration
# 
from prmClasses import *
import os, os.path, distutils.spawn

class ExtProgs(PRMSet):  
    def __init__(self,_verb=False):                     
        fname = 'metaforExtProgs.cfg'
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
        if isUnix():       
            # Mesh generation     
            TextPRM(self.pars,  'SAMCEF',      'Samcef',         'samcef')
            TextPRM(self.pars,  'GMSH',        'Gmsh',           'gmsh')        
            TextPRM(self.pars,  'TRIANGLE',    'Triangle',       'triangle')
            TextPRM(self.pars,  'TETGEN',      'Tetgen',         'tetgen')
            TextPRM(self.pars,  'ISOSURF',     'Isosurf',        'isosurf')
            # Post pro (curve plot,...)
            TextPRM(self.pars,  'MATLAB',      'Matlab',         'matlab')
            TextPRM(self.pars,  'SCILAB',      'Scilab',         'scilab')
            TextPRM(self.pars,  'GNUPLOT',     'GnuPlot',        'gnuplot')
            # other post
            TextPRM(self.pars,  'LATEX',       'Latex',          'latex')
            TextPRM(self.pars,  'GHOSTSCRIPT', 'GhostScript',    'gs')
            TextPRM(self.pars,  'IMAGEMAGICK', 'Image Magick',   'convert')            
        else : # windows
            # Mesh generation
            TextPRM(self.pars,  'SAMCEF',      'Samcef',        'samcef.cmd')   
            TextPRM(self.pars,  'GMSH',        'Gmsh',          'gmsh.exe')        
            TextPRM(self.pars,  'TRIANGLE',    'Triangle',      'triangle.exe')
            TextPRM(self.pars,  'TETGEN',      'Tetgen',        'tetgen.exe')
            TextPRM(self.pars,  'ISOSURF',     'Isosurf',       'isosurf.exe')                     
            # Post pro (curve plot,...)
            TextPRM(self.pars,  'MATLAB',      'Matlab',        'matlab.exe')
            TextPRM(self.pars,  'SCILAB',      'Scilab',        'scilex.exe')
            TextPRM(self.pars,  'GNUPLOT',     'GnuPlot',       'gnuplot.exe')
            # other post
            TextPRM(self.pars,  'LATEX',       'Latex',         'latex.exe')
            TextPRM(self.pars,  'GHOSTSCRIPT', 'GhostScript',   'gswin32c.exe')
            TextPRM(self.pars,  'IMAGEMAGICK', 'Image Magick',  'convert.exe')
            
    def checkValidity(self, key):
        if distutils.spawn.find_executable(os.path.splitext(self.pars[key].val)[0]) :
            return True
        else :
            print "%s is not found (%s)...."%self.pars[key].val
            print "\t Check installation and accessibility..."        
            print "\t Use 'externalProgramPathGui' to define the full program path (recommanded)" 
            print "\t or add %s in your user path (not recommanded)"%key
            return False
        
    def configAction(self):
        # 
        PRMAction(self.actions, 'a', self.pars['SAMCEF']) 
        PRMAction(self.actions, 'b', self.pars['GMSH']) 
        PRMAction(self.actions, 'c', self.pars['TRIANGLE']) 
        PRMAction(self.actions, 'd', self.pars['TETGEN']) 
        PRMAction(self.actions, 'e', self.pars['ISOSURF']) 
        NoAction(self.actions)
        PRMAction(self.actions, 'f', self.pars['MATLAB']) 
        PRMAction(self.actions, 'g', self.pars['SCILAB']) 
        NoAction(self.actions)
        PRMAction(self.actions, 'h', self.pars['LATEX']) 
        PRMAction(self.actions, 'i', self.pars['GHOSTSCRIPT']) 
        PRMAction(self.actions, 'j', self.pars['IMAGEMAGICK']) 
        NoAction(self.actions)
        SaveAction(self.actions , 'S')
        QuitAction(self.actions , 'Q')
            
#=================================================================================
def main():
    progsConf = ExtProgs() #verb=True)
    progsConf.configAction()
    progsConf.menu()


if __name__ == "__main__":

    try:
        import signal  
        signal.signal(signal.SIGBREAK, sigbreak);
    except:
        pass
    main()
