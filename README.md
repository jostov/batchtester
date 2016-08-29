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

## Splitting a file.

In order to split a file, the syntax is as follows

```  
  python cheaptest.py -o="Path/To/Output/File" file1 [file2 ... fileN]
```  
 
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
 Some/Path/
    file1/
       file1kfold0_training.txt
       file1kfold0_testing.txt
       file1kfold1_training.txt
       file1kfold1_testing.txt
       file1kfold2_training.txt
       file1kfold2_testing.txt
       file1kfold3_training.txt
       file1kfold3_testing.txt
       file1kfold4_training.txt
       file1kfold4_testing.txt
       file1kfold5_training.txt
       file1kfold5_testing.txt
       file1kfold6_training.txt
       file1kfold6_testing.txt
       file1kfold7_training.txt
       file1kfold7_testing.txt
       file1kfold8_training.txt
       file1kfold8_testing.txt
       file1kfold9_training.txt
       file1kfold9_testing.txt
       file1_parameter_tuning.txt
```
  
## Testing a pre-split directory

In order to run a set of tests against the previously described  directory of split files, 
simply run the following command,

 ```
  python cheaptest.py Some/Path/file1/ -B -o="Some_output.xls" -c=GNB
 ```
The -c=CLASSIFIER argument specifies which classifier is to be used for the batch of tests, where
classifier is the key to that particular classifier's entry in the class_dictionary dictionary
More classifiers can be easily introduced to the script, by simply ensuring the following things 
are true about the classifier

  * The classifier class has the two following methods, fit(list_of_feature_vectors, list_of_class_labels)
    and also predict(feature_vector).

  * The classifier must have an entry in the dictionary, class_dictionary. To use the classifier, pass whatever
    key it has with the -c=KEY arguments




The -o argument is required as this program is built to run piles of files at once, rather than one file
at a time. By default, the file name is /dev/null.
  
Hmmm. As I write this, that seems like a terrible goddamn idea. Yeah, include that -o option every time.
Don't mess around with that.
  
## Quick Testing

As this was initially built just to do some quick testing with files without dealing with the parsing junk,
this script has the ability to test and directly output results without ever creating the batch of testing files.
Theoretically, the random number generator uses the same seed, and it does preserve its state between splitting the
files and testing the classifier, so it should still produce the same splits every time, however, order in which files
are passed as arguments, and runtime environment will affect the PNRG, so for effective comparison between classifiers
it is highly recommended that the user split the files, and then run the script on the split files, so that the data
set is the same for all tests. That being said, it does have this ability to quickly gauge the effectiveness of a classifier.

In order to use this unrecommended feature, use the following syntax


```
python cheaptest.py -l -o="outputfile" file1 file2
``` 

Note: You may use as many files as you like in a run. The arguments are unordered.

## All currently available command flags
 
```
  -pX where X is a decimal between 0 and 1, this is the portion of 
      data to be used for param tuning. This should either be a float or 0, 
      everything else is expected to break this.
    
  -l  activates the one off classifier testing mode.

  -kZ where Z is an integer, this is the number of partitions to create. Floats here will break everything.
      
  -o=DIR where DIR is an output directory. If it does not exist it 
      will be created. 

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
```

 
 
Authors: Joseph Overbeck <joverbeck@mail.sfsu.edu>

Contributors: Diana Chu, Andrew Scott

Copyright (C) 2016 Joseph Overbeck


Distributed under terms of the MIT license, right now at least.
  
