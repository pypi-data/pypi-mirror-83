import pandas as pd
import numpy as np
import spacy
import sys

def load_spacy_data(file_path):
  file = open(file_path, 'r')
  start =0
  end = 0
  sentence,unique_labels,entities,training_data=[],[],[],[]
  for line in file:
    line=line.strip("\n").split("\t")
    if len(line)>1:
      label=line[1]
      if(label!='O'):
        label=line[1]+'_Disease'
      word = line[0]
      sentence.append(word)
      start = end
      end += (len(word) + 1)
    
      if label == 'I_Disease' :
        entities.append(( start,end-1, label))  # append the annotation
                              
      if label == 'B_Disease':                         
        entities.append(( start,end-1, label))# start annotation at beginning of word

      if label != 'O' and label not in unique_labels:
        unique_labels.append(label) 
  
    # lines with len == 1 are breaks between sentences
    if len(line) == 1:
      if(len(entities) > 0):
        sentence = " ".join(sentence)
        training_data.append([sentence, {'entities' : entities}])
        # reset the counters and temporary lists
        end = 0 
        start = 0
        entities, sentence = [], []  
  file.close()
  return training_data,unique_labels