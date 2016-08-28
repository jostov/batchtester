# Batchtester.py
  Though this is named batchtester.py, the main file here is actually
  cheaptest.py. This script is built for the management of BIDAL datasets
  and also as a basic python testbed for classifiers. This script operates
  in three primary ways. First, it can be used to generate a partitioned
  and appropriately mutilated data-set for k-cross validation and 
  parameter tuning. The second mode of operation is more for quick and dirty
  testing, it turns a file into the partitioned dataset, runs a classifier
  against all the folds, outputs the results of the tests to an excel file
  and throws out all the resulting partitioned files. The final way this
  script can be run is as a standalone testing script, this requires the
  files to be split up by this script being run in the first way. It will
  also output its testing results to an excel file. It is strongly
  recommended that only the first and third modes be used, for the sake of
  experimental consistency. Using the second mode in any serious
  experimental capacity seems grotesquely wrong and wildly innappropriate
  for anything official.

# Splitting a file.

  In order to split a file, the syntax is as follows
  
  python cheaptest.py -o="Path/To/Output/File" file1 [file2 ... fileN]
 
  By default this will split up the data into the following portions.
  Firstly, it will remove 26% of the samples and preserve them as parameter
  tuning data. This can be changed with the -pN flag, where N is some float
  between 0 and 1.

  Additionally, by default, it splits the dataset up into ten different
  partitions and creates ten different  training/testing set using each 
  partition as the testing set, and the remaining partitions as the training
  set for that particular testing/training pair. The partition sizing can
  be changed quite easily with the -kN flag, where N is some integer greater
  than 0 and less than the number of samples remaining after partition.

  Using this command,
```
  python cheaptest.py -o="Some/Path" file1
```

  produces the following output directories
```
 -Some/Path/
    -file1/
       -file1kfold0_training.txt
       -file1kfold0_testing.txt
       -file1kfold1_training.txt
       -file1kfold1_testing.txt
       -file1kfold2_training.txt
       -file1kfold2_testing.txt
       -file1kfold3_training.txt
       -file1kfold3_testing.txt
       -file1kfold4_training.txt
       -file1kfold4_testing.txt
       -file1kfold5_training.txt
       -file1kfold5_testing.txt
       -file1kfold6_training.txt
       -file1kfold6_testing.txt
       -file1kfold7_training.txt
       -file1kfold7_testing.txt
       -file1kfold8_training.txt
       -file1kfold8_testing.txt
       -file1kfold9_training.txt
       -file1kfold9_testing.txt
       -file1_parameter_tuning.txt
```
  
# Testing a pre-split directory
  
  

# Example use:
 
     python cheaptest.py somefile.txt .... nfiles.txt [-plkoOc]
 
#  Arguments are:
 
    -pX where x is a decimal between 0 and 1, this is the portion of 
        data to be used for param tuning. this can be a float. I swear
        to god though if you fucking put an int here, that's some serious fuckerydoo.
    
    -l  activates classifier mode
 
    -kZ where z is an integer, this is the number of partitions to 
        be used. how the fuck is it even supposed to make a float sized
        partition anyways, well i guess it could just be a fraction of
        the main thing or whatever. I guess it could work, except it won't
        so frig the fuck off.
 
    -o=DIR where DIR is an output directory. If it does not exist it 
        will be created. of course it fucking goes there, where else would it go?
 
    -O=SOMEFILE where somefile is the desired xls output file for results. Overwrites
       on collision, defaults to /dev/null/
 
    -c=CLASSIFIER where classifier is the desired classifier, new classifiers and options
       can be added to the classifier dict object. Working on a way to pass arguments to the
       classifier through command line
 
    -n=NAME where name is the name of the person to be put in the header
    
    -B activates batch mode, which is for running experiments on pre-split data
       this should not be attempted with -l on. If you are running this program
       with this command flag, file arguments should point to folders with pre-split
       data in them.
 
 
 
  Authors: Joseph Overbeck <joverbeck@mail.sfsu.edu> THE most mediocre!!!!
           Andrew Scott <ats@mail.sfsu.edu>
  Contributor: Diana Chu
  Computer Science Department, SFSU
  Copyright (C) 2016 SFSU
 
  Distributed under terms of the MIT license.
  
