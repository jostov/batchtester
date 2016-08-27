import pandas as pd
import numpy as np
import xlsxwriter 
# This is a class to manage the creation of excel files
# conforming to the standards of the RAP-BIDAL group
class Excelsterbator(object):

  # Creation of the Excelsterbator object
  # Accepts a matrix dictionary for some reason, the intention was to track
  # the names of matrix columns and rows. I'm not sure if it does that anymore
  def __init__(self, matrix_dictionary=None, output_path=None, dims=None, \
      class_dictionary=None, header=None):

    # Handling the default case for matrix configuration
    if dims is None and matrix_dictionary is not None:
      dims = len(matrix_dictionary[matrix_dictionary.keys()[0]])
      print dims

    # breaking appropriately
    if output_path is None:
      raise IOError("No file provided")
    
    # setting output path appropriately
    else:
      self.output_path = output_path
    
    # populating the matrix dictionary, because at one point I thought
    # it was an important thing. I'm really not quite sure now. wait,
    # there's a class dictionary? Hold up a sec.
    if matrix_dictionary is not None:
      if class_dictionary is None:
        self.class_dictionary = {}
        for i in range(dims):
          self.class_dictionary[i] = i

      else:
        # Who are you and why are you here
        self.class_dictionary = class_dictionary
      self.matrix_dictionary = matrix_dictionary
      self.binary_matrices = {}
      self.dims = dims

    self.header = header
    self.writer = pd.ExcelWriter(self.output_path, engine='xlsxwriter')

  # This is some janky shit that should never make it to github.
  # How do you branch shit?
  def set_classifier(self, classifier):
    self.classifier = classifier
    self.header = { "Name" : "Joseph Overbeck", \
               "Classifier" : classifier}

  # This gets the header.
  def get_header(self):
    return self.header

  # It's called calculate all matrices.
  # Take a wild fucking guess as to what it does.
  # No, really.
  def calculate_all_matrices(self, matrix_dictionary, dims=None, 
      class_dictionary=None):
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

    # It calculates all the matrices by the way, unless you hadn't 
    # guessed now
    for each in self.matrix_dictionary:
      self.binary_matrices[each] = self.calculate_binary_matrices(
                                   self.matrix_dictionary[each])


  # Calculate all the binary confusion matrices
  def calculate_binary_matrices(self, matrix):
    binary_matrices = {}
    for each in sorted(self.class_dictionary):
      a = self.calculate_binary_matrix(matrix, each)
      binary_matrices[each] = a
    return binary_matrices

  # Calculates the binary confusion matrix from
  # of a given class from the multiclass confusion matrix
  def calculate_binary_matrix(self, matrix, chosen_class):
    a = self.class_dictionary[chosen_class]
    cols = ['PP', 'PN']
    rows = ['AP', 'AN']
    binary = np.zeros([2,2])

    # Performs calculations for the binary class matrix
    binary[0,0] = matrix[a][a]
    binary[0,1] = sum([matrix[i][a] for i in range(self.dims)]) - binary[0][0]
    binary[1,0] = sum(matrix[a]) - binary[0][0]
    binary[1,1] = sum([sum(matrix[i]) for i in range(self.dims)]) \
        - binary[0,0] - binary[1,0] - binary[0,1]

    # Putting things in the appropriate place, and creating the appropriate
    # row and column labels
    bina = pd.DataFrame(np.transpose(binary), index=cols, columns=rows)
    row = ['Accuracy', 
                'Pos Accuracy',
                'Neg Accuracy',
                'Sensitivity',
                'Specificity']
    cols = [ 'class ' + str(chosen_class)]
    bintts =  [ (binary[0,0] + binary[1,1] )/ float(binary[0,0] + 
                binary[0,1] + binary[1,0] + binary[1,1]),
                binary[0,0] / float(binary[0,0] + binary[0,1]),
                binary[1,1] / float(binary[1,0] + binary[1,1]),
                binary[0,0] / float(binary[1,0] + binary[0,0]),
                binary[1,1] / float(binary[1,1] + binary[0,1])]
    binatts = pd.DataFrame(bintts, index=row, columns=cols)

    # Returns the binary matrix and labels.
    return (bina, binatts)

  # This configures header information, it is non functional right now
  # Just ignore it.
  # Are you ignoring it now? Ok, good.
  def config_header(self, name, data_set, classifier):
    self.name = name
    self.data_set = data_set
    # Wow, really? You disgust me.
    self.classifier = classifier

  # This outputs data into the spreadsheet, it should be putting things in 
  # several different sheets, but it is not, so it must be fixed at some 
  # point. It's fixed now. Everything is good.  Welcome to the future. 
  # Or look at the first part of this comment as a kind of time capsule
  def output_data(self, sheet):

    # Handle too long of names
    if len(sheet) > 30:
      sheet = sheet[:30]
     
    # Initializes indices for tracking write position on excel document
    indices=[0,0]
    k = self.binary_matrices.keys()
    
    # Labels appropriately in the case of the cumulative matrix
    if 'Cumulative' in k:
      k.remove('Cumulative')
      k = sorted(k)
      k.insert(0, 'Cumulative')

    header = self.get_header()
    header_data = pd.DataFrame([header[i] for i in header],
                               index=header.keys())
    header_data.to_excel(self.writer, sheet_name=sheet, startrow=indices[0], 
               startcol=indices[1])
    indices[0] += len(header.keys()) + 1
    # Performing the testing for each k-fold
    for each in k:
      # Creating labels for multi-class matrix
      col = ['P' + str(i) for i in self.class_dictionary.keys()]
      row = ['A' + str(i) for i in self.class_dictionary.keys()]
      sensitivities = {}
      predictivities = {}
      acc = [0,0]
      curmat = np.array(self.matrix_dictionary[each])

      # Calculates sensitivities and predictivities
      for i in self.class_dictionary:
        sensitivities[i] = curmat[i][i] /float(sum(curmat[:,i]))
        predictivities[i] = curmat[i][i] /float(sum(curmat[i,:]))
        acc[0] += curmat[i][i]
        acc[1] += sum(curmat[i, :])
      # Puts sensitivity values for each column into a dictionary and makes 
      # labels
      sensitivities_index = [str(i) + ' sensitivity' for i in 
                             sorted(sensitivities)] + ['Accuracy']
      sensitivitys = [sensitivities[i] for i in sorted(sensitivities)] + \
          [acc[0]/float(acc[1])]
      sensitivity_accuracy = pd.DataFrame(data=sensitivitys,
                                          index=sensitivities_index)

      # Ugly lines
      sensitivity_accuracy.to_excel(self.writer, sheet_name=sheet, 
          startrow=indices[0]+1, startcol=indices[1])

      # Puts predictivity values for each row into a dictionary and makes labels
      p_column1 = pd.DataFrame(data=[predictivities[i] for i in 
           sorted(predictivities)], index=[str(i) + ' predictivity' 
           for i in sorted(predictivities)])
      p_column1.to_excel(self.writer, sheet_name=sheet, startrow=indices[0]+1, 
                 startcol=indices[1]+2)

      # Multiclass label
      multiclass_label = pd.DataFrame(np.array(['']), index=[''], 
          columns=[str(each) + ' MultiClass'])
      multiclass_label.to_excel(self.writer, sheet_name=sheet, 
          startrow=indices[0], startcol=indices[1])
       
      # Multiclass matrix
      multiclass_matrix = pd.DataFrame(np.transpose(curmat), index=col, 
          columns=row)
      multiclass_matrix.to_excel(self.writer, sheet_name=sheet, 
          startrow=indices[0], startcol=indices[1]+4)

      # Predictivities columns
      p_column2 = pd.DataFrame([' ' for i in sorted(predictivities)], 
          index=[predictivities[i] 
          for i in sorted(predictivities)], columns=[''])
      p_column2.to_excel(self.writer, sheet_name=sheet, startrow=indices[0], 
          startcol=indices[1]+5+self.dims)
      indices[0] += self.dims + 1 

      try:
        s_row = pd.DataFrame(['' for i in sensitivitys], index=sensitivitys, 
            columns=['']).transpose()
        s_row.to_excel(self.writer, sheet_name=sheet, startrow=indices[0], 
            startcol=indices[1]+4)
      except ValueError:
        s_row.fillna('missing value')
        s_row.to_excel(self.writer, sheet_name=sheet, startrow=indices[0], 
            startcol=indices[1]+4)
        print g
      indices[0] += 3
      # self.writer.sheets[sheet].conditional_format(ran, {'type': 
       # '3_color_scale'})
      for j in self.binary_matrices[each]:
        self.binary_matrices[each][j][1].to_excel(self.writer,
            sheet_name=sheet, startrow=indices[0], startcol=indices[1] )
        self.binary_matrices[each][j][0].to_excel(self.writer, 
            sheet_name=sheet,startrow=indices[0] +1 , startcol=indices[1] + 3)
        indices[0] += 10

    #formatting the sheet
    workbook = self.writer.book
    worksheet = self.writer.sheets[sheet]
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 20)

  # Outputs and saves the sheet. Previously had inappropriate print statement
  # Now it says nothing.
  # The computers have been silenced.
  def fin(self):
    self.writer.save()

if __name__ == '__main__':
  print "This is not a standalone executable. Go elsewhere, do something else."


