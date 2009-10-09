# -*- coding:utf-8 -*-
"""
Created on 2009-10-5

@author: summit
"""
from Utility import *


class ImageReader:
    
    def __init__(self, filename):
        self.filename = filename
    
    def GetImageProperties(self):
        testReader = itk.ImageFileReader.IUS3.New()
        testReader.SetFileName(self.filename)
        
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
                
    def Read(self):
        imageinfo = self.GetImageProperties()
        reader = itk.ImageFileReader[itk.Image[itkpixeltype[imageinfo[1]], 2]].\
                New(FileName=self.filename)
     
        try:
            reader.Update()
        except RuntimeError, e:
            print e
            return False
        self.Image = reader.GetOutput()
        return True
    
    def ExportVTKImage(self):
        converter = itk.ImageToVTKImageFilter[self.Image].New(self.Image)
        return converter.GetOutput()
    
    def ReadToVTK(self):
        imageinfo = self.GetImageProperties()
        reader = itk.ImageFileReader[itk.Image[itkpixeltype[imageinfo[1]], 2]].\
                New(FileName=self.filename)
        converter = itk.ImageToVTKImageFilter[self.Image].New(reader)
        return converter.GetOutput()


if __name__ == "__main__":
        reader = ImageReader("../data/open.jpg")
        if reader.Read():
            print reader.Image
        reader = ImageReader("../data/MR")
        if reader.Read():
            print reader.Image
        reader = ImageReader("../data/CT")
        if reader.Read():
            print reader.Image
        print reader.ReadToVTK()
        
    
    