import numpy as np
class BatchTest(object):
  def __init__(self, classifier, excelout, output_location):
    self.classifier = classifier
    self.out = excelout
    self.output_location = output_location
    self.matrices = {}
    self.iterations = 0

  #classifier is the key to whatever classifier in classifier_dict
  #that you want to test with
  #training and testing are dictionaries of BIDAL formatted feature vectors
  #Each key in the dictionary is associated with a class and the entry for 
  #that key is a list of feature vectors
  def test(self, training, testing, iter_label='K-Fold'):
    clf = self.classifier()
    train = [[],[]]
    test = [[],[]]
    x=0
    matrix_key = {}
    for each in sorted(training, key=int):
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
    self.matrices[iter_label + str(self.iterations)] = test_list
    if 'Cumulative' in self.matrices.keys():
      self.matrices['Cumulative'] += test_list
    else:
      self.matrices['Cumulative'] = test_list
    self.iterations += 1

  #Adds output to an excel sheet
  def to_excel(self, sheetname):
    self.out.calculate_all_matrices(self.matrices)
    self.out.output_data(sheetname)

