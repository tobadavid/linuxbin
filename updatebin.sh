#!/bin/sh
echo "===== updating local bin..."
cd ~/bin ; git pull
echo "===== updating blueberry..."
ssh blueberry 'cd ~/bin ; git pull'
echo "===== updating thorgal..."
ssh thorgal 'cd ~/bin ; git pull'
echo "===== updating fabulous..."
ssh fabulous 'module load git ; cd ~/bin ; git pull'
echo "===== updating spring..."
ssh spring 'cd ~/bin ; git pull'
echo "===== done."
ssh gaston 'cd ~/bin ; git pull'
echo "===== done."

