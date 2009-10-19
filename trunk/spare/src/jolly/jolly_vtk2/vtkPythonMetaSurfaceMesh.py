'''
Created on 2009-10-18

@author: Qiu wenfeng
'''
import vtk
import os
from jolly.jolly_vtk2.vtkPythonMetaDataSet import *

class vtkPythonMetaSurfaceMesh(vtkPythonMetaDataSet):
    '''
    vtkMetaSurfaceMesh
    @summary: Concrete implementation of vtkMetaDataSet for surface mesh handling
       This class is a powerfull vtk Addon class that helps handling a vtkDataSet.
       You can use it as a tool for handling surface mesh, modify it, Add some scalars to it, etc.
       Use the Read function to read vtkPolyData format files, as well as .mesh files.
       Use the Write function to write it into a vtkPolyData format files.
       And you can associate to the metamesh a specific vtkProperty
    @see: vtkPythonMetaImageData vtkPythonMetaDataSet vtkPythonMetaVolumeMesh
    @license: Nicolas Toussaint, Qiu wenfeng
    @since: 2009-10-18
     
    @cvar FILE_IS_VTK: PolyData read from vtk format
    @cvar FILE_IS_MESH: PolyData read from mesh format
    @cvar FILE_IS_OBJ: PolyData read from obj format
    '''
    
    FILE_IS_VTK=1
    FILE_IS_MESH=2
    FILE_IS_OBJ=3
    LAST_FILE_ID=4
  
    def __init__(self):
        '''
        Constructor
        '''
        vtkPythonMetaDataSet.__init__(self)
        self.__Type = self.VTK_META_SURFACE_MESH
#        self.__Dictionary = {}
    
    def Read(self, filename):
        '''
        Overwridden methods for read and write surface meshes
        can only read and write vtkPolyData format files
        @param filename: str
        @rtype: None
        '''
        try:
            print "Reading : %s... "%(filename)
            filetype=self.CanReadFile(filename)
            if filetype==self.FILE_IS_VTK:
                self.ReadVtkFile(filename)
            elif filetype==self.FILE_IS_MESH:
                self.ReadMeshFile(filename)
            elif filetype==self.FILE_IS_OBJ:
                self.ReadOBJFile(filename)
            else:
                print "unknown dataset type : %s"%(filename)
                raise IOError, "Unrecognized file type!"
            print "done."
        except Exception, e:
            print e
            raise IOError
        
        self.setFilePath(filename)
                
    
    def Write(self, filename):
        '''
        Overwridden methods for read and write surface meshes
        can only read and write vtkPolyData format files
        @param filename: str
        @rtype: None
        '''
        try:
            print "Writing : %s... "%(filename)
            print self.getFilePath()
            format=self.CanReadFile(self.getFilePath())
            if format==self.FILE_IS_VTK:
                self.WriteVtkFile(filename)
                print "done."
            else:
                print "unknown dataset type : %s"%(filename)
                raise IOError, "Unrecognized file type!"
        except Exception, e:
            print e
            raise IOError
       
    
    def GetPolyData(self):
        '''
        Get method to get the vtkDataSet as a vtkPolyData
        @rtype: vtkPolyData
        '''
        if not self.__DataSet:
            return None
        return vtk.vtkPolyData.SafeDownCast(self.__DataSet)
    
    def IsVtkExtension(self, ext):
        '''
        Static methods for I/O
        @param ext: str 
        @rtype: bool
        '''
        if ext in [".fib", ".vtk", ".vtp"]:
            return True
        return False
    
    def IsMeshExtension(self, ext):
        '''
        Static methods for I/O
        @param ext: str 
        @rtype: bool
        '''
        if ext in [".mesh"]:
            return True
        return False
    
    def IsOBJExtension(self, ext):
        '''
        Static methods for I/O
        @param ext: str 
        @rtype: bool
        '''
        if ext in [".obj"]:
            return True
        return False
    
    def CanReadFile(self, filename):
        '''
        Static methods for I/O
        @param filename: str 
        @rtype: unsigned int
        '''
        if self.IsMeshExtension(os.path.splitext(filename)[1]):
            return self.FILE_IS_VTK
        if self.IsOBJExtension(os.path.splitext(filename)[1]):
            reader = vtk.vtkOBJReader()
            reader.SetFileName(filename)
            try:
                reader.Update()
            except:
#                del reader
                return 0
#            del reader
            return self.FILE_IS_OBJ
        if not self.IsVtkExtension(os.path.splitext(filename)[1]):
            return 0
        try:
            reader = vtk.vtkPolyDataReader()
            reader.SetFileName(filename)
            if reader.IsFilePolyData():
#                del reader
                return self.FILE_IS_VTK
#            del reader
        except:
            pass
        return 0
    
    def GetDataSetType(self):
        '''
        Get the type of the metadataset as string
        @rtype: str
        '''
        return "SurfaceMesh"
    
    def CreateWirePolyData(self):
        '''
        @rtype: None
        '''
        if self.getWirePolyData():
            return
        if not self.GetPolyData():
            return
        
        extractor = vtk.vtkExtractEdges()
        extractor.SetInput(self.GetPolyData())
        extractor.Update()
        self.setWirePolyData(extractor.GetOutput())
        
#        del extractor
        self.Modified()
    
    def ReadVtkFile(self, filename):
        '''
        @param filename: str 
        @rtype: None
        '''
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(filename)
        try:
            reader.Update()
            self.setDataSet(reader.GetOutput())
        except Exception, e:
#            del reader
            print e
            raise IOError, "Could not read the vtk file !"
#        del reader
    
    def ReadMeshFile(self, filename):
        '''
        @param filename: str 
        @rtype: None
        '''
        print "Not implemented."
        
    
    def ReadOBJFile(self, filename):
        '''
        @param filename: str 
        @rtype: None
        '''
        reader = vtk.vtkOBJReader()
        reader.SetFileName(filename)
        
        try:
            reader.Update()
            cleanFilter = vtk.vtkCleanPolyData()
            cleanFilter.SetInput(reader.GetOutput())
            cleanFilter.ConvertLinesToPointsOn()
            cleanFilter.ConvertPolysToLinesOn()
            cleanFilter.ConvertStripsToPolysOn()
            cleanFilter.PointMergingOn()
            cleanFilter.Update()
            surfaceFilter = vtk.vtkDataSetSurfaceFilter()
            surfaceFilter.SetInput(cleanFilter.GetOutput())
            surfaceFilter.Update()
            self.setDataSet(surfaceFilter.GetOutput())
            del cleanFilter
            del surfaceFilter
        except Exception, e:
#            del reader
            print e
            raise IOError, "Could not read the OBJ file! "
#        del reader
    
    def WriteOBJFile(self, filename):
        '''
        @param filename: str 
        @rtype: None
        '''
        print "Not yet implemented"
    
    def WriteVtkFile(self, filename):
        '''
        @param filename: str 
        @rtype: None
        '''
        if not self.getDataSet():
            raise ValueError, "No DataSet to write"
        
        c_mesh = vtk.vtkPolyData.SafeDownCast(self.getDataSet())
        if not c_mesh:
            raise ValueError, "DataSet is not a polydata object"
        writer = vtk.vtkPolyDataWriter()
        writer.SetFileName(filename)
        
        try:
            writer.SetInput(c_mesh)
            writer.Write()
#            del writer
        except Exception, e:
            print e
#            del writer
            raise IOError, "Could not write to vtk file!"
#        del writer
    
    def Initialize(self):
        '''
        @rtype: None
        '''
        vtkPythonMetaDataSet.Initialize(self)
        if not self.getDataSet():
            return
        if not isinstance(self.getProperty(), vtk.vtkObject):
            return
        property = vtk.vtkProperty.SafeDownCast(self.getProperty())
        if not property:
            property = vtk.vtkProperty()
            self.setProperty(property)
#            del property
        

if __name__=="__main__":
    from vtk.util.misc import vtkGetDataRoot
    VTK_DATA_ROOT = vtkGetDataRoot()
    x = vtkPythonMetaSurfaceMesh()
    x.Read('%s/Data/bore.vtk'%(VTK_DATA_ROOT))
    x.Write('C:/bore.stl')