#!/usr/bin/python
# Authors: Joseph Overbeck <joverbeck@mail.sfsu.edu>
#         
# Contributor: Diana Chu, Andrew Scott 
# Computer Science Department, SFSU
# Copyright (C) 2016 SFSU
#
# Distributed under terms of the MIT license.
# 
import importlib
import os
import sys
import random
import pandas as pd
import numpy as np
from batchtest import BatchTest
from excelsterbator import Excelsterbator


#This dictionary contains the command flag and associated module path
#of the currently available classifiers. Simply add an entry to this
#dictionary to add a new classifier to this program

#In order for a classifier to work with this program, it simply needs
#to have fit() and predict() methods with inputs similar to those implemented
#in the following classes
classifier_dict = { 'Ada' : 'sklearn.ensemble.AdaBoostClassifier',
                  'GNB' : 'sklearn.naive_bayes.GaussianNB',
                  'RF' : 'sklearn.ensemble.RandomForestClassifier',
                  'GradBoost' : 'sklearn.ensemble.GradientBoostingClassifier',
                  'SVC' : 'sklearn.svm.SVC',
                  'dumbayes': 'simplebayes.Classifier',
                  'dum' : 'dumdumherd.DumDumHerd',
                  'KNN' : 'sklearn.neighbors.KNeighborsClassifier',
                  'LDA' : 'sklearn.discriminant_analysis.LinearDiscriminantAnalysis'}

#Handles dynamic imports
for each in classifier_dict:
  try:
    b = importlib.import_module(''.join([j + '.' for j in classifier_dict[each].split('.')[:-1]])[:-1])
    classifier_dict[each] = getattr(b, classifier_dict[each].split('.')[-1])
  except ImportError:
    print each + " failed to import"

#Dictionary where runtime options are stored
params = {}
args = []
args = sys.argv

#Seeding random number generator with classy seed
random.seed('BIDAL')

params['p'] = .266666
params['k'] = 10
params['o'] = ''
params['O'] = '/dev/null'
params['l'] = False 
params['B'] = False 
params['c']  = 'GNB'
params['n']  = None

# Parse out the arguments 
for each in args[1:]:      # for each arg
  if each.startswith('-'): # capture the flags
    k = args.pop(args.index(each)) # pop each arg

    # Parse command line options and record values
    try: 
      if k[1] is 'p':
        if float(k[2:]) >= 1:
          print "Bad partition-value"
          quit()
        params[k[1]]=float(k[2:])
      elif k[1] is 'k':
        if int(k[2:]) <= 1:
          print "Bad k-fold value, this hurts me physically"
          quit()
        params[k[1]]=int(k[2:])
      elif k[1] is 'O':
        if k[2] is not '=':
          print "Args are formatted wrong"
          quit()
        params[k[1]]=k[3:] if k[3:].endswith('.xls') else k[3:] + '.xls'

      elif k[1] is 'n':
        if k[2] is not '=':
          print "Args are formatted wrong"
          quit()
        params[k[1]]=k[3:]

      elif k[1] is 'c':
        if k[2] is not '=':
          print "Args are formatted wrong"
          quit()
        if k[3:] in classifier_dict:
          params['c'] = k[3:]
        else:
          print "classifier not recognized"
      elif k[1] is 'o':
        if k[2] is not '=':
          print "Args are formatted wrong"
          quit()
        params[k[1]]=k[3:] if k[3:].endswith('/') else k[3:] + '/'
        # If an output folder was given set that up
        try:
          os.mkdir(params['o'])
        except OSError:
          pass

      elif k[1] is 'l':
        params[k[1]]=True

      elif k[1] is 'B':
        params[k[1]]=True
      #Not an argument and it was passed
      else:
        print k + " is not a valid argument"

    #This is the result when someone gives the wrong kind of data to an argument
    except ValueError:
      print "something went horribly wrong. reexamine the documentation"
      quit()

# Making the header, god, this is so ugly, why am I doing this like this?
# This shows a clear lack of style, sense, or even decency as a human being
# I hope nobody reads these comments.
if params['n'] is not None:
  lena_headley = { 'Name' : params['n'], #Name goes here
           'Classifier' : params['c']}
else:
  lena_headley = { 'Classifier' : params['c']}

# Providing user some information
print "Preserving " + str(params['p']*100) + \
  "% of segments for parameter tuning"
print "Partitioning data into " + str(params['k']) + " segments"
paths = args[1:]


#Create and hold excelsterbator object
excel_output = Excelsterbator(matrix_dictionary=None, output_path=params['O'], 
    header=lena_headley)
excel_output.set_classifier(params['c'])

state = None
# For each file 
for fp in paths:
  if not params['B']:
    basename = ''
    if state is not None:
      random.setstate(state)
    if not params['l'] and not os.path.isfile(fp):
      print fp + ' was not found. Skipping this.'
      continue
    print "attempting to setup k-cross validation partitioned data from " + fp

    if not params['l']:
      # Creating output directory 
      try:
        basename = params['o'] + '/' + os.path.split(fp)[-1][:-4]
        os.mkdir(basename)
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
      ffp = os.path.basename(fp)
      with open(basename+ "/"+ ffp[:-4] + \
        "_parameter_tuning.txt", "a") as f:
        for each in sorted(parameter_tuning.keys()):
          for i in parameter_tuning[each]:
            f.write(each +"\t"+"\t".join(map(str, i))+ "\n")

    first_index = 0
    partition = {}
    # Writing K-folded data set
    state = random.getstate()
    classifier = BatchTest(classifier_dict[params['c']], excelout=excel_output, output_location=params['O'])

  if params['B']:
    classifier = BatchTest(classifier_dict[params['c']], excelout=excel_output, output_location=params['O'])
    fp = fp if fp.endswith('/') else fp + '/'
    params['k'] = int(max(os.listdir(fp))[-14])+1
  for i in range(params['k']):
    testing = {}
    training= {}

    if not params['B']:
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
        with open(basename+ "/"+ ffp[:-4] + \
          "kfold" + str(i) + "_training.txt", "a") as f:
          nu = '\n'
          for each in sorted(training.keys()):
            for j in training[each]:
              f.write(each +"\t"+"\t".join(map(str, j))+ nu)
        # Writing testing data
        with open(basename+ "/"+ ffp[:-4] + \
          "kfold" + str(i) + "_testing.txt", "a") as f:
        #with open(params['o'] + fp[:-4]+ "/"+ fp[:-4] + "kfold" + str(i) +"_testing.txt", "a") as f:
          nu = '\n'
          for each in sorted(testing.keys()):
            for j in testing[each]:
              f.write(each +"\t"+"\t".join(map(str, j))+ nu)
        print "successfully partitioned " + fp
    if params['B']:
      if fp.endswith('/'):
        basename = os.path.split(fp[:-1])[1]
      else:
        basename = os.path.split(fp)[1]
        fp += '/'

      for each in open(fp + basename  + "kfold" + str(i) +"_training.txt", "r").readlines():
        key = str(each).split()[0]
        if key not in training:
          training[key] = []
        if key in training:
          a = [float(x) for x in each.split()[1:-1]]
          a.append(each.split()[-1])
          training[key].append(a)

      for each in open(fp + basename + "kfold" + str(i) +"_testing.txt", "r").readlines():
        key = str(each).split()[0]
        if key not in testing:
          testing[key] = []
        if key in testing:
          a = [float(x) for x in each.split()[1:-1]]
          a.append(each.split()[-1])
          testing[key].append(a)


    if params['B'] or params['l']:
      classifier.test(training, testing)
  if params['B'] or params['l']:
    classifier.to_excel(os.path.split(fp)[1])
    print "Successfully tested " + fp
excel_output.fin()
