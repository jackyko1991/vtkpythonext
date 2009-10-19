'''
Created on 2009-10-18

@author: Qiu wenfeng
'''
from jolly.jolly_vtk2.vtkPythonMetaDataSet import *
import vtk
import os

class vtkPythonMetaDataSetSequence(vtkPythonMetaDataSet):
    '''
    vtkMetaDataSetSequence
    @summary: This class is a powerfull vtk Addon class that helps handling a serie of vtkDataSets.
    
       vtkMetaDataSet has a flag of time, that allows this class to handle a sequence
       of different vtkMetaDataSet (of the same type), the output dataset (got from GetDataSet())
       can be updated to a specific time with UpdateToTime().
       
       It does not compute any time interpolation. 
    @see: vtkPythonMetaImageData vtkPythonMetaSurfaceMesh vtkPythonMetaVolumeMesh vtkPythonMetaDataset
        vtkPythonDataManager
    @license: Nicolas Toussaint, Qiu wenfeng
    @since: 2009-10-18
    '''


    def __init__(self):
        '''
        Constructor
        '''
        