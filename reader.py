# -*- coding: utf-8 -*-
"""
This module has two functions that read matlab file and generate required data
Created on Thu May 19 15:20:13 2022
@author: MShamas
"""

import scipy.io as scp
from Data_Manager import subFields_Dataset

def read_matlab_matrix(filename, variable_name):
    # filename: string containing full name of matlab file
    # variable_name: string that indicate the name of the variable that contains matlab structure
    # function returns a 3D matrix of form [RxRxNb] where R is number of Regions and Nb number of subjects
    mat_dic = {} # initialize empty  variable
    try: 
        mat_dic = scp.loadmat(filename)[variable_name]
    except OSError:
        print("could not read file: ", filename)
    except ValueError:
        print("please enter a .mat file")
    except KeyError:
        print("please enter a valid variable name")
    else:
        return mat_dic
    
def read_matlab_struct(filename,variable_name,field_names):
    # filename: string containing full nae of matlab file
    # variable_name: string that indicate the name of the variable that contains matlab structure
    # filed_names: list of filed names to read
    # function returns arrays of specified structure field names in struct_names
    
    # try to read the file
    try:
        mat_strct = scp.loadmat(filename)[variable_name]
    except OSError:
        print("could not read file: ", filename)
    except ValueError:
        print("please enter a .mat file")
    except KeyError:
        print("please enter a valid variable name")
    else:
        return mat_strct[field_names]

# to be deleted    
def main():
    filename = r"C:\Users\mshamas\Documents\Data\MRI_Conor\Patients_con.mat"
    patients = read_matlab_matrix(filename,'covariation_patients_subV')
    filename_labels = r"C:\Users\mshamas\Documents\Data\MRI_Conor\MRI_Data_noOutliers_withSubfields_Residuals.mat"
    labels = read_matlab_struct(filename_labels,'patients',['outcome','eeg_onset'])
    print(labels['eeg_onset'])
    eeg_onset = labels['eeg_onset']
    patients_dataset = subFields_Dataset(patients, eeg_onset)
    # Display image and label.
    print('\nFirst iteration of data set: ', next(iter(patients_dataset)), '\n')
    
if __name__ == "__main__":
    main()