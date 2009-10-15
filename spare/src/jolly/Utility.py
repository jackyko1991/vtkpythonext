# -*- coding:utf-8 -*-
"""
Created on 2009-10-5

@author: summit
"""

from StateMachine import *
import itk

class ImageProcessingState:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name

class ImageProcessingInput:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name


ImageProcessingInput.Dir = ImageProcessingInput("Directory")
ImageProcessingInput.FileName = ImageProcessingInput("FileName")
ImageProcessingInput.Image = ImageProcessingInput("Image")
ImageProcessingInput.ITKImage = ImageProcessingInput("ITK Image")
ImageProcessingInput.VTKImage = ImageProcessingInput("VTK Image")
ImageProcessingInput.Numpy = ImageProcessingInput("numpy")

ImageProcessingState.Begin = ImageProcessingState("Begin")
ImageProcessingState.End = ImageProcessingState("End")
ImageProcessingState.Error = ImageProcessingState("Error")

# itk pixel type, it is depend on your itk-python supporting pixeltypes
#itkpixeltype = {"unsigned_char":itk.UC, "char":itk.SC, "unsigned_short":itk.US, 
#                "short":itk.SS, "unsigned_int":itk.UI, "int":itk.SI, 
#                "unsigned_long":itk.UL, "long":itk.SI, "float":itk.F, "double":itk.D }
itkpixeltype = {"unsigned_char":itk.UC, "char":itk.SC, "unsigned_short":itk.F, 
                "short":itk.F, "unsigned_int":itk.UI, "int":itk.F, 
                "unsigned_long":itk.UL, "long":itk.F, "float":itk.F, "double":itk.D }