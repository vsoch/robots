#!/bin/bash

# Change color of existing image based on R,G,and B scale
# factors

#########################################################
# Inputs
#########################################################

# make sure all command line arguments are actually given
if [ -z $1 ] || [ -z $2 ] || [ -z $3 ] || [ -z $4 ] || [ -z $5 ]
then 
   echo "Usage: $0 <input file> <output file> <Rscale> <Gscale> <Bscale>"
   exit 0
fi

# make sure the input file is a real file
if [ ! -e $1 ]
then
   echo "Input file '$1' does not exist"
   exit 0
fi

# make sure the input file can be read by us
if [ ! -r $1 ]
then
   echo "Input file '$1' cannot be opened for reading"
   exit 0
fi

# if the output file exists, make sure that we can write to it
if [ -e $2 ]
then
   if [ ! -w $2 ]
   then
      echo "Output file '$2' cannot be opened for writing"
      exit 0
   fi
fi

infile=$1
outfile=$2
Rscale=$3
Gscale=$4
Bscale=$5

convert -recolor \
   " ${Rscale}, 0, 0, 0, 0,   \
     0, ${Gscale}, 0, 0, 0,   \
     0, 0, ${Bscale}, 0, 0,   \
     0, 0, 0, 1, 0,   \
     0, 0, 0, 0, 1"   \
     $infile $outfile
