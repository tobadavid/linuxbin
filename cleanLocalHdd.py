#!/usr/bin/env python
# -*- coding: latin-1; -*-
#
# Script cleanLocalHdd.py : listing de l'utilisation et nettoyage des disques locaux sur le cluster
#

import os, sys, subprocess

def listByUser(user, nodesList):
    print "listing local disk use for user %s"%user
    print "\t on nodes : %s"%nodesList

    global nbnodes
    outFN = 'listLocalHddUse.out'
    out = open(outFN, "w")
    # ignore ne marche pas !!! (ai essayé toutes les combinaisons)
    #cmd1 = "ls -ldh /local/%s* --ignore='/local/lost+found'" %user
    cmd1 = "ls -ldh /local/%s*" %user
    cmd2 = "du -sh /local/%s* --exclude /local/lost+found " %user

    cmd="%s; %s"%(cmd1,cmd2)
    print cmd
    for inode in nodesList:
        print "\n\tNode%03d\n\t========"%(inode)
        sshCmd  = "ssh node%03d '%s'"%(inode, cmd)
        callOut =  subprocess.call(sshCmd, shell=True)

def delByUser(user, nodesList):
    print "deleting local disk dirs for user %s"%user
    print "\t on nodes : %s"%nodesList

    sure = raw_input("are you sure ? (yes/No) : ")
    if sure=='' or sure.lower()!="yes":
        print "Aborted ..."
        return
    global nbnodes
    outFN = 'listLocalHddUse.out'
    out = open(outFN, "w")

    cmd2 = "rm -rf /local/%s*" %user
    print cmd2
    for inode in nodesList:
        print "\tNode%03d"%(inode)
        cmd  = "ssh node%03d '%s'"%(inode, cmd2)
        callOut =  subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    nbnodes = 14
    nodesList = range(1,nbnodes+1)

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="user", type="str",
                      default=os.getenv('USER'),
                      help="user name for listing or deletion. \"-u ''\" for all users")
    parser.add_option("-F", "--force", dest="force",
                      default=False, action="store_true",
                      help="force deletion for multi users or nodes")

    parser.add_option("-c", "--clean", dest="clean",
                      default=False, action="store_true")
    parser.add_option("-n", "--nodes", dest="nodesList", type="int",
                      action="append", help="number of nodes to check (multiple nodes allowed: -n 1 -n 3 ...)")


    (options, args) = parser.parse_args()
    print "options.nodesList=",options.nodesList

    if options.nodesList:
       nodesList = options.nodesList

    if options.clean == True:
        if (options.user == '' or not options.nodesList)and options.force==False:
            print "Error deleting for all users or on all nodes not allowed without --force option"
        else:
            delByUser(options.user, nodesList)
    else:
        listByUser(options.user, nodesList)

