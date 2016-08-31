import numpy as np
import scipy.stats as sp
from math import exp, pi, sqrt
class Classifier(object):
  def __init__(self):
    self.Classes = {}
   
  def fit(self, training_vectors, training_labels):
    training_data =  {}
    for i in range(len(training_vectors)):
      if training_labels[i] in training_data:
        training_data[training_labels[i]].append(training_vectors[i])
      else:
        training_data[training_labels[i]] = [training_vectors[i]]
        
    for each in training_data:
      self.Classes[each] = []
      self.Classes[each].append(np.mean(training_data[each], axis=0))
      self.Classes[each].append(np.std(training_data[each], axis=0))

  def predict(self, test_vector):
    k = [1, 0, None]
    for each in self.Classes:
      k[0] = 1
      for i in range(len(test_vector[0])):
        k[0] *= self.normpdf(test_vector[0][i], self.Classes[each][0][i], self.Classes[each][1][i])
      if k[0] >= k[1]:
        k[2] = each
        k[1] = k[0]
      k[0] = 1
    return k[2] 

  def normpdf(self, x, mu, sigma):
    u = (float(x)-mu)/abs(sigma)
    y = (1.0/(sqrt(2.0*pi)*abs(sigma)))*exp(-u*u/2.0)
    return y
