'''
Created on 2009-10-18

@author: Qiu wenfeng
'''
import vtk
import random
from jolly.jolly_vtk2.vtkPythonMetaDataSetSequence import *
import os
from jolly.jolly_vtk2.vtkPythonMetaDataSet import *
from jolly.jolly_vtk2.vtkPythonMetaVolumeMesh import *
from jolly.jolly_vtk2.vtkPythonMetaSurfaceMesh import *
from jolly.jolly_vtk2.vtkPythonMetaImageData import *

class vtkPythonDataManager(vtk.vtkObject):
    '''
    vtkDataManager
    @summary: usefull class to handle several datasets, and dataset sequences
    This class is a powerfull vtk tool to manage datasets.
    @license: Nicolas Toussaint, Qiu wenfeng
    @since: 2009-10-18
    @see: vtkPythonMetaImageData vtkPythonMetaSurfaceMesh vtkPythonMetaVolumeMesh vtkPythonMetaDataset
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__MetaDataSetList = []

    def __str__(self):
        '''
        '''
        msg = "has %d MetaDataSets... "%(len(self.__MetaDataSetList))
        for metadataset in self.__MetaDataSetList:
            msg+=str(metadataset)
        return msg
    
    def GetMetaDataSet(self, id):
        '''
         Primary method to get a metadataset of the manager from its index.
         returns NULL object if out of range.
         @param id: unsigned int
         @rtype: vtkMetaDataSet 
        '''
        try:
            return self.__MetaDataSetList[id]
        except IndexError:
            return None
    
    def GetMetaDataSetFromName(self, name):
        '''
        Secondary method to get a metadataset of the manager
         from the metadataset's name.
         returns NULL object if the name is not referenced in datamanager.
         @param name: str 
         @rtype: vtkMetaDataSet
        '''
        id=self.IsNameInManager(name)
        try:
            self.__MetaDataSetList[id]
        except IndexError:
            return None
    
    def GetMetaDataSetFromTag(self, tag):
        '''
        Secondary method to get a metadataset of the manager
         from the metadataset's tag.
         returns NULL object if the name is not referenced in datamanager.
         @param tag: str
         @rtype: vtkMetaDataSet 
        '''
        id = self.IsTagInManager(tag)
        try:
            self.__MetaDataSetList[id]
        except IndexError:
            return None
    
    def AddMetaDataSet(self, metadataset):
        '''
        Primary method to add a metadataset to the manager.
         The metadataset is added at the end of the list.
         @param metadataset: vtkMetaDataSet
         @rtype: None
        '''
        if not metadataset:
            return
        
        random.seed()
        
#       put a random color
        i1 = random.randint(0,100)
        i2 = random.randint(0,100)
        i3 = random.randint(0,100)
        
        r = float(i1)/100.0
        g = float(i2)/100.0
        b = float(i3)/100.0
        
        if i1<33:
            r=1
        elif i1<66:
            g=1
        elif i1<100:
            b=1
        
        prop=None
        if metadataset.getProperty():
            prop = vtk.vtkProperty.SafeDownCast(metadataset.getProperty())
        if prop:
            prop.SetColor(r,g,b)
        
        nameisok = False
        adding=1
        
        if not self.GetMetaDataSetFromName(metadataset.getName()):
            nameisok=True
        
        while not nameisok:
            name="%s(%d)"%(metadataset.getName(), adding)
            metadataset.setName(name)
            metadataset.setTag(name)
            if not self.GetMetaDataSet(metadataset.getName()):
                nameisok=True
        
        self.__MetaDataSetList.append(metadataset)
        metadataset.Register(self)
        
    
    def RemoveMetaDataSet(self, metadataset):
        '''
         Only method to remove a metadataset from the datamanager.
         This method simply unreferences the object by calling a delete.
         @param metadataset: vtkMetaDataSet
         @rtype: None
        '''
        if not metadataset:
            return
        try:
            self.__MetaDataSetList.remove(metadataset)
        except:
            return
    
    def ReadFile(self, filename, name=None, forsequence=False):
        '''
        Only method to get a sequence of the manager from its index.
         returns NULL pointer if out of range.
         @param filename: str
         @param name: str
         @param forsequence: bool
         @rtype: vtkMetaDataSet
        '''
        if os.path.isdir(filename):
            return self.ScanDirectoryForSequence(filename)
        type=vtkPythonMetaDataSet.VTK_META_UNKNOWN
        
        if type==vtkPythonMetaDataSet.VTK_META_UNKNOWN:
            metadataset=vtkPythonMetaVolumeMesh()
            if metadataset.CanReadFile(filename):
                type=vtkPythonMetaDataSet.VTK_META_VOLUME_MESH
        if type==vtkPythonMetaDataSet.VTK_META_UNKNOWN:
            metadataset=vtkPythonMetaSurfaceMesh()
            if metadataset.CanReadFile(filename):
                type=vtkPythonMetaDataSet.VTK_META_SURFACE_MESH
        if type==vtkPythonMetaDataSet.VTK_META_UNKNOWN:
            metadataset=vtkPythonMetaImageData()
            if metadataset.CanReadFile(filename):
                type=vtkPythonMetaDataSet.VTK_META_IMAGE_DATA
        if type==vtkPythonMetaDataSet.VTK_META_UNKNOWN:
            metadataset=vtkPythonMetaDataSetSequence()
            if metadataset.CanReadFile(filename):
                type=vtkPythonMetaDataSet.VTK_META_IMAGE_DATA
        if type==vtkPythonMetaDataSet.VTK_META_UNKNOWN:
            print "unknown file format : %s"%(filename)
            raise IOError, "Unrecognized File Type!"
        
        try:
            metadataset.Read(filename)
            if name==None:
                metadataset.setName(os.path.splitext(os.path.split(filename)[1])[0])
            else:
                metadataset.setName(name)
            self.AddMetaDataSet(metadataset)
#            del metadataset
            
            return metadataset
        except:
#            del metadataset
            raise IOError
        return None
        
    
    def ScanDirectory(self, dirname):
        '''
        Call this method to scan an entire directory.
         This will add every dataset that is readable in the manager.
         @param dirname: str
         @rtype: None
        '''
        directory=vtk.vtkDirectory()
        ret=directory.Open(dirname)
        if not ret:
            raise IOError, "Cannot open directory %s"%(dirname)
        list = []
        for i in range(directory.GetNumberOfFiles()):
            if directory.GetFile(i) in [".", ".."]:
                continue
            list.append(os.path.join(dirname, directory.GetFile(i)))
        
        list.sort()
        for filepath in list:
            try:
                self.ReadFile(filepath)
            except:
#                we don't throw exception as we want to continue scanning the directory
                print "skipping file %s"%(filepath)
#        del directory
        
    def ScanDirectoryForSequence(self, dirname, duration):
        '''
        Call this method to scan an entire directory where files belong to a sequence.
         This will add every dataset that is readable in a sequence, set it to the given duration
         and add the sequence to the manager.
         @param dirname: str
         @param duration: double
         @rtype: vtkMetaDataSetSequence
        '''
        Sequence = vtkPythonMetaDataSetSequence()
        try:
            Sequence.SetSequenceDuration(duration)
            Sequence.Read(dirname)
            Sequence.setName(os.path.split(dirname)[1])
            self.AddMetaDataSet(Sequence)
#            del Sequence
        except:
#            del Sequence
            raise IOError
        
        return Sequence
    
    def IsInManager(self, metadataset):
        '''
         returns true if the given metadataset is referenced in the manager.
         if yes, returns the its index in the list.
         @param metadataset: vtkMetaDataSet
         @rtype: int
        '''
        return self.__MetaDataSetList.index(metadataset)
    
    def IsNameInManager(self, name):
        '''
        returns true if the given name is used in the manager.
         if yes, returns the its index in the list.
         @param name: str
         @rtype: in
        '''
        for i in range(len(self.__MetaDataSetList)):
            if name==self.__MetaDataSetList[i].getName():
                return i
        return -1
    
    def IsTagInManager(self, tag):
        '''
        returns true if the given tag is used in the manager.
         if yes, returns the its index in the list.
         @param tag: str
         @rtype: int
        '''
        for i in range(len(self.__MetaDataSetList)):
            if tag==self.__MetaDataSetList[i].getTag:
                return i
        return -1
    
    def GetNumberOfMetaDataSet(self):
        '''
        returns the number of metadatasets referenced in the manager
        @rtype: unsigned int
        '''
        return len(self.__MetaDataSetList)
    
    def GetNumberOfTypedMetaDataSet(self, type):
        '''
        returns the number of metadatasets referenced in the manager for a specific type.
         This type can be : VTK_META_IMAGE_DATA, VTK_META_SURFACE_MESH or VTK_META_VOLUME_MESH.  
         @param type: unsigned int
         @rtype: unsigned int
        '''
        ret=0
        for metadataset in self.__MetaDataSetList:
            if metadataset.getType()==type:
                ret = ret+1
        return ret
    
    def UpdateSequencesToTime(self, time):
        '''
        Method to update the current time of all sequences referenced in the manager.
         NB : can be accessed directly from the vtkMetaDataSetSequence.
         @param time: double
         @rtype: None
        '''
        for metadataset in self.__MetaDataSetList:
            if isinstance(metadataset,vtkPythonMetaDataSetSequence):
                metadataset.UpdateToTime(time)
            
    def UpdateSequencesMatchingTagToTime(self, tag, time):
        '''
         Method to update the current time of all sequences referenced in the manager.
         NB : can be accessed directly from the vtkMetaDataSetSequence.
         @param tag: str
         @param time: time
         @rtype: None 
        '''
        for metadataset in self.__MetaDataSetList:
            if (isinstance(metadataset,vtkPythonMetaDataSetSequence) and 
                metadataset.getTag()==tag):
                metadataset.UpdateToTime(time)
    
    def GetSequencesRangeMin(self):
        '''
        Get the maximum time flag from all sequences referenced in the manager.
        @rtype: double
        '''
        min=9999999
        for metadataset in self.__MetaDataSetList:
            if (isinstance(metadataset,vtkPythonMetaDataSetSequence)):
                temp = metadataset.getMinTime()
                if temp<min:
                    min=temp
        return min
    
    def GetSequencesRangeMax(self):
        '''
        Get the maximum time flag from all sequences referenced in the manager.
        @rtype: double
        '''
        max=-9999999
        for metadataset in self.__MetaDataSetList:
            if (isinstance(metadataset,vtkPythonMetaDataSetSequence)):
                temp = metadataset.getMaxTime()
                if temp>max:
                    max=temp
        return max
    
    def GetSequencesMaxNumber(self):
        '''
        Get the maximum number of metadatasets from all sequences referenced in the manager.
        @rtype: unsigned int
        '''
        max=0
        for metadataset in self.__MetaDataSetList:
            if (isinstance(metadataset,vtkPythonMetaDataSetSequence)):
                temp=metadataset.getNumberOfMetaDataSets()
                if temp>max:
                    max=temp
        return max
        
    
    def GetTypedMetaDataSetList(self, type):
        '''
        access to the list of metadatasets of a specific type referenced in the manager.
         Use this method carefully.
         The type can be : VTK_META_IMAGE_DATA, VTK_META_SURFACE_MESH or VTK_META_VOLUME_MESH.
         @param type: unsigned int
         @rtype: vtkMetaDataSet list []
        '''
        list=[]
        for metadataset in self.__MetaDataSetList:
            if metadataset.getType()==type:
                list.append(metadataset)
        return list
        
    
    def GetMetaDataSetListFromTag(self, tag):
        '''
         access to the list of metadatasets of a specific tag referenced in the manager.
         Use this method carefully.
         Tag argument can be set to each metadataset by SetTag().
         @param tag: str
         @rtype: vtkMetaDataSet list []
        '''
        list = []
        for metadataset in self.__MetaDataSetList:
            if metadataset.getTag()==tag:
                list.append(metadataset)
        return list
    
    def GetSequenceListFromTag(self, tag):
        '''
        access to the list of sequences of a specific tag referenced in the manager.
         Use this method carefully.
         Tag argument can be set to each metadataset by SetTag().
         @param tag: str
         @rtype: vtkMetaDataSet list []
        '''
        list = []
        for metadataset in self.__MetaDataSetList:
            if (isinstance(metadataset,vtkPythonMetaDataSetSequence) 
                and metadataset.getTag()==tag):
                list.append(metadataset)
        return list
            
    
    def CreateDefaultName(self, type, filename=None):
        '''
        returns a string of characters corresponding to the default name
         to be used when adding a metadataset. Use this method to avoid two
         metadatasets with the same name.
         @param type: unsigned int
         @rtype: filename
        '''
        isused=True
        id=0
        ret=""
        
        if filename:
            filename_str = os.path.split(filename)[1]
            if self.IsNameInManager(filename_str):
                return self.filename_str
        
        while isused:
            if type==vtkPythonMetaDataSet.VTK_META_IMAGE_DATA:
                ret="image_%i"%(id)
            elif type==vtkPythonMetaDataSet.VTK_META_SURFACE_MESH:
                ret="mesh_%i"%(id)
            elif type==vtkPythonMetaDataSet.VTK_META_VOLUME_MESH:
                ret="tetra_%i"%(id)
            else:
                ret="unknown_%i"%(id)
                dummy=self.IsNameInManager(ret)
            if dummy>=0:
                isused=True
        return ret
        
            
    
    def DuplicateMetaDataSet(self, input):
        '''
         Duplicate a metadataset from a metadataset,
         this is a static method returning a new object, to be deleted outside the method
         @param input: vtkMetaDataSet
         @rtype: vtkMetaDataSet
        '''
        metadataset=None
        dataset=None
        type=0
        
        if input.getType()==vtkPythonMetaDataSet.VTK_META_SURFACE_MESH:
            type=vtkPythonMetaDataSet.VTK_META_SURFACE_MESH
            metadataset=vtkPythonMetaSurfaceMesh()
            dataset=vtk.vtkPolyData()
        elif input.getType()==vtkPythonMetaDataSet.VTK_META_VOLUME_MESH:
            type=vtkPythonMetaDataSet.VTK_META_VOLUME_MESH
            metadataset=vtkPythonMetaVolumeMesh()
            dataset=vtk.vtkUnstructuredGrid()
        elif input.getType()==vtkPythonMetaDataSet.VTK_META_IMAGE_DATA:
            type=vtkPythonMetaDataSet.VTK_META_IMAGE_DATA
            metadataset=vtkPythonMetaImageData()
            dataset=vtk.vtkImageData()
        else:
            return None
        if input.getDataSet():
            dataset.DeepCopy(input.getDataSet())
        metadataset.CopyInformation(input)
        metadataset.setDataSet(dataset)
        metadataset.setProperty(input.getProperty())
        
        del dataset
        
        return metadataset
    
    def getMetaDataSetList(self):
        return self.__MetaDataSetList


    def setMetaDataSetList(self, value):
        self.__MetaDataSetList = value

if __name__=="__main__":
    from vtk.util.misc import vtkGetDataRoot
    VTK_DATA_ROOT = vtkGetDataRoot()
    x = vtkPythonDataManager()
    x.ScanDirectory('%s/Data'%(VTK_DATA_ROOT))
    print x
#    x.Write('C:/blow.vtk')

    