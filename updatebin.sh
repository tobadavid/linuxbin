#!/bin/sh
echo "===== updating local bin..."
#svn update ~/bin
cd ~/bin ; git pull
echo "===== updating blueberry..."
#ssh blueberry 'svn update ~/bin'
ssh blueberry 'cd ~/bin ; git pull'
echo "===== updating thorgal..."
#ssh thorgal 'svn update ~/bin'
ssh thorgal 'cd ~/bin ; git pull'
echo "===== updating fabulous..."
#ssh fabulous 'module load subversion ; svn update ~/bin'
ssh fabulous 'cd ~/bin ; git pull'
echo "===== updating spring..."
#ssh spring 'svn update ~/bin'
ssh spring 'cd ~/bin ; git pull'
echo "===== done."

