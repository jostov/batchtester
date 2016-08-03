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
#    python kcross.py somefile.txt .... nfiles.txt
#
# Arguments are:
#
#   -pX where x is a decimal between 0 and 1, this is the portion of 
#       data to be used for param tuning. this can be a float. I swear
#       to god though if you fucking put an int here, that's some serious fuckerydoo.
#   
#   -l  l for l337 haxcor mode. 
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
# Authors: Joseph Overbeck <joverbeck@mail.sfsu.edu> THE BEST!!!!
#          Andrew Scott <ats@mail.sfsu.edu>
# Contributor: Diana Chu
# Computer Science Department, SFSU
# Copyright (C) 2016 SFSU
#
# Distributed under terms of the MIT license.
# 
# HAKT LOLOLOLOL
import os
import sys
import random
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostRegressor, RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from excelsterbator import Excelsterbator

params = {}
args = []
args = sys.argv
random.seed('BIDAL')

params['p'] = .266666
params['k'] = 10
params['o'] = ''
params['l'] = False #l33t haxx0r m0d3 l3l3l3l3l3l
classifier_dict = { 'Ada' : AdaBoostRegressor, #If ever implemented, this line is some fucking evil ass voodoo.
                  'GNB' : GaussianNB,
                  'RF' : RandomForestClassifier,
                  'GradBoost' : GradientBoostingClassifier,
                  'LDA' : LinearDiscriminantAnalysis }


# Parse out the arguments 
for each in args[1:]:      # for each arg
  if each.startswith('-'): # capture the flags
    k = args.pop(args.index(each)) # pop each arg

    # Parse command line options and record values
    try: 
      if k[1] is 'p':
        params[k[1]]=float(k[2:])
      elif k[1] is 'k':
        params[k[1]]=int(k[2:])
      elif k[1] is 'O':
        params[k[1]]=k[3:] if k[3:].endswith('.xls') else k[3:] + '.xls'
      elif k[1] is 'o':
        params[k[1]]=k[3:] if k[3:].endswith('/') else k[3:] + '/'
        # If an output folder was given set that up
        try:
          os.mkdir(params['o'])
        except OSError:
          pass

      elif k[1] is 'l':
        params[k[1]]=True
      else:
        print k + " is not a valid argument"
    except ValueError:
      print "something went horribly wrong. reexamine the documentation"
      quit()

# Providing user some information
print "Preserving " + str(params['p']*100) + \
  "% of segments for parameter tuning"
print "Partitioning data into " + str(params['k']) + " segments"
paths = args[1:]

thing = Excelsterbator(matrix_dictionary=None, output_path=params['O'])
# For each file 
for fp in paths:
  if not params['l'] and not os.path.isfile(fp):
    print fp + ' was not found. Skipping this.'
    continue
  print "attempting to setup k-cross validation partitioned data from " + fp

  if not params['l']:
    # Creating output directory 
    try:
      os.mkdir(params['o'] + fp[:-4])
    except OSError:
      print "directory and presumably data already exist for - " + fp
      print "skipping " + fp
      continue

  # Parsing file
  data = {}
  for each in open(fp, "r").readlines():
    key = str(each).split()[0]
    if key not in data:
      data[key] = []
    if key in data:
      a = [float(x) for x in each.split()[1:-1]]
      a.append(each.split()[-1])
      data[key].append(a)

  # Separating out parameter tuning data
  parameter_tuning = {}
  new_data = {}
  prev = {}
  for each in data:
    parameter_tuning[each] = []
    new_data[each] = []
    random.shuffle(data[each])
    parameter_tuning[each]= data[each][:int(round(params['p'] * \
      len(data[each]),0))]
    new_data[each]= data[each][int(round(params['p'] * len(data[each]),0)):]
    prev[each] = 0

  # Write parameter tuning data
  data = new_data
  if params['l'] is False:
    with open(params['o'] + fp[:-4]+ "/"+ fp[:-4] + \
      "_parameter_tuning.txt", "a") as f:
      for each in sorted(parameter_tuning.keys()):
        for i in parameter_tuning[each]:
          f.write(each +"\t"+"\t".join(map(str, i))+ "\n")

  first_index = 0
  partition = {}
  cumulative_data = np.zeros([len(data),len(data)])
  fold_matrices = {}
  # Writing K-folded data set
  for i in range(params['k']):
    testing = {}
    training= {}

    # Splitting Training and test data
    for each in data:
      partition[each] = (i+1) * len(data[each]) / params['k']
      testing[each] = data[each][prev[each]:partition[each]]
      training[each] = data[each][:prev[each]] + data[each][partition[each]:]

    # Updating slice indices
    for each in partition:
      prev[each] = partition[each]

    if params['l'] is False:
      # Writing training data
      with open(params['o'] + fp[:-4]+ "/"+ fp[:-4] + "kfold" + str(i) +"_training.txt", "a") as f:
        nu = '\n'
        for each in sorted(training.keys()):
          for j in training[each]:
            f.write(each +"\t"+"\t".join(map(str, j))+ nu)
      # Writing testing data
      with open(params['o'] + fp[:-4]+ "/"+ fp[:-4] + "kfold" + str(i) +"_testing.txt", "a") as f:
        nu = '\n'
        for each in sorted(testing.keys()):
          for j in testing[each]:
            f.write(each +"\t"+"\t".join(map(str, j))+ nu)

            
    ##l337 hacking
    if params['l'] is True:
      clf = AdaBoostClassifier()
      train = [[],[]]
      test = [[],[]]
      x=0
      matrix_key = {}
      for each in sorted(training):
        matrix_key[each] = x
        [train[1].append([float(z) for z in j[:-1]]) for j in training[each]]
        [train[0].append(j) for j in [each for k in range(len(training[each]))]]
        x += 1

    
      print matrix_key
      train1 = np.array(train[0])
      train2 = np.array(train[1])
      clf.fit(train2 , train1)
      test_list = np.zeros([len(matrix_key), len(matrix_key)])
      z = 0
      q = 0
      for j in testing:
        for each in testing[j]:
          ach = np.array(each[:-1])
          prediction = matrix_key[clf.predict(ach.reshape(1,-1))[0]]
          actual = matrix_key[j]
          test_list[actual, prediction] +=1 
          if actual == prediction:
            q +=1
          z += 1
          
      fold_matrices['K-fold ' +str(i)] = test_list
      print float(q)/z
      cumulative_data += test_list


  print cumulative_data
  fold_matrices['Cumulative'] = cumulative_data
  thing.calculate_all_matrices(fold_matrices)
  thing.output_data(os.path.split(fp)[1][:30])
  #for each in fold_matrices:
    #print each
    #print fold_matrices[each]
  print "Successfully partitioned " + fp
thing.fin()
