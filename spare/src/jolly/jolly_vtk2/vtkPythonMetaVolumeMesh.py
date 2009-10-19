'''
Created on 2009-10-18

@author: Qiu wenfeng
'''
from jolly.jolly_vtk2.vtkPythonMetaDataSet import *
import vtk
import os
class vtkPythonMetaVolumeMesh(vtkPythonMetaDataSet):
    '''
    vtkMetaVolumeMesh
    @summary: Concrete implementation of vtkMetaDataSet for volumic mesh handling
     This class is a powerfull vtk Addon class that helps handling a vtkDataSet.
     Specific case of a volumic mesh, hendles, read and writes vtkUntructuredGrid object
    @see: vtkMetaImageData vtkMetaSurfaceMesh vtkMetaDataSet
    @license: Nicolas Toussaint, Qiu wenfeng
    @since: 2009-10-18
    '''
    FILE_IS_VTK=1
    FILE_IS_MESH=2
    FILE_IS_OBJ=3
    FILE_IS_GMESH=4
    LAST_FILE_ID=5

    def __init__(self):
        '''
        Constructor
        '''
        vtkPythonMetaDataSet.__init__(self)
        
        self.__Type = self.VTK_META_VOLUME_MESH
    
    
    def Read(self, filename):
        '''
        @param filename: str 
        @rtype: None
        '''
        format = self.CanReadFile(filename)
        
        try:
            print "Reading: %s... "%(filename)
            if format==self.FILE_IS_VTK:
                self.ReadVtkFile(filename)
            elif format==self.FILE_IS_MESH:
                self.ReadMeshFile(filename)
            elif format==self.FILE_IS_GMESH:
                self.ReadGMeshFile(filename)
            else:
                print "unknown dataset type : "
                raise IOError, "Unrecognized File Type!"
            print "done."
        except Exception, e:
            print e
            raise IOError
        self.setFilePath(filename)
    
    def Write(self, filename):
        '''
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
    
    def GetUnstructuredGrid(self):
        '''
        @rtype: vtkUnstructuredGrid
        '''
        if not self.getDataSet():
            return None
        return vtk.vtkUnstructuredGrid.SafeDownCast(self.getDataSet())
    
    def IsVtkExtension(self, ext):
        '''
        @param ext: str
        @rtype: bool
        '''
        if ext in [".vtk", ".vtu"]:
            return True
        return False
    
    def IsMeshExtension(self, ext):
        '''
        @param ext: str
        @rtype: bool
        '''
        if ext in [".mesh"]:
            return True
        return False
    
    def IsGMeshExtension(self, ext):
        '''
        @param ext: str 
        @rtype: bool
        '''
        if ext in [".meh"]:
            return True
        return False
    
    def CanReadFile(self, filename):
        '''
        @param filename: str
        @rtype: unsigned int
        '''
        if self.IsMeshExtension(os.path.splitext(filename)[1]):
            print "Not implemented."
            return 0
        if self.IsGMeshExtension(os.path.splitext(filename)[1]):
            print "Not implemented."
            return 0
        if not self.IsVtkExtension(os.path.splitext(filename)[1]):
            return 0
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(filename)
        if reader.IsFileUnstructuredGrid():
#            del reader
            return self.FILE_IS_VTK
#        del reader
        return 0
    
    def GetDataSetType(self):
        '''
        @rtype: str
        '''
        return "VolumeMesh"
    
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
    
    def ReadVtkFile(self, filename):
        '''
        @param filename: str
        @rtype: None
        '''
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(filename)
        
        try:
            reader.Update()
            self.setDataSet(reader.GetOutput())
        except Exception, e:
            print e
#            del reader
            raise IOError, "Could not read the vtk file! "
#        del reader
    
    def ReadMeshFile(self, filename):
        '''
        @param filename: str
        @rtype: None 
        '''
        print "Not implemented."
    
    def ReadGMeshFile(self, filename):
        '''
        @param filename: str
        @rtype: None
        '''
        print "Not implemented."
    
    def WriteVtkFile(self, filename):
        '''
        @param filename: str
        @rtype: None
        '''
        if not self.getDataSet():
            raise ValueError, "No DataSet to write"
        
        c_mesh = vtk.vtkUnstructuredGrid.SafeDownCast(self.getDataSet())
        if not c_mesh:
            raise ValueError, "DataSet is not a polydata object"
        writer = vtk.vtkUnstructuredGridWriter()
        writer.SetFileName(filename)
        
        try:
            writer.SetInput(c_mesh)
            writer.Write()
#            del writer
        except Exception, e:
#            del writer
            print e
        self.setFilePath(filename)
        
if __name__ == "__main__":
    from vtk.util.misc import vtkGetDataRoot
    VTK_DATA_ROOT = vtkGetDataRoot()
    x = vtkPythonMetaVolumeMesh()
    x.Read('%s/Data/blow.vtk'%(VTK_DATA_ROOT))
    x.Write('C:/blow.vtk')
        