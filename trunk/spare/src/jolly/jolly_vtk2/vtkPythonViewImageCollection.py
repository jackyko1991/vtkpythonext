'''
Created on 2009-10-14

@author: summit
'''
import vtk

from jolly.jolly_vtk2.vtkPythonViewImage import *
from jolly.jolly_vtk2.vtkPythonViewImage2D import *

class vtkPythonViewImageCollection(vtk.vtkCollection):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__Command = vtkPythonViewImageCollectionCommand()
        self.__Command.setCollection(self)
    
    def GetNextItem(self):
        '''
        Description:
        Get the next vtkViewImage in the list. Return NULL when at the end of the
        list.
        @return: vtkViewImage
        '''
        return self.GetNextItemAsObject()
    
    def GetItem(self, i):
        '''
        Description:
        Get the next vtkViewImage in the list. Return NULL when at the end of the
        list.
        @param i: int
        @return: vtkViewImage 
        '''
        return self.GetItemAsObject(i)
    
    def AddItem(self, a):
        '''
        Description:
        Add an object to the list. Does not prevent duplicate entries.
        @param a: vtkViewImage
        @return: None
        '''
        vtk.vtkCollection.AddItem(self, a)
        if isinstance(a, vtkPythonViewImage2D) and a.getInteractorStyleSwitcher():
#            a.getInteractorStyleSwitcher().AddObserver("ResetWindowLevelEvent", None)
#            a.getInteractorStyleSwitcher().AddObserver("WindowLevelEvent", None)
#            a.getInteractorStyleSwitcher().AddObserver("UserEvent", None)
            a.getInteractorStyleSwitcher().AddObserver("ResetWindowLevelEvent", lambda obj, event: self.__Command.Execute(obj, "ResetWindowLevelEvent", None))
            a.getInteractorStyleSwitcher().AddObserver("WindowLevelEvent", lambda obj, event: self.__Command.Execute(obj, "WindowLevelEvent", None))
            # SliceMoveEvent RequestedPositionEvent ResetViewerEvent
            a.getInteractorStyleSwitcher().AddObserver("UserEvent", lambda obj, event: self.__Command.Execute(obj, "UserEvent", None)) 
            a.GetInteractor().SetInteractorStyle(None)
            a.getInteractorStyleSwitcher().SetInteractor(a.GetInteractor())
            
    def ReplaceItem(self, i, a):
        '''
        Description:
         Replace the i'th item in the collection with a
        @param i: int
        @param a: vtkViewImage
        @return: None
        '''
        vtk.vtkCollection.ReplaceItem(self, i, a)
        
    def RemoveItem(self, i):
        '''
        Description:
        Remove the i'th item in the list.
        Be careful if using this function during traversal of the list using
        GetNextItemAsObject (or GetNextItem in derived class).  The list WILL
        be shortened if a valid index is given!  If this->Current is equal to the
        element being removed, have it point to then next element in the list.
        @param i: int 
        @return: None
        '''
        vtk.vtkCollection.RemoveItem(i)
        
    def RemoveItemByObject(self, a):
        '''
        Description:
        Remove an object from the list. Removes the first object found, not
        all occurrences. If no object found, list is unaffected.  See warning
        in description of RemoveItem(int).
        @param a: vtkViewImage
        @return: None
        '''
        vtk.vtkCollection.RemoveItem(self, a)
        
    def RemoveAllItems(self):   
        '''
        Description:
        Remove all objects from the list.
        @return: None
        '''
        vtk.vtkCollection.RemoveAllItems(self)
    
    def InstallCrossAxes(self):
        '''
        Description:
        Initialize the viewers togethers.
        @return: None
        '''
        for i in range(self.GetNumberOfItems()):
            for j in range(self.GetNumberOfItems()):
                if i<>j:
                    Vi = self.GetItem(i)
                    Vj = self.GetItem(j)
                    if (isinstance(Vi, vtkPythonViewImage2D) and Vi 
                        and isinstance(Vj, vtkPythonViewImage2D) and Vj):
                        
                        Vi.AddDataSet(Vj.getSlicePlane())
    
    def SyncSetSlice(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetSlice(arg)
            item = self.GetNextItem()
    
    def SyncSetSliceOrientation(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetSliceOrientation(arg)
            item = self.GetNextItem()
    
    def SyncSetShowAnnotations(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetShowAnnotations(arg)
            item = self.GetNextItem()
    
    def SyncSetShowScalarBar(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetShowScalarBar(arg)
            item = self.GetNextItem()
    
    def SyncSetColorWindow(self, arg):
        '''
        @param arg: double 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetColorWindow(arg)
            item = self.GetNextItem()
    
    def SyncSetColorLevel(self, arg):
        '''
        @param arg: double 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetColorLevel(arg)
            item = self.GetNextItem()
    
    def SyncSetViewOrientation(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            if (isinstance(item, vtkPythonViewImage2D)):
                item.SetViewOrientation(arg)
            item = self.GetNextItem()
    
    def SyncSetViewConvention(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            if (isinstance(item, vtkPythonViewImage2D)):
                item.SetViewConvention(arg)
            item = self.GetNextItem()
    
    def SyncSetInterpolate(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            if (isinstance(item, vtkPythonViewImage2D)):
                item.SetInterpolate(arg)
            item = self.GetNextItem()
    
    def SyncSetInteractorStyleType(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            if (isinstance(item, vtkPythonViewImage2D)):
                item.SetInteractorStyleType(arg)
            item = self.GetNextItem()
    
    def SyncSetOrientationMatrix(self, arg):
        '''
        @param arg: vtkMatrix4x4 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetOrientationMatrix(arg)
            item = self.GetNextItem()
    
    def SyncSetLookupTable(self, arg):
        '''
        @param arg: vtkLookupTable 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetLookupTable(arg)
            item = self.GetNextItem()
    
    def SyncSetTextProperty(self, arg):
        '''
        @param arg: vtkTextProperty 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetTextProperty(arg)
            item = self.GetNextItem()
    
    def SyncSetInput(self, arg):
        '''
        @param arg: vtkImageData 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetInput(arg)
            item = self.GetNextItem()
    
    def SyncSetInputConnection(self, arg):
        '''
        @param arg: vtkAlgorithmOutput 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetInputConnection(arg)
            item = self.GetNextItem()
    
    def SyncSetSize(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetSize(arg)
            item = self.GetNextItem()
    
    def SyncSetPosition(self, arg):
        '''
        @param arg: int 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetPosition(arg)
            item = self.GetNextItem()
    
    def SyncSetWorldCoordinates(self, arg):
        '''
        @param arg: double 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetWorldCoordinates(arg)
            item = self.GetNextItem()
    
    def SyncSetBackground(self, arg):
        '''
        @param arg: double 
        '''
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.SetBackground(arg)
            item = self.GetNextItem()
    
    def SyncAddDataSet(self, dataset, property):
        '''
        @param dataset: vtkDataSet 
        @param property: vtkProperty 
        '''
        pass

    def SyncRemoveDataSet(self, dataset):
        '''
        @param dataset: vtkDataset
        '''
        pass
    
    def SyncResetCamera(self):
        pass
    
    def SyncResetWindowLevel(self):
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.ResetWindowLevel()
            item = self.GetNextItem()
    
    def SyncRender(self):
        self.InitTraversal()
        item = self.GetNextItem()
        while item:
            item.GetRenderWindow().Render()
            item = self.GetNextItem()
    
    def SyncReset(self):
        self.InitTraversal()
        item = self.GetNextItem()
        
        while item:
            item.Reset()
            item = self.GetNextItem()
    
    def SyncStart(self):
        self.InitTraversal()
        item = self.GetNextItem()
        print item.__class__
        while item:
            item.GetInteractor().Start()
            item = self.GetNextItem()

    def getCommand(self):
        return self.__Command


    def setCommand(self, value):
        self.__Command = value


class vtkPythonViewImageCollectionCommand(vtk.vtkObject):
    
    def __init__(self):
        self.__Collection = None
        self.__InitialWindow = 0.0
        self.__InitialLevel = 0.0
    
    def Execute(self, caller, event, callData):
        '''
        Description:
        Satisfy the superclass API for callbacks. Recall that the caller is
        the instance invoking the event; eid is the event id (see
        vtkCommand.h); and calldata is information sent when the callback
        was invoked (e.g., progress value in the vtkCommand::ProgressEvent).
        @param caller: vtkInteractorStyleImage2D
        @param callData: None
        '''
        
        if not self.__Collection:
            return
        isi = caller
        if not isi:
            return
        
        self.getCollection().InitTraversal()
        
        v = self.getCollection().GetNextItem()
        viewer = None
        while v:
            if (isinstance(v, vtkPythonViewImage2D) and 
                isi == v.getInteractorStyleSwitcher()):
                viewer = v
            v = self.getCollection().GetNextItem()
        if not isi or not viewer or not viewer.GetInput():
            return
       
        print event ,": ",isi.getUserEventTag()
        # Reset
        if event == "ResetWindowLevelEvent":
            self.__Collection.SyncResetWindowLevel()
            self.__Collection.SyncRender()
            return
        
        # Reset
        if event == "UserEvent" and isi.getUserEventTag()=="ResetViewerEvent":
            self.__Collection.SyncReset()
            self.__Collection.SyncRender()
            return
        
        # Adjust the window level here
        if event == "WindowLevelEvent":
            self.__Collection.SyncSetColorWindow(viewer.GetColorWindow())
            self.__Collection.SyncSetColorLevel(viewer.GetColorLevel())
            self.__Collection.SyncRender()
            return
        
        # Move
        if event == "UserEvent" and isi.getUserEventTag()=="SliceMoveEvent":
            # do not synchronize this, but render all
            self.__Collection.SyncRender()
        
        # Position requested
        if event == "UserEvent" and isi.getUserEventTag()=="RequestedPositionEvent":
            position = viewer.GetWorldCoordinatesFromDisplayPosition(isi.GetRequestedPosition())
            self.__Collection.SyncSetWorldCoordinates(position)
            self.__Collection.SyncRender()
            
    def getCollection(self):
        return self.__Collection


    def getInitialWindow(self):
        return self.__InitialWindow


    def getInitialLevel(self):
        return self.__InitialLevel


    def setCollection(self, value):
        self.__Collection = value


    def setInitialWindow(self, value):
        self.__InitialWindow = value


    def setInitialLevel(self, value):
        self.__InitialLevel = value




if __name__ == "__main__":
    import sys
    from jolly.ImageSeriesReader import *
    from vtk.util.misc import vtkGetDataRoot
    sys.argv.append("C:/head")
    
    if len(sys.argv)<2:
        sys.exit("Usage:\n\t%s <image file>\nExample: \n\t%s [vtkINRIA3D_DATA_DIR]/MRI.vtk\n" 
                 % (sys.argv[0], sys.argv[0]))
        
    pool = vtkPythonViewImageCollection()
    reader = ImageSeriesReader(sys.argv[1])
    image = vtk.vtkImageData()
    image.DeepCopy(reader.ReadToVTK(".dcm"))
    image.SetOrigin(0,0,0)
    
    view = vtkPythonViewImage2D()
    iren = vtk.vtkRenderWindowInteractor()
    view.SetupInteractor(iren)
    view.SetInput(image)
    view.SetAboutData("C:/head")
    view.SetInteractorStyleTypeToNavigation()
    view.setViewOrientation(vtkPythonViewImage2D.VIEW_ORIENTATION_AXIAL) 
    pool.AddItem(view) # "AddItem" function should be invoke at last
    
    

    view2 = vtkPythonViewImage2D()
    iren2 = vtk.vtkRenderWindowInteractor()
    view2.SetupInteractor(iren2)
    view2.SetInput(image)
    view2.SetAboutData("C:/head")
    view2.setViewOrientation(vtkPythonViewImage2D.VIEW_ORIENTATION_SAGITTAL)
    view2.SetInteractorStyleTypeToNavigation()
    pool.AddItem(view2)
    
    
    view3 = vtkPythonViewImage2D()
    iren3 = vtk.vtkRenderWindowInteractor()
    view3.SetupInteractor(iren3)
    view3.SetInput(image)
    view3.SetAboutData("C:/head")
    view3.setViewOrientation(vtkPythonViewImage2D.VIEW_ORIENTATION_CORONAL)
    view3.SetInteractorStyleTypeToNavigation()
    pool.AddItem(view3)
    
    
    pool.SyncSetSize([400,400])
    pool.InstallCrossAxes()
    
    pool.SyncReset()
    pool.SyncRender()
    #pool.InstallCrossAxes()
    pool.SyncStart() # // Starts all the render interactors related to the pool
    
    