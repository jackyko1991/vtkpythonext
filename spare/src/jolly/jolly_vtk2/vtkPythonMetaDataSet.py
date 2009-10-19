'''
Created on 2009-10-17

@author: Qiu wenfeng
'''
import vtk 
#import itk

class vtkPythonMetaDataSet(vtk.vtkDataObject):
    '''
    Abstract class for vtkDataset handling
    This class is a powerfull vtk Addon class that helps handling a vtkDataSet.
    see the lower level classes for details
    '''

#    DataSetTypeId
    VTK_META_IMAGE_DATA = 0
    VTK_META_SURFACE_MESH = 0
    VTK_META_VOLUME_MESH = 0
    VTK_META_DATATYPE_NUMBER = 3
    VTK_META_UNKNOWN = 1000
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__Type = self.VTK_META_UNKNOWN
        self.__pickedPointId = -1                       #int
        self.__PickedCellId = -1                        #int
        self.__DataSet  = 0                             #vtkDataSet
        self.__ActorList = vtk.vtkActorCollection()     #vtkDataArrayCollection
        self.__Time = -1                                #double
        self.__Property = 0                             #vtkObject
        self.__ArrayCollection = vtk.vtkDataArrayCollection() #vtkDataArrayCollection
        
        self.__CurrentScalarArray = 0                   #vtkDataArray
        self.__Name = ""                                #string
        self.__FilePath = ""                            #string
        self.__Tag = ""                                 #string
        self.__Lock = 0                                 #int
        
        self.__MetaDataDictionary = None                #itk.MetaDataDictionary
        
        self.__WirePolyData = None                      #vtkPolyData
        
        self.Initialize()

    def SetMetaData(self, key, value):
        '''
        Fill the metadataset dictionary with this method
        Example :
           mymetadataset->SetMetaData< std::vector<int> >( "idlist", myidlist );
        @param key: string
        @param value: any type  
        '''
#        if self.__MetaDataDictionary.HasKey(key):
#            itk.EncapsulateMetaData[value](self.__MetaDataDictionary, key , value)
#        else:
#            itk.EncapsulateMetaData[value](self.__MetaDataDictionary, key , value)
#    
    def GetMetaData(self, key):
        pass
    
    def GetMetaDataKeyList(self):
        pass
    
    
    def AddActor(self, actor):
        '''
        Add an actor to the metadataset. Use this method
         to be able to handle several actors of the same metadataset at the same time :
         mymetadataset->SetVisibility(true);
         @param actor: vtkActor 
         @return: None
        '''
        if actor and not self.HasActor(actor):
            self.__ActorList.AddItem(actor)
    
    def RemoveActor(self, actor):
        '''
        Removes an actor from the list
        @param actor: vtkActor 
        @return: None
        '''
        self.__ActorList.RemoveItem(actor)
        
    def RemoveAllActors(self):
        '''
        Clear actor list
        @return: None
        '''
        for i in range(self.__ActorList.GetNumberOfItems()):
            self.__ActorList.RemoveItem(i)
     
    def GetActor(self, i):
        '''
        Access to an actor of list
        @param i: unsigned int
        @return: vtkActor 
        '''
        return vtk.vtkActor.SafeDownCast(self.__ActorList.GetItemAsObject(i))
    
    def GetNumberOfActors(self): 
        '''
        returns the amount of actors handled by this metadataset
        @return int: 
        '''
        return self.__ActorList.GetNumberOfItems()
    
    def HasActor(self, actor):
        '''
        returns true if the actor is handled by this metadataset
        @param actor: vtkActor
        @return: bool 
        '''
        for i in range(self.__ActorList.GetNumberOfItems()):
            if self.GetActor(i)==actor:
                return True
        
        return False
        
    def SetVisibility(self, visible):
        '''
        Get/Set the visibility of the metadataset : to be used with AddActor()
        @param visible: bool
        @return: None 
        '''
        for i in range(self.__ActorList.GetNumberOfItems()):
            self.SetActorVisibility(i, visible)
    
    def GetVisibility(self):
        '''
        Get/Set the visibility of the metadataset : to be used with AddActor()
        @return: int
        '''
        ret = False
        for i in range(self.__ActorList.GetNumberOfItems()):
            if self.GetActorVisibility(i):
                ret=True
                break
        return ret
    
    def SetActorVisibility(self, it, visible):
        '''
        Get/Set the visibility of the metadataset : to be used with AddActor()
        @param it: unsigned int
        @param visible: bool 
        @return: void
        '''
        actor = self.GetActor(it)
        if actor:
            actor.SetVisibility (visible)
    
    def GetActorVisibility(self, it):
        '''
        Get/Set the visibility of the metadataset : to be used with AddActor()
        @param it: unsigned it
        @return: int
        '''
        actor = self.GetActor(it)
        if actor:
            return actor.GetVisibility()
        return False
    
    def Read(self, filename):
        '''
        Overridden methods for read and write the dataset
        @param filename: str 
        @return: None
        '''
        print "not implemented here"
        
    
    def Write(self, filename):
        '''
        Overridden methods for read and write the dataset
        @param filename: str 
        @return: None
        '''
        print "not implemented here"
    
    def ReadData(self, filename):
        '''
        read and assign some scalars to the dataset (should be point set). 
         Either vtkMetaSurfaceMesh or vtkMetaVolumeMesh. The scalars are casted in float type
         for memory purpose. the scalars are added to the PointData or CellData of the dataset
         according to a flag written in the file.
         head of the file should be : \n\n
         keyword (string that be the name of the scalar field)\n
         type (flag that says where the scalars should be assigned : 1 for vertices, 2 for cells) \n
         nb dim (integers. nb is the number of Tuples of the field; dim is the Tuple size)\n\n
         @param filename: str 
         @return: None
        '''
        if not self.__DataSet:
            return
        
        keyword = open(filename).readline()
        print keyword
        if keyword=="position":
            self.ReadPosition(filename)
        else:
            self.ReadDataInternal(filename)
    
    def WriteData(self, filename, dataname):
        '''
        read and assign some scalars to the dataset (should be point set). 
         Either vtkMetaSurfaceMesh or vtkMetaVolumeMesh. The scalars are casted in float type
         for memory purpose. the scalars are added to the PointData or CellData of the dataset
         according to a flag written in the file.
         head of the file should be : \n\n
         keyword (string that be the name of the scalar field)\n
         type (flag that says where the scalars should be assigned : 1 for vertices, 2 for cells) \n
         nb dim (integers. nb is the number of Tuples of the field; dim is the Tuple size)\n\n
         @param filename: str 
         @param dataname: str 
         @return: None
        '''
        if not self.getDataSet():
            return
        
        pass
        
    
    def GetDataSetType(self):
        '''
        Get the type of the metadataset as string
        @return: str
        '''
        return "MetaDataSet"
    
    def CopyInformation(self, metadataset):
        '''
        Copy some informations from a given metadataset
         It corresponds basically to all metadataset characteristics unless the vtkDataSet
         name, time, metadata dictionary...
         @param metadataset: vtkMetaDataSet
         @return: None 
        '''
        if not metadataset:
            return
        
        self.setName(metadataset.getName())
        self.setTime(metadataset.getTime())
        self.setFilePath(metadataset.getFilePath())
    
#        self.setProperty(metadataset.getProperty())
#        add actors?
        self.setTag(metadataset.getTag())
        
        for i in range(metadataset.getArrayCollection().GetNumberOfItems()):
            self.__ArrayCollection.AddItem(vtk.vtkDataArray.SafeDownCast(metadataset.GetArrayCollection().GetItemAsObject (i)))
     
    def GetColorArrayCollection(self, collection):
        '''
        Access to the collection of vtkDataArray contained by the member vtkDataSet
         in points or cells for colorization mapping purpose
         @param collection: vtkDataArrayCollection 
         @return: None
        '''
        if not self.getDataSet():
            return
        
        for i in self.getDataSet().GetPointData().GetNumbeofArrays():
            collection.AddItem(self.getDataSet().GetPointData().GetArray(i)) 
        for i in self.getDataSet().GetCellData().GetNumbeofArrays():
            collection.AddItem(self.getDataSet().GetCellData().GetArray(i)) 
        
    
    def GetArray(self, name):
        '''
        Returns the vtkDataArray contained in the DataSet or in metadataset, named name
         returns NULL if not found
         @param name: str
         @return: None 
        '''
        for i in self.__ArrayCollection.GetNumberOfItems():
            if self.__ArrayCollection.GetItem(i).GetName() and self.__ArrayCollection.GetItem(i).GetName()=="name":
                return self.__ArrayCollection.GetItem(i)
        
#        then try in the pointdata and celldata array collections
        ret=None
        
        arrays = vtk.vtkDataArrayCollection()
        self.GetColorArrayCollection(arrays)
        
        for i in range(arrays.GetNumberofItems()):
            if arrays.GetItem(i).GetName() and arrays.GetItem(i).GetName()=="name":
                ret=arrays.GetItem(i)
                break
#        del array
        return ret
        
    def AddArray(self, array):
        '''
        Add an array to the MetaDataSet,
         does not add it to the pointdata or celldata
         Access to this dataarray by its name with GetArray()
         @param array: vtkDataArray
         @return: None 
        '''
        self.__ArrayCollection.AddItem(array)
        
    def ColorByArray(self, array):
        '''
        Use this method to colorize the actors of this metadata by a given vtkDataArray
         The array must be contained by the member vtkDataSet of this metadataset.
         Use GetArray() to find a specific array
         @param array: vtkDataArray
         @return None 
        '''
        self.__CurrentScalarArray = array
        if not array:
            return 
        
        array_is_in_points = False
        
        if self.__DataSet.GetPointData().HasArray(array.GetName()):
            array_is_in_points = True
        
        min = max = 0.0
        
        # vtkDataArray
        junk = None 
        # vtkDataSetAttributes
        attributes = None
        
        if array_is_in_points:
            junk = self.getDataSet().GetPointData().GetArray(array.GetName())
            attributes = self.getDataSet().GetPointData()
        else:
            junk = self.getDataSet().GetCellData().GetArray(array.GetName())
            attributes = self.getDataSet().GetCellData()
        
        if not junk:
            return
        
        if min>junk.GetRange()[0]:
            min=junk.GetRange()[0]
        if max<junk.GetRange()[1]:
            max=junk.GetRange()[1]
        
        lut = array.GetLookupTable()
        if lut:
            junk.SetLookupTable()
        
        attributes.SetActiveScalars(array.GetName())
        for i in range(self.__ActorList.GetNumberOfItems()):
            actor = self.GetActor(i)
            if not actor:
                continue
            mapper = actor.GetMapper()
            
            if not array_is_in_points:
                mapper.SetScalarModeToUseCellFieldData()
            else:
                mapper.SetScalarModeToUsePointFieldData()
            
            lut = array.GetLookupTable()
            
            if lut:
                lut.SetRange(min, max)
#                mapper.SetLookupTable()
                mapper.UseLookupTableScalarRangeOn()
            
            mapper.SetScalarRange(min, max)
            mapper.SelectColorArray(array.GetName())
    
    def SetScalarVisibility(self, val):
        '''
        Get/Set the scalar visibility, operates on the actors
        @param val: bool
        @return: None 
        '''
        for i in self.__ActorList.GetNumberOfItems():
            actor = self.GetActor(i)
            if not actor:
                continue
            mapper = actor.GetMapper()
            mapper.SetScalarVisibility(val)
    
    def GetScalarVisibility(self):
        '''
        Get/Set the scalar visibility, operates on the actors
        @return: bool
        '''
        if self.GetNumberOfActors() and self.GetActor(0):
            return self.GetActor(0).GetMapper().GetScalarVisibility()
        return False
    
    def ScalarVisibilityOn(self):
        '''
        Get/Set the scalar visibility, operates on the actors
        '''
        self.SetScalarVisibility(True)
            
    
    def ScalarVisibilityOff(self):
        '''
        Get/Set the scalar visibility, operates on the actors
        '''
        self.SetScalarVisibility(False)
    
    def GetCurrentScalarRange(self):
        '''
        @return: double[]
        '''
        val = [vtk.VTK_DOUBLE_MAX, vtk.VTK_DOUBLE_MIN]
        
        if self.getCurrentScalarArray():
            val = self.getCurrentScalarArray().GetRange()
        elif self.getDataSet() and val[0] == vtk.VTK_DOUBLE_MAX:
            val = self.getDataSet().GetScalarRange()
        
        return val 
    
    def LockOn(self):
        '''
        Lock/Unlock flag
        '''
        self.setLock(True)
    
    def LockOff(self):
        '''
        Lock/Unlock flag
        '''
        self.setLock(False)

    def CreateWirePolyData(self):
        pass
    
    def LinkFilters(self):
        '''
        Method called everytime the dataset changes for connexion updates
        '''


    def Initialize(self):
        '''
        Method called everytime the dataset changes for initialization
        '''
        self.__ActorList.RemoveAllItems()
#        if self.__DataSet:
#            self.__DataSet.GetPointData().CopyScalarsOn()
    
    def ReadPosition(self, filename):
        '''
         Internal use : read and assign positions to the dataset (should be point set). 
         Either vtkMetaSurfaceMesh or vtkMetaVolumeMesh
         @param filename: str 
        '''
    
    def ReadDataInternal(self, filename):
        '''
         Internal use : read and assign some scalars to the dataset (should be point set). 
         Either vtkMetaSurfaceMesh or vtkMetaVolumeMesh. The scalars are casted in float type
         for memory purpose. 
         @param filename: str 
        '''
    
    def getType(self):
        '''
        Get the type of the metadataset :
          vtkMetaDataSet::VTK_META_IMAGE_DATA, vtkMetaDataSet::VTK_META_SURFACE_MESH,
          vtkMetaDataSet::VTK_META_VOLUME_MESH, or vtkMetaDataSet::VTK_META_UNKNOWN
        '''
        return self.__Type


    def getPickedPointId(self):
        '''
        Internal use only
        @return: int
        '''
        return self.__pickedPointId


    def getPickedCellId(self):
        '''
        Internal use only
        @return: int
        '''
        return self.__PickedCellId


    def getDataSet(self):
        '''
        Get the dataset associated with the metadataset
        '''
        return self.__DataSet


    def getActorList(self):
        return self.__ActorList


    def getTime(self):
        '''
        Get/Set methods for a flag of time
        @return: double
        '''
        tmp = self.__Time
        isvalid = self.GetMetaData("Time", tmp)
        if isvalid:
            self.__Time = tmp
        return self.__Time


    def getProperty(self):
        '''
        Access to the visualization property of the metadataset
         downcast the object to the write type :
         vtkProperty for vtkMetaSurfaceMesh
         vtkVolumeProperty for vtkMetaImageData
        '''
        return self.__Property


    def getArrayCollection(self):
        '''
         Access to the collection of vtkDataArray contained in this metadataset. 
         These arrays do not have any colorization purpose. They are stored for the user
         convenience. 
         @return: vtkDataArrayCollection
        '''
        return self.__ArrayCollection


    def getCurrentScalarArray(self):
        '''
        Get the currently used scalar array for visualization
        '''
        return self.__CurrentScalarArray


    def getName(self):
        '''
        Get/Set methods fot the metadataset name
        @return: str
        '''
        return self.__Name


    def getFilePath(self):
        '''
        Get/Set methods fot the metadataset current file path
        @return: str
        '''
        return self.__FilePath


    def getTag(self):
        '''
        Get/Set methods for the metadataset tag
          You can associate several metadataset to a single tag to retrieve them easily
        @return: str 
        '''
        return self.__Tag


    def getLock(self):
        '''
        Lock/Unlock flag
        @return: int
        '''
        return self.__Lock


    def getMetaDataDictionary(self):
        '''
        Access to the metadataset dictionary
        The dictionary can be used to hold some arbitrary types of flags
        '''
        return self.__MetaDataDictionary


    def getWirePolyData(self):
        return self.__WirePolyData


    def setType(self, value):
        self.__Type = value


    def setPickedPointId(self, value):
        '''
        Internal use only
        @param value: int 
        '''
        self.__pickedPointId = value


    def setPickedCellId(self, value):
        '''
        Internal use only
        @param value: int 
        '''
        self.__PickedCellId = value


    def setDataSet(self, dataset):
        '''
        Set the dataset associated with the metadataset
         @param dataset: vtkDataSet 
        '''
        if self.__DataSet == dataset:
            return
#        if self.__DataSet:
#            self.__DataSet.UnRegister(self)

        # because I don't know the dataset's really type, thanks to newInstance!
        newdataset = dataset.NewInstance()  
        newdataset.DeepCopy(dataset)
        
        self.__DataSet = dataset
        
#        if self.__DataSet:
#            self.__DataSet.Register(self)
        if self.__DataSet:
#            self.__DataSet.GetPointData().CopyAllOn()
            self.Initialize()
        
#        del newdataset
        self.Modified()


    def setActorList(self, value):
        self.__ActorList = value


    def setTime(self, time):
        '''
         Get/Set methods for a flag of time
         @param time: double 
        '''
        self.__Time = time
        self.SetMetaData("Time", time)
        


    def setProperty(self, value):
        '''
        Access to the visualization property of the metadataset
         downcast the object to the write type :
         vtkProperty for vtkMetaSurfaceMesh
         vtkVolumeProperty for vtkMetaImageData
        '''
        self.__Property = value


    def setArrayCollection(self, value):
        self.__ArrayCollection = value


    def setCurrentScalarArray(self, array):
        '''
        Get the currently used scalar array for visualization
        @param array: vtkDataArray 
        '''
        self.__CurrentScalarArray = array


    def setName(self, name):
        '''
        Get/Set methods fot the metadataset name
        @param name: str
        '''
        self.__Name = name


    def setFilePath(self, path):
        '''
        Get/Set methods fot the metadataset current file path
        @param path: str 
        '''
        self.__FilePath = path


    def setTag(self, path):
        '''
        Get/Set methods for the metadataset tag
          You can associate several metadataset to a single tag to retrieve them easily
        @param path: str 
        '''
        self.__Tag = path


    def setLock(self, value):
        '''
        Description:
         Lock/Unlock flag
        '''
        if int(value)<0 or int(value)>1:
            return
        self.__Lock = int(value)


    def setMetaDataDictionary(self, dictionary):
        '''
         Set the metadataset dictionary
         @param dictionary: itkMetaDataDictionary 
        '''
        self.__MetaDataDictionary = dictionary


    def setWirePolyData(self, dataset):
        '''
        @param dataset: vtkPolyData 
        '''
        if self.__WirePolyData == dataset:
            return
        
#        if self.__WirePolyData:
#            self.__WirePolyData.UnRegister(self)

        self.__WirePolyData = dataset
        
#        if self.__WirePolyData:
#            self.__WirePolyData.Register(self)

        self.Modified()
    
    def __str__(self):
        return "Name \t: %s\nDataSet \t: %s\n"%(self.__Name, self.__DataSet)
        
    

        