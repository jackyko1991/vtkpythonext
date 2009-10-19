'''
Created on 2009-10-17

@author: summit
'''
from jolly.jolly_vtk2.vtkPythonMetaDataSet import *
from jolly.Utility import *
import itk
import vtk
import os

class vtkPythonMetaImageData(vtkPythonMetaDataSet):
    '''
    vtkMetaDataSet
    @summary: This class is a powerfull vtk Addon class that helps handling a vtkDataSet.
       You can use it as a tool for handling an image, modify it, convert it into itkImage, etc
       Use the Read function to read any type of itk and vtk image file formats.
       Use the Write function to write it into a previous formats file.
       And you can associate to the metaimage a specific vtkVolumeProperty

       A DICOM dictionary is provided to carry DICOM information
   
   
       Note : This class will be able to read and write files only if ITK is used
    @see: vtkPythonMetaDataSet vtkPythonMetaDataSetSequence vtkPythonMetaSurfaceMesh vtkPythonMetaVolumeMesh vtkDataManager
    @author: Nicolas Toussaint, summit
    @copyright: summit
    '''


    def __init__(self):
        '''
        Constructor
        '''
        vtkPythonMetaDataSet.__init__(self)
        
        self.__Type = self.VTK_META_IMAGE_DATA
        self.__VolumeProperty=None
        self.__ComponentType=None
        self.__OrientationMatrix = vtk.vtkMatrix4x4()
        self.__OrientationMatrix.Identity()
        
        self.__m_ItkImage = None
        self.__m_ItkConverter = None
        self.__DicomDictionary = None
    
    def GetItkImage(self):
        '''
        Access directly to the itk image 
         For other use please refer to templated method GetItkImage()
        '''
        if not self.getDataSet():
            return None
        
        if not self.__m_ItkImage:
            caster = vtk.vtkImageCast()
            caster.SetOutputScalarTypeToFloat()
            caster.SetInput(self.GetImageData())
            caster.Update()
            self.__m_ItkConverter = itk.VTKImageToImageFilter[itk.Image[itk.F,3]].New()
            self.__m_ItkConverter.SetInput(caster.GetOutput())
            try:
                self.__m_ItkConverter.Update()
            except Exception, e:
                print e
                print "error when converting"
                return None
            
            self.__m_ItkImage = self.__m_ItkConverter.GetOutput()
        
        return self.__m_ItkImage
        
        
    
    def GetDicomDictionary(self):
        '''
        Access to the DICOM dictionary of this image
         Note that this dictionary is not filled automatically when ITK image is set.
         You have to explicitally call SetDicomDictionary() for that
        @return: itk::MetaDictionary but python itk-wrap could not support
        '''
        return self.__DicomDictionary
        
    def SetDicomDictionary(self, dictionary):
        self.__DicomDictionary=dictionary
        
    def SetItkImage(self, input):
        '''
        Sets the dataset as an ITK image.
         template type is the image scalar component type (i.e. unsigned char, float, etc)
         This method converts the itk image into a corresponding type of vtkImageData
         so that there is no unusefull memory stored.
         @param input: itk.Image 
        '''
        direction = input.GetDirection()
        origin = input.GetOrigin()
        
        matrix = vtk.vtkMatrix4x4()
        matrix.Identity()
        for x in range(3):
            for y in range(3):
                matrix.SetElement(x, y, direction[x][y])
        for x in range(3):
            matrix.SetElement(x, 3, origin[x])
        
        self.setOrientationMatrix(matrix)
        
#        del matrix
        converter = itk.ImageToVTKImageFilter[input].New()
        converter.SetInput(input)
        converter.Update()
        vtkinput = vtk.vtkImageData()
        vtkinput.DeepCopy(converter.GetOutput())
        vtkinput.SetOrigin(0, 0, 0)
        self.setDataSet(vtkinput)
#        del vtkinput
        self.LinkFilters()
    
    def ReadFile(self, filename):
        '''
        Reads a file and creates a image of a given scalar component type.
         Use with care. Please prefer using Read()
         @param filename: str 
        '''
#        ext = os.path.splitext(filename)[1]
        reader1 = vtk.vtkPNGReader()
        if reader1.CanReadFile(filename):
            reader1.SetFileName(filename)
            reader1.Update()
            self.SetDataSet(reader1.GetOutput())
            self.setFilePath(os.path.join('',filename))
            
            self.__DicomDictionary = dict()
            self.__DicomDictionary['DescriptiveName'] = reader1.GetDescriptiveName()
            self.__DicomDictionary['FileExtensions'] = reader1.GetFileExtensions()
#            del reader1
            return
#        del reader1
        
        reader2 = vtk.vtkJPEGReader()
        if reader2.CanReadFile(filename):
            reader2.SetFileName(filename)
            reader2.Update()
            self.setDataSet(reader2.GetOutput())
            self.setFilePath(os.path.join('',filename))
            
            self.__DicomDictionary = dict()
            self.__DicomDictionary['DescriptiveName'] = reader2.GetDescriptiveName()
            self.__DicomDictionary['FileExtensions'] = reader2.GetFileExtensions()
#            del reader2
            return
#        del reader2
        
        reader3 = vtk.vtkTIFFReader()
        if reader3.CanReadFile(filename):
            reader3.SetFileName(filename)
            reader3.Update()
            self.setDataSet(reader3.GetOutput())
            self.setFilePath(os.path.join('',filename))
            
            self.__DicomDictionary = dict()
            self.__DicomDictionary['DescriptiveName'] = reader3.GetDescriptiveName()
            self.__DicomDictionary['FileExtensions'] = reader3.GetFileExtensions()
#            del reader3
            return
#        del reader3
        reader4 = vtk.vtkDICOMImageReader()
        if reader4.CanReadFile(filename):
            
            reader4.SetFileName(filename)
            reader4.Update()
            self.setDataSet(reader4.GetOutput())
            
            self.setFilePath(os.path.join('',filename))
#            set the dictionary
            self.__DicomDictionary = dict()
            self.__DicomDictionary['ImageType'] = "DICOM"
            self.__DicomDictionary['PixelSpacing'] = reader4.GetPixelSpacing ()
            self.__DicomDictionary['Width'] = reader4.GetWidth()
            self.__DicomDictionary['Height'] = reader4.GetHeight()
            self.__DicomDictionary['ImagePositionPatient'] = reader4.GetImagePositionPatient()
            self.__DicomDictionary['ImageOrientationPatient'] = reader4.GetImageOrientationPatient()
            self.__DicomDictionary['BitsAllocated'] = reader4.GetBitsAllocated()
            self.__DicomDictionary['NumberOfComponents'] = reader4.GetNumberOfComponents()
            self.__DicomDictionary['TransferSyntaxUID'] = reader4.GetTransferSyntaxUID()
            self.__DicomDictionary['RescaleSlope'] = reader4.GetRescaleSlope()
            self.__DicomDictionary['RescaleOffset'] = reader4.GetRescaleOffset()
            self.__DicomDictionary['PatientName'] = reader4.GetPatientName()
            self.__DicomDictionary['StudyUID'] = reader4.GetStudyUID()
            self.__DicomDictionary['StudyID'] = reader4.GetStudyID()
            self.__DicomDictionary['GantryAngle'] = reader4.GetGantryAngle()
            self.__DicomDictionary['DescriptiveName'] = reader4.GetDescriptiveName()
            self.__DicomDictionary['FileExtensions'] = reader4.GetFileExtensions()
#            del reader4
            return
#        del reader4
        
        raise IOError, "Can not open file!"
    
    def ReadSeriesFile(self, filename):
        '''
        Reads v file and creates a image of a given scalar component type.
         Use with care. Please prefer using Read()
         @param filename: str path 
        '''
        directory = vtk.vtkDirectory()
        directory.Open (filename)
        
        sortFileNames = vtk.vtkSortFileNames()
        sortFileNames.SetInputFileNames(directory.GetFiles())
        sortFileNames.NumericSortOn()
        sortFileNames.GroupingOn()
        sortFileNames.IgnoreCaseOn()
        testfile=os.path.join(filename, sortFileNames.GetNthGroup(2).GetValue(0))
    
        reader1 = vtk.vtkPNGReader()
        if reader1.CanReadFile(testfile):
            
            reader1.SetFileNames(sortFileNames.GetNthGroup(2))
            reader1.Update()
            self.SetDataSet(reader1.GetOutput())
            self.setFilePath(os.path.join('',filename))
            
            self.__DicomDictionary = dict()
            self.__DicomDictionary['DescriptiveName'] = reader1.GetDescriptiveName()
            self.__DicomDictionary['FileExtensions'] = reader1.GetFileExtensions()
#            del reader1
            return
#        del reader1
        
        reader2 = vtk.vtkJPEGReader()
        if reader2.CanReadFile(testfile):
            reader2.SetFileName(sortFileNames.GetNthGroup(2))
            reader2.Update()
            self.setDataSet(reader2.GetOutput())
            self.setFilePath(os.path.join('',filename))
            
            self.__DicomDictionary = dict()
            self.__DicomDictionary['DescriptiveName'] = reader2.GetDescriptiveName()
            self.__DicomDictionary['FileExtensions'] = reader2.GetFileExtensions()
#            del reader2
            return
#        del reader2
        
        reader3 = vtk.vtkTIFFReader()
        if reader3.CanReadFile(testfile):
            reader3.SetFileName(sortFileNames.GetNthGroup(2))
            reader3.Update()
            self.setDataSet(reader3.GetOutput())
            self.setFilePath(os.path.join('',filename))
            
            self.__DicomDictionary = dict()
            self.__DicomDictionary['DescriptiveName'] = reader3.GetDescriptiveName()
            self.__DicomDictionary['FileExtensions'] = reader3.GetFileExtensions()
#            del reader3
            return
#        del reader3
        reader4 = vtk.vtkDICOMImageReader()
        if reader4.CanReadFile(testfile):
            
            reader4.SetDirectoryName(filename)
            reader4.Update()
            self.setDataSet(reader4.GetOutput())
            
            self.setFilePath(os.path.join('',filename))
#            set the dictionary
            self.__DicomDictionary = dict()
            self.__DicomDictionary['ImageType'] = "DICOM"
            self.__DicomDictionary['PixelSpacing'] = reader4.GetPixelSpacing ()
            self.__DicomDictionary['Width'] = reader4.GetWidth()
            self.__DicomDictionary['Height'] = reader4.GetHeight()
            self.__DicomDictionary['ImagePositionPatient'] = reader4.GetImagePositionPatient()
            self.__DicomDictionary['ImageOrientationPatient'] = reader4.GetImageOrientationPatient()
            self.__DicomDictionary['BitsAllocated'] = reader4.GetBitsAllocated()
            self.__DicomDictionary['NumberOfComponents'] = reader4.GetNumberOfComponents()
            self.__DicomDictionary['TransferSyntaxUID'] = reader4.GetTransferSyntaxUID()
            self.__DicomDictionary['RescaleSlope'] = reader4.GetRescaleSlope()
            self.__DicomDictionary['RescaleOffset'] = reader4.GetRescaleOffset()
            self.__DicomDictionary['PatientName'] = reader4.GetPatientName()
            self.__DicomDictionary['StudyUID'] = reader4.GetStudyUID()
            self.__DicomDictionary['StudyID'] = reader4.GetStudyID()
            self.__DicomDictionary['GantryAngle'] = reader4.GetGantryAngle()
            self.__DicomDictionary['DescriptiveName'] = reader4.GetDescriptiveName()
            self.__DicomDictionary['FileExtensions'] = reader4.GetFileExtensions()
#            del reader4
            return
#        del reader4
        
        raise IOError, "Can not open file!"
    
    def WriteFile(self, filename):
        '''
        Writes a file of a given scalar component type.
         Use with care. Please prefer using Write()
         @param filename: str
        '''
        itkimage = self.GetItkImage()
        if not itkimage or itkimage.IsNull():
            raise ValueError, "cannot convert image !"
        
        ext = os.path.splitext(filename)[1]
        if not ext:
            ext = self.__DicomDictionary['FileExtensions']
            filename = filename+ext
        writer = itk.ImageFileWriter[itkimage].New()
        writer.SetFileName(filename)
        writer.SetInput(itkimage)
        print itkimage
        try:
            print "writing: %s..."%(filename)
            writer.Update()
            print "done."
        except Exception, e:
            print e
            raise IOError, "cannot write file : %s"%(filename)
        
    
    def CopyInformation(self, metadataset):
        '''
         Copy some informations from a given metadataset
         It corresponds basically to all metadataset characteristics unless the vtkDataSet
         name, time, metadata dictionary...
         @param metadataset: vtkMetaDataSet
        '''
        vtkPythonMetaDataSet.CopyInformation(self, metadataset)
        imagedata = vtkPythonMetaImageData.SafeDownCast(metadataset)
        
        if not imagedata:
            return
        
        self.SetDicomDictionary(imagedata.GetDicomDictionary())
        self.setOrientationMatrix(imagedata.GetOrientationMatrix())
    
    def Read(self, filename):
        '''
        Overwridden methods for read and write images
         These methods could only be used if ITK is set to ON
         Note that the read and write process are build in order
         to reduce the unusefull memory storage. A unsigned int image file will be opened
         as so, and stored in memory as so.
         @param filename: str 
        '''
        self.ReadFile(filename)
    
    def Write(self, filename):
        '''
        @param filename: str 
        '''
        self.WriteFile(filename)
    
    def ReadColorImage(self, filename):
        '''
        @param filename: str 
        '''
        ext = os.path.splitext(filename)[1]
        reader1 = vtk.vtkPNGReader()
        if reader1.CanReadFile(filename):
            reader1.SetFileName(filename)
            reader1.Update()
            self.SetDataSet(reader1.GetOutput())
#            del reader1
            return
#        del reader1
        
        reader2 = vtk.vtkJPEGReader()
        if reader2.CanReadFile(filename):
            reader2.SetFileName(filename)
            reader2.Update()
            self.setDataSet(reader2.GetOutput())
#            del reader2
            return
#        del reader2
        
        reader3 = vtk.vtkTIFFReader()
        if reader3.CanReadFile(filename):
            reader3.SetFileName(filename)
            reader3.Update()
            self.setDataSet(reader3.GetOutput())
#            del reader3
            return
#        del reader3
        raise IOError, "Can not open file!"
    
    def SetDataSet(self, dataset):
        '''
        Set the dataset associated with the metadataset
        @param dataset: vtkDataSet
        '''
#        THINK OF A GOOD STRATEGY
#        CONCERNING PIXEL-TYPE HANDLING 
        image = vtk.vtkImageData.SafeDownCast(dataset)
        if (not image or not image.GetScalarType()==vtk.VTK_FLOAT):
#            this is OK now as we can handle any type of scalar !!
#            print "this pixel type is not float, \nand might induce some errors in further process"
            pass
        vtkPythonMetaDataSet.setDataSet(self, dataset)
    
    def GetImageData(self):
        '''
        Get mehtod to get the vtkDataSet as an vtkImageData
        @return: vtkImageData 
        '''
        if not self.getDataSet():
            return None
        return vtk.vtkImageData.SafeDownCast(self.getDataSet())
    
    def GetDataSetType(self):
        '''
        Get the type of the metadataset as string
        @return: str
        '''
        return "ImageData"

    def IsColorExtension(self, ext):
        '''
        @param ext: str 
        @return: bool
        '''
        if ext in ['.png', '.jpg', '.tiff']:
            return True
        return False
    
    def IsImageExtension(self, ext):
        '''
        @param ext: str
        @return: bool
        '''
        if ext in ['.hdr', '.gipl', '.gipl.gz', '.mha', '.vtk', '.nrrd',
                   '.nil', '.nil.gz', '.png', '.jpg', '.tiff', '.inr',
                   '.inr.gz', '.dcm']:
            return True
        return False
    
    def CanReadFile(self, filename):
        '''
        @return: int
        '''
        reader1 = vtk.vtkPNGReader()
        if reader1.CanReadFile(filename):
            return True
#        del reader1
        
        reader2 = vtk.vtkJPEGReader()
        if reader2.CanReadFile(filename):
            return True
#        del reader2
        
        reader3 = vtk.vtkTIFFReader()
        if reader3.CanReadFile(filename):
            return True
#        del reader3
        try:
            reader4 = vtk.vtkDICOMImageReader()
            if reader4.CanReadFile(filename):
                return True
        except:
            print "DICOMPaser Could not read!"
            return False
#        del reader4
        
    
    def LinkFilters(self):
        '''
        Method called everytime the dataset changes for connexion updates
        '''
        vtkPythonMetaDataSet.LinkFilters(self)
        
        #=======================================================================
        # For itk
        #=======================================================================
#        c_image = self.GetImageData()
#        if c_image:
#            self.__m_ItkConverter.SetInput(c_image)

        
         
    def Initialize(self):
        '''
        Method called everytime the dataset changes for initialization
        '''
        vtkPythonMetaDataSet.LinkFilters(self)
        self.LinkFilters()
    
    def getVolumeProperty(self):
        return self.__VolumeProperty


    def getComponentType(self):
        return self.__ComponentType


    def getOrientationMatrix(self):
        return self.__OrientationMatrix


    def setVolumeProperty(self, value):
        self.__VolumeProperty = value


    def setComponentType(self, value):
        self.__ComponentType = value


    def setOrientationMatrix(self, matrix):
        if self.__OrientationMatrix == matrix:
            return
#        if self.__OrientationMatrix:
#            self.__OrientationMatrix.UnRegister(self)
        self.__OrientationMatrix = matrix
        if self.__OrientationMatrix:
            self.__OrientationMatrix.Register(self)
        self.Modified()

    def getDicomDictionary(self):
        return self.__DicomDictionary

    def setDicomDictionary(self, value):
        self.__DicomDictionary = value



if __name__ == "__main__":
    globFileNames = vtk.vtkDirectory()
    globFileNames.Open ("C:/S70/")
    
    sortFileNames = vtk.vtkSortFileNames()
    sortFileNames.SetInputFileNames(globFileNames.GetFiles())
    sortFileNames.NumericSortOn()
    sortFileNames.GroupingOn()
    sortFileNames.IgnoreCaseOn()
    
    meta = vtkPythonMetaImageData()
    meta.ReadSeriesFile("C:/S70/")
    print meta.GetDicomDictionary()
    meta.WriteFile("C:/hello.vtk")
    print sortFileNames.GetNthGroup(2)
    
    files = None
    for i in range( sortFileNames.GetNumberOfGroups()):
        files = sortFileNames.GetNthGroup(i)
        print "%d:"%i
        for j in range(files.GetNumberOfValues()):
            print str(files.GetValue(j))
        
    files = sortFileNames.GetNthGroup(2)
    for j in range(files.GetNumberOfValues()):
        files.SetValue(j,os.path.join("C:/S70/", files.GetValue(j)))
        
    reader2 = vtk.vtkImageReader2 ()
    reader2.SetFileNames(files)
    reader2.Update()
    print reader2.GetOutput().GetScalarTypeAsString  ()
   
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName("C:/S70")
    reader.SetFileNames(files)
    
    reader.Update()
    
    print reader.GetPatientName()
    print reader.GetImagePositionPatient ()
    print reader.GetDescriptiveName ()
    print reader.GetTransferSyntaxUID ()
    print reader.GetRescaleSlope ()
    print reader.GetRescaleOffset()