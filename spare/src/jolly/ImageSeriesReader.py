# -*- coding:utf-8 -*-
"""
Created on 2009-9-16

@author: summit
"""
from Utility import *
import os

class ImageSeriesReader:
    def __init__(self, dir):
        self.dir = dir
    
    def GetImageProperties(self):
        
        thefiles = [os.path.join(self.dir,f) for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir,f)) and (os.path.splitext(f)[1]==".dcm" or os.path.splitext(f)[1]=="")]
        
        testReader = itk.ImageFileReader.IUS3.New()
        testReader.SetFileName(thefiles[0])
        
        try:
            testReader.GenerateOutputInformation()
        except RuntimeError, e:
            print e
            return False
        
        testImageIOBase = testReader.GetImageIO()
        
        dimension = testImageIOBase.GetNumberOfDimensions()
        numberofcomponents = testImageIOBase.GetNumberOfComponents()
        componenttype = testImageIOBase.GetComponentTypeAsString(
                        testImageIOBase.GetComponentType())
        pixeltype = testImageIOBase.GetPixelTypeAsString(
                        testImageIOBase.GetPixelType())
        imagesize = []
        imagespacing = []
        imageoffset = []
        for dim in range(0, dimension):
            imagesize.append(testImageIOBase.GetDimensions(dim))
            imagespacing.append(testImageIOBase.GetSpacing(dim))
            imageoffset.append(testImageIOBase.GetOrigin(dim))
            
        if not itkpixeltype.has_key(componenttype):
            raise ValueError, "Error while determining image properties!The found \
                    The found componenttype is %s ,which is not supported." % componenttype
            
        return  dimension, componenttype, dimension, numberofcomponents, \
                imagesize, imagespacing, imageoffset
    
    def Read(self, ext):
        imageinfo = self.GetImageProperties()
        #thefiles = [os.path.join(self.dir,f) for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir,f)) and os.path.splitext(f)[1]==ext ]
        reader = itk.ImageSeriesReader[itk.Image[itkpixeltype[imageinfo[1]], 3]].\
                New()
        
        nameGenerator = itk.GDCMSeriesFileNames.New()
        nameGenerator.SetDirectory(self.dir)
        filenames  = nameGenerator.GetInputFileNames()
        print filenames
        reader.SetFileNames(filenames)
     
        try:
            reader.Update()
        except RuntimeError, e:
            print e
            return False
        self.Image = reader.GetOutput()
        return True
    
    def ExportVTKImage(self):
        converter = itk.ImageToVTKImageFilter[self.Image].New(self.Image)
        converter.Update()
        return converter.GetOutput()
    
    def ReadToVTK(self, ext):
        imageinfo = self.GetImageProperties()
        reader = itk.ImageSeriesReader[itk.Image[itkpixeltype[imageinfo[1]], 3]].\
                New()
        
        nameGenerator = itk.GDCMSeriesFileNames.New()
        nameGenerator.SetDirectory(self.dir)
        filenames  = nameGenerator.GetInputFileNames()
        print filenames
        reader.SetFileNames(filenames)
     
        try:
            reader.Update()
        except RuntimeError, e:
            print e
            return False
        self.Image = reader.GetOutput()
        converter = itk.ImageToVTKImageFilter[self.Image].New(reader)
        converter.Update()
        return converter.GetOutput()
    
if __name__ == "__main__":
    print ImageSeriesReader("../data/head").Read('.dcm')