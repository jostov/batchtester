#!/usr/bin/python
#
# This is a script for splitting an HMI data set into partitioning and 
# kfolded data sets. This is intened solely for use at RAP-BIDAL lab.  
#
# The expected output is a folder of partitioned data, two files for
# each fold, one testing and one training, as well as a parameter file
# for the entire dataset. The name of the folder is the name of the
# text file that will be partitioned.
#
# Example use:
#
#    python kcross.py somefile.txt .... nfiles.txt [-plkoOc]
#
# Arguments are:
#
#   -pX where x is a decimal between 0 and 1, this is the portion of 
#       data to be used for param tuning. this can be a float. I swear
#       to god though if you fucking put an int here, that's some serious fuckerydoo.
#   
#   -l  activates classifier mode
#
#   -kZ where z is an integer, this is the number of partitions to 
#       be used. how the fuck is it even supposed to make a float sized
#       partition anyways, well i guess it could just be a fraction of
#       the main thing or whatever. I guess it could work, except it won't
#       so frig the fuck off.
#
#   -o=DIR where DIR is an output directory. If it does not exist it 
#       will be created. of course it fucking goes there, where else would it go?
#
#   -O=SOMEFILE where somefile is the desired xls output file for results. Overwrites
#      on collision, defaults to /dev/null/
#
#   -c=CLASSIFIER where classifier is the desired classifier, new classifiers and options
#      can be added to the classifier dict object. Working on a way to pass arguments to the
#      classifier through command line
#
#   -n=NAME where name is the name of the person to be put in the header
#   
#   -B activates batch mode, which is for running experiments on pre-split data
#      this should not be attempted with -l on. If you are running this program
#      with this command flag, file arguments should point to folders with pre-split
#      data in them.
#
#
#
# Authors: Joseph Overbeck <joverbeck@mail.sfsu.edu> THE most mediocre!!!!
#          Andrew Scott <ats@mail.sfsu.edu>
# Contributor: Diana Chu
# Computer Science Department, SFSU
# Copyright (C) 2016 SFSU
#
# Distributed under terms of the MIT license.
# 
