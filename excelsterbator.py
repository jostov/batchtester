import pandas as pd
import numpy as np
import xlsxwriter 
#This is a class to manage the creation of excel files
#conforming to the standards of the RAP-BIDAL group
class Excelsterbator(object):
  #instantiation
  def __init__(self, matrix_dictionary=None, output_path=None, dims=None, class_dictionary=None):
    if dims is None and matrix_dictionary is not None:
      dims = len(matrix_dictionary[matrix_dictionary.keys()[0]])
      print dims
    if output_path is None:
      print "Some shit went horribly wrong, i need an output path"
      print "Dropping this process like hot fire"
      quit()
    else:
      self.output_path= output_path
    if matrix_dictionary is not None:
      if class_dictionary is None:
        self.class_dictionary = {}
        for i in range(dims):
          self.class_dictionary[i] = i
      else:
        self.class_dictionary = class_dictionary
      self.matrix_dictionary = matrix_dictionary
      self.binary_matrices = {}
      self.dims = dims
    self.writer = pd.ExcelWriter(self.output_path, engine='xlsxwriter')

  #It's called calculate all matrices.
  #Take a wild fucking guess as to what it does.
  #No, really.
  def calculate_all_matrices(self, matrix_dictionary, dims=None, class_dictionary=None):
    if dims is None:
      dims = len(matrix_dictionary[matrix_dictionary.keys()[0]])
    if class_dictionary is None:
      self.class_dictionary = {}
      for i in range(dims):
        self.class_dictionary[i] = i
    else:
      self.class_dictionary = class_dictionary
    self.matrix_dictionary = matrix_dictionary
    self.binary_matrices = {}
    self.dims = dims
    for each in self.matrix_dictionary:
      self.binary_matrices[each] = self.calculate_binary_matrices(self.matrix_dictionary[each])


  #Calculate all the binary confusion matrices
  def calculate_binary_matrices(self, matrix):
    binary_matrices = {}
    for each in sorted(self.class_dictionary):
      a = self.calculate_binary_matrix(matrix, each)
      binary_matrices[each] = a
    return binary_matrices

  #Calculates the binary confusion matrix from
  #of a given class from the multiclass confusion matrix
  def calculate_binary_matrix(self, matrix, chosen_class):
    a = self.class_dictionary[chosen_class]
    cols = ['PP', 'PN']
    rows = ['AP', 'AN']
    binary = np.zeros([2,2])
    binary[0,0] = matrix[a][a]
    binary[0,1] = sum([matrix[i][a] for i in range(self.dims)]) - binary[0][0]
    binary[1,0] = sum(matrix[a]) - binary[0][0]
    binary[1,1] = sum([sum(matrix[i]) for i in range(self.dims)]) \
        - binary[0,0] - binary[1,0] - binary[0,1]
    bina = pd.DataFrame(np.transpose(binary), index=cols, columns=rows)
    row = ['Accuracy', 
                'Pos Accuracy',
                'Neg Accuracy',
                'Sensitivity',
                'Specificity']
    cols = [ 'class ' + str(chosen_class)]
    bintts =  [ (binary[0,0] + binary[1,1] )/ float(binary[0,0] + binary[0,1] + binary[1,0] + binary[1,1]),
                binary[0,0] / float(binary[0,0] + binary[0,1]),
                binary[1,1] / float(binary[1,0] + binary[1,1]),
                binary[0,0] / float(binary[1,0] + binary[0,0]),
                binary[1,1] / float(binary[1,1] + binary[0,1])]
    binatts = pd.DataFrame(bintts, index=row, columns=cols)

    return (bina, binatts)

  #This configures header information, it is non functional right now
  def config_header(self, name, data_set, classifier):
    self.name = name
    self.data_set = data_set
    self.classifier = classifier

  #This outputs data into the spreadsheet, it should be putting things in several different
  #sheets, but it is not, so it must be fixed at some point
  def output_data(self, sheet):
    indices=[0,0]
    k = self.binary_matrices.keys()
    if 'Cumulative' in k:
      k.remove('Cumulative')
      k.insert(0, 'Cumulative')
    for each in k:
      col = ['P' + str(i) for i in self.class_dictionary.keys()]
      row = ['A' + str(i) for i in self.class_dictionary.keys()]
      sensitivities = {}
      predictivities = {}
      acc = [0,0]
      curmat = np.array(self.matrix_dictionary[each])
      for i in self.class_dictionary:
        sensitivities[i] = curmat[i][i] /float(sum(curmat[:,i]))
        predictivities[i] = curmat[i][i] /float(sum(curmat[i,:]))
        acc[0] += curmat[i][i]
        acc[1] += sum(curmat[i, :])
      sensitivities_index = [str(i) + ' sensitivity' for i in sorted(sensitivities)] + ['Accuracy']
      sensitivitys = [sensitivities[i] for i in sorted(sensitivities)] + [acc[0]/float(acc[1])]
      #pd.DataFrame(data=[sensitivities[i] for i in sorted(sensitivities)], index=[str(i) + ' sensitivity' for i in sorted(sensitivities)]).to_excel(self.writer, sheet_name=sheet, startrow=indices[0], startcol=indices[1])
      pd.DataFrame(data=sensitivitys, index=sensitivities_index).to_excel(self.writer, sheet_name=sheet,  startrow=indices[0]+1, startcol=indices[1])
      pd.DataFrame(data=[predictivities[i] for i in sorted(predictivities)], index=[str(i) + ' predictivity' for i in sorted(predictivities)]).to_excel(self.writer, sheet_name=sheet, startrow=indices[0]+1, startcol=indices[1]+2)
      #pd.DataFrame(data=[acc[0]/float(acc[1])], columns=['Accuracy']).to_excel(self.writer, sheet_name=sheet, startrow=indices[0], startcol=indices[1] + 5)

      pd.DataFrame(np.array(['']), index=[''], columns=[str(each) + ' MultiClass']).to_excel(self.writer, sheet_name=sheet, startrow=indices[0], startcol=indices[1])
      a = pd.DataFrame(np.transpose(curmat), index=col, columns=row)
      a.to_excel(self.writer, sheet_name=sheet, startrow=indices[0], startcol=indices[1]+4)
      #ran = xlsxwriter.utility.xl_range(indices[0]+1, indices[1]+5, indices[0]+self.dims, indices[1]+4+self.dims)
      #print ran
      indices[0] += self.dims + 4
      #self.writer.sheets[sheet].conditional_format(ran, {'type': '3_color_scale'})
      for j in self.binary_matrices[each]:
        self.binary_matrices[each][j][1].to_excel(self.writer, sheet_name=sheet,startrow=indices[0], startcol=indices[1] )
        self.binary_matrices[each][j][0].to_excel(self.writer, sheet_name=sheet,startrow=indices[0] +1 , startcol=indices[1] + 3)
        indices[0] += 7

    workbook = self.writer.book
    worksheet = self.writer.sheets[sheet]
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 20)
  def fin(self):
    self.writer.save()
    print 'this shit got called at least'


if __name__ == '__main__':
  a = {'fold1' : [[1,0,0,3],\
       [0,1,0,0],\
       [0,0,1,0],\
       [2,0,0,1]]}
  for each in a['fold1']:
    print each
  thing = Excelsterbator(a, output_path='output.xls')
  thing.calculate_all_matrices()
  thing.output_data()
  for each in thing.binary_matrices:
    for i in thing.binary_matrices[each]:
      print "class is " + str(i)
      print thing.binary_matrices[each][i]


'''
  b = pd.DataFrame(np.array(a))
  output_path = 'test_excel.xls'
  writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
  b.to_excel(writer, sheet_name='Sheet1',startrow=2, startcol=2)
'''
