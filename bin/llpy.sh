#!/bin/bash
help_info='Usage ./llpy.sh input output'
if [ $# -lt 2 ]; then
	echo Only $# arguments given
	echo $help_info
	exit
fi
if [ ! -f $1 ]; then
	echo 'File 1 does not exist'
	echo $help_info
	exit
fi
echo >$2
if [ ! -f $2 ]; then
	echo 'File 2 does not exist'
	echo $help_info
	exit
fi
prv_path=$(pwd)
cd ../src/infer
f1_path=$1
if [ ! -f $1 ]; then
	f1_path=${prv_path}/$1
fi
f2_path=$2
if [ ! -f $2 ]; then
	f2_path=${prv_path}/$2
fi
python3 llpy.py <$f1_path >$f2_path
cd ${prv_path}
