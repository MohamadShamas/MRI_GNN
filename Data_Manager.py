# -*- coding: utf-8 -*-
"""
Created on Fri May 20 12:18:23 2022

@author: MShamas
"""
import numpy
import torch
from torch.utils.data import Dataset, DataLoader

float_type = torch.float32  # Hardcoding datatypes for tensors
categorical_type = torch.long
labels_type = torch.float32 # Hardcoding datatype for labels


class Cont_Feat:
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return f'<ContinuousFeature: {self.name}>'

  def __eq__(self, other): 
    return self.name == other.name

  def __hash__(self):
    return hash(self.name)

class Cat_Feat:
  def __init__(self, name, values, add_null_value=True):
    self.name = name
    self.has_null_value = add_null_value
    if self.has_null_value:
      self.null_value = None
      values = (None,) + tuple(values)
    self.values = tuple(values)
    self.value_to_idx_mapping = {v: i for i, v in enumerate(values)}
    self.inv_value_to_idx_mapping = {i: v for v, i in self.value_to_idx_mapping.items()}
    
    if self.has_null_value:
      self.null_value_idx = self.value_to_idx_mapping[self.null_value]
   
  
  
  def get_null_idx(self): 
    if self.has_null_value:
      return self.null_value_idx
    else:
      raise RuntimeError(f"Categorical variable {self.name} has no null value")   
    
  def value_to_idx(self, value):
    return self.value_to_idx_mapping[value]
  
  def idx_to_value(self, idx):
    return self.inv_value_to_idx_mapping[idx]
  
  def __len__(self):
    return len(self.values)
  
  def __repr__(self):
    return f'<CategoricalFeature: {self.name}>'

  def __eq__(self, other):
    return self.name == other.name and self.values == other.values

  def __hash__(self):
    return hash((self.name, self.values))   
      
# Subfields Type
ANATOMY = [1, 2] # Hippocampus 1, Amygdala: 2
ANATOMY_FEATURE = Cat_Feat('anatomy', ANATOMY)
# Subfields Location i.e. right or left hemisphere
HEMISPHERE = [1, 2] # Right 1, Left 2
HEMISPHERE_FEATURE = Cat_Feat('Hemisphere', HEMISPHERE)
# combine in one list of features
FEATURES = [ANATOMY_FEATURE, HEMISPHERE_FEATURE]
  
#class subFields_Dataset(Dataset):
class subFields_Dataset(Dataset):
  def __init__(self, *, graphs, labels, node_var, edge_var):

    self.graphs = graphs
    self.labels = labels
    assert len(self.graphs) == len(self.labels), \
      "Graphs and labels lists must be the same length"
    self.node_var = node_var
    self.edge_var = edge_var
    self.cat_node_var = [var for var in self.node_var
                                       if isinstance(var, Cat_Feat)]
    self.cont_node_var = [var for var in self.node_var
                                      if isinstance(var, Cont_Feat)]
    self.cat_edge_var = [var for var in self.edge_var
                                       if isinstance(var, Cat_Feat)]
    self.cont_edge_var = [var for var in self.edge_var
                                      if isinstance(var, Cont_Feat)]   
    