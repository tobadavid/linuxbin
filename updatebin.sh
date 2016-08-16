#!/bin/sh
echo "===== updating local bin..."
svn update ~/bin
echo "===== updating blueberry..."
ssh blueberry 'svn update ~/bin'
echo "===== updating thorgal..."
ssh thorgal 'svn update ~/bin'
echo "===== updating fabulous..."
ssh fabulous 'module load subversion ; svn update ~/bin'
echo "===== updating spring..."
ssh spring 'svn update ~/bin'
echo "===== done."

