'''
Created on 2009-10-13

@author: summit
'''
import math
import vtk
class vtkPythonViewImage(vtk.vtkImageViewer2):
    '''
    \class vtkViewImage 
   \brief This class is a top-level convenience class for displaying a scalar - or RGB
   image in a 2D or 3D scene.

   It inherits from the vtkImageViewer2 class, which is initially designed for 2D scene
   visualization. However, vtkViewImage overrides some of its parents' methods (SetSlice())
   in order to generalize its purpose to 2D AND 3D scene visualization.

   As a high-level class, it provides the user with convinient functionalities
   such as a colormap (SetLookupTable()), a scalar bar (ScalarBarActor), some corner annotations
   (CornerAnnotation), access to the background color (SetBackground()), the
   annotation text properties (SetTextProperty()), or a call for reseting to default values
   (Reset() or ResetCamera()).

   
   The principle add-on of this class is to tacke the common issue of placing
   different objects in a same consistent reference frame. In a world coordinates system, an
   volume image can be localized by its origin and its spacing, and an orientation vector defining
   how to rotate the volume to be consistent with reality.

   The vtkImageData class has among its attributes the origin and the spacing information.
   However, the orientation information is missing.

   The vtkViewImage class tackle this lack by providing the user the possibility to set an
   orientation matrix with SetOrientationMatrix(). This matrix will directly be applied to the
   actor describing the image in the 2D - or 3D - scene. The rotation 3x3 component of this matrix
   has to be orthogonal (no scaling). The offset component may contain the origin information.
   In this case the user will have to make sure that this information is absent from the vtkImageData
   instance given in SetInput(). For that you can call : view->GetInput()->SetOrigin(0,0,0).
    '''
    
    #===========================================================================
    # The number of DirectionIds
    #===========================================================================
    
    X_ID = 0
    Y_ID = 1
    Z_ID = 2
    NB_DIRECTION_IDS = 3
    
    #==========================================================================
    # The number of PlanIds
    #==========================================================================
    SAGITTAL_ID = 0
    CORONAL_ID = 1
    AXIAL_ID = 2
    NB_PLAN_IDS = 3

    def __init__(self):
        '''
        Constructor
        '''
        
        self.__OrientationMatrix = vtk.vtkMatrix4x4()
        self.__CornerAnnotation = vtk.vtkCornerAnnotation()
        self.__TextProperty = vtk.vtkTextProperty()
        self.__LookupTable = vtk.vtkLookupTable()
        self.__ScalarBarActor = vtk.vtkScalarBarActor()
        self.__Prop3DCollection = vtk.vtkProp3DCollection()
        self.__DataSetCollection = vtk.vtkDataSetCollection()
        self.__OrientationTransform = vtk.vtkMatrixToLinearTransform()
        
        self.__OrientationMatrix.Identity()
        self.__CornerAnnotation.SetNonlinearFontScaleFactor(0.30)
        self.__CornerAnnotation.SetText(0, "Jolly - (c) summit 2009 ref vtkINRIA3D")
        self.__CornerAnnotation.SetMaximumFontSize(46)
        
        self.__ScalarBarActor.SetLabelTextProperty(self.__TextProperty)
        
        self.__ScalarBarActor.GetLabelTextProperty().BoldOff()
        self.__ScalarBarActor.GetLabelTextProperty().ItalicOff()
        self.__ScalarBarActor.SetNumberOfLabels(3)
        self.__ScalarBarActor.SetWidth(0.1)
        self.__ScalarBarActor.SetHeight(0.5)
        self.__ScalarBarActor.SetPosition(0.9, 0.3)
        self.__LookupTable.SetTableRange(0, 1)
        self.__LookupTable.SetSaturationRange(0, 0)
        self.__LookupTable.SetHueRange(0, 0)
        self.__LookupTable.SetValueRange(0, 1)
        self.__LookupTable.Build()
        
        self.__ShowAnnotations = True
        self.__ShowScalarBar = True
        
        self.__OrientationTransform.SetInput(self.__OrientationMatrix)
        
        self.__WindowLevel = self.GetWindowLevel()
        self.__WindowLevel.SetLookupTable( self.__LookupTable )
        self.__ScalarBarActor.SetLookupTable(self.__LookupTable)
        
        self.__Renderer = self.GetRenderer()
        self.__Renderer.AddViewProp(self.__CornerAnnotation)
        self.__Renderer.AddViewProp(self.__ScalarBarActor)
        
        self.__ImageActor = self.GetImageActor()
        self.__RenderWindow = self.GetRenderWindow ()
        self.__InteractorStyle = self.GetInteractorStyle()
        self.__Interactor = None
        
        self.__CornerAnnotation.SetWindowLevel(self.__WindowLevel)
        self.__CornerAnnotation.SetImageActor(self.__ImageActor)
        self.__CornerAnnotation.ShowSliceAndImageOn()
        
    
    def SetInput(self, input):
        '''
        @param input: vtkImageData
        @return: None
        '''
        vtk.vtkImageViewer2.SetInput(self, input)
    
    def Render(self):
        '''
        Render the resulting image.
        @return: None
        '''
#        if (self.GetInput() and self.__RenderWindow 
#                            and not self.__RenderWindow.GetNeverRendered()):
        if self.GetInput() and self.__RenderWindow:
            vtk.vtkImageViewer2.Render(self)
            
        
    def SetupInteractor(self, iren):
        '''
        @param iren: vtkRenderWindowInteractor
        @return: None
        '''
        self.__Interactor = iren
        vtk.vtkImageViewer2.SetupInteractor(self, self.__Interactor)
        
    def GetInteractor(self):
        '''
        Access to the RenderWindow interactor
        @return: vtkRenderWindowInteractor
        '''
        return self.__Interactor
    
    def SetWorldCoordinates(self, x, y, z):
        '''
        The world is not always what we think it is ...

         Use this method to move the viewer slice such that the position
         (in world coordinates) given by the arguments is contained by
         the slice plane. If the given position is outside the bounds
         of the image, then the slice will be as close as possible.
         @param x:double
         @param y:double
         @param z:double   
        '''
        pos=[x, y, z]
        self.SetWorldCoordinatesByArray(pos)
    
    def SetWorldCoordinatesByArray(self, pos):
        '''
        @param pos:double[3] 
        '''
        pass

    def AddDataSet(self, dataset, property=None):
        '''
        Add a dataset to the view (has to be subclass of vtkPointSet).
        The dataset will be cut through the implicit slice plane
        (GetImplicitSlicePlane()).
    
        This results in a loss of dimensionality, i.e. tetrahedron will be displayed
        as triangles, triangles as lines, lines as points.
        A vtkProperty of the dataset can be specified.
        @param dataset: vtkDataSet
        @param property: vtkProperty
        '''
        return None
    
    def RemoveDataSet(self, dataset):
        '''
        @param dataset: vtkDataSet
        @return: bool
        '''
        index = self.__DataSetCollection.IsItemPresent(dataset)
        if not index:
            return False
        self.__Renderer.RemoveViewProp(self.__Prop3DCollection.GetItemAsObject(index))
        self.__DataSetCollection.RemoveItem(index)
        self.__Prop3DCollection.RemoveItem(index)
        return True
    
    def SetSlice(self, s):
        '''
         Set/Get the current slice to display (depending on the orientation 
         this can be in X, Y or Z).
    
         This method has been overriden in order to generalize the use of this class
         to 2D AND 3D scene visualization. Thus in this top-level class SetSlice() does
         not do anything.
         @param s:int 
        '''
        vtk.vtkImageViewer2.SetSlice(self, s)
    
    def Update(self):
        '''
        @return: None
        '''
        pass
    
    def GetWorldCoordinatesFromImageCoordinates(self, indices):
        '''
        Convert an indices coordinate point (image coordinates) into a world coordinate point
        @param indices:int[3]
        @return: double[3]
        '''
        if not self.GetInput():
            return [0.0, 0.0, 0.0]
        
        # Get information
        spacing = self.GetInput().GetSpacing()
        origin = self.GetInput().GetOrigin()
        
        unorientedposition = [0.0]*4
        for i in range(3):
            unorientedposition[i] = origin[i] + spacing[i]*indices[i]
        unorientedposition[3] = 1
        
        # apply orientation matrix 
        position = unorientedposition
        if self.getOrientationMatrix():
            self.getOrientationMatrix().MultiplyPoint(unorientedposition, position)
        return position
    
    def GetImageCoordinatesFromWorldCoordinates(self, position):
        '''
        Convert a world coordinate point into an image indices coordinate point
        @param position: double[3]
        @return: int[3] 
        '''
        if not self.GetInput():
            return [0.0, 0.0, 0.0]
        
        # Get information
        unorientedposition = [position[0], position[1], position[2], 1]
        spacing = self.GetInput().GetSpacing()+[0.0]
        origin = self.GetInput().GetOrigin()+[0.0]
        
        #  apply inverted orientation matrix to the world-coordinate position
        inverse = vtk.vtkMatrix4x4()
        vtk.vtkMatrix4x4.Invert(self.getOrientationMatrix(), inverse)
        inverse.MultiplyPoint(unorientedposition, unorientedposition)
        
        indices = [0]*3
        for i in range[3]:
            if math.fabs(spacing[i]) > 1e-5:
                indices[i] = vtk.vtkMath.Round((unorientedposition[i]-origin[i])/spacing[i])
            else:
                indices[i] = 0
        del inverse
        return indices
        
    
    def GetValueAtPosition(self, worldcoordinates, component=0):
        '''
         Get the pixel value at a given world coordinate point in space, return
         zero if out of bounds.
         @param worldcoordinates: double[3]
         @param component:int
         @return: double 
        '''
        if not self.GetInput():
            return 0.0
        
        indices = self.GetImageCoordinatesFromWorldCoordinates(worldcoordinates)
        extent = self.GetInput().GetWholeExtent()
        if ( (indices[0] < extent[0]) or (indices[0] > extent[1])
             or (indices[1] < extent[2]) or (indices[1] > extent[3])
             or (indices[2] < extent[4]) or (indices[2] > extent[5])):
            return 0
        else:
            return self.GetInput().GetScalarComponentAsDouble(indices[0], indices[1],
                                                              indices[2], component)
    
    def SetBackgroundByRGB(self, rgb):
        '''
        Set the background color. Format is RGB, 0 <= R,G,B <=1
         Example: SetBackground(0.9,0.9,0.9) for grey-white.
         @param rgb:double[3]
         @return: None 
        '''
        if self.__Renderer:
            self.__Renderer.SetBackground(rgb)
    
    def SetBackground(self, r, g, b):
        '''
        @param r:double
        @param g:double
        @param b:double   
        @return: None
        '''
        rgb = [r,g,b]
        self.SetBackgroundByRGB(rgb)
    
    def GetBackground(self):
        '''
        @return: double[3]
        '''
        if self.__Renderer:
            return self.__Renderer.GetBackground()
        return None
    
    def ResetCamera(self):
        '''
         Reset the camera
         @return: None
        '''
        if self.__Renderer:
            self.__Renderer.ResetCamera()
    
    def Reset(self):
        '''
        Reset position - zoom - window/level to default
        @return: None
        '''
        self.Update()
        self.ResetCamera()
        self.ResetWindowLevel()
    
    def ShowAnnotationsOn(self):
        '''
        Show the annotations.
        @return: None
        '''
        self.setShowAnnotations(True)
    
    def ShowAnnotationsOff(self):
        '''
        Hide the annotations.
        @return: None
        '''
        self.setShowAnnotations(False)
    
    def Enable(self):
        '''
        Enable interaction on the view.
        @return: None
        '''
        self.__Interactor.Enable()
    
    def Disable(self):
        '''
        Disable interaction on the view.
        @return: None
        '''
        self.__ImageActor.Disable()
    
    def GetEnabled(self):
        '''
        Enable or Disable interaction on the view.
        @return: int
        '''
        return self.__Interactor.GetEnable()
        
    def ShowScalarBarOn(self):
        '''
        Show the scalarbar
        @return: None
        '''
        self.setScalarBarActor(True)
    
    def ShowScalarBarOff(self):
        '''
        Hide the scalarbar
        @return: None
        '''
        self.setScalarBarActor(False)
    
    def SetColorWindow(self, s):
        '''
        Set window for mapping pixels to colors.
        @param s:double
        @return: None
        '''
        if s<0:
            s = 1.0
        vtk.vtkImageViewer2.SetColorWindow(self, s)
        v_min = self.GetColorLevel() - 0.5*s
        v_max = self.GetColorLevel() + 0.5*s
        self.getLookupTable().SetRange(v_min, v_max)
    
    def SetColorLevel(self, s):
        '''
        Set  level for mapping pixels to colors.
        @param s:double
        @return: None
        '''
        vtk.vtkImageViewer2.SetColorLevel(self, s)
        v_min = s - 0.5*self.GetColorWindow()
        v_max = s + 0.5*self.GetColorWindow()
        self.getLookupTable().SetRange(v_min, v_max)
    
    def ResetWindowLevel(self):
        '''
        Reset the window level
        @return: None
        '''
        if not self.GetInput():
            return
        range = self.GetInput().GetScalarRange()
        window = range[1] - range[0]
        level = 0.5*(range[1]+range[0])
        
        self.SetColorWindow(window)
        self.SetColorLevel(level)
    

    def getOrientationMatrix(self):
        '''
        The OrientationMatrix instance (GetOrientationMatrix()) is a very important
         added feature of this viewer. It describes the rotation and translation to
         apply to the image bouding box (axis aligned) to the world coordinate system.
    
         Rotation part is usually given by the GetDirection() method on an itk::Image
         for instance. Translation usually correspond to the origin of the image given
         by GetOrigin() on an itk::Image.
    
         CAUTION: if you provide non-zero origin to the viewer vtkImageData input
         (SetInput()), then don't provide translation to the OrientationMatrix instance,
         otherwise the information is redundant.
         
         The best behaviour is to force the origin of the vtkImageData input to zero and
         provide this origin information in the OrientationMatrix.
        @return: vtkMatrix4x4
        '''
        return self.__OrientationMatrix


    def getCornerAnnotation(self):
        '''
        make the corner annotation such that it follows the slice number, the 
        image scalar value at cursor, the spacing, etc
        @return: vtkCornerAnnotation  
        '''
        return self.__CornerAnnotation


    def getTextProperty(self):
        '''
        The TextProperty instance (GetTextProperty()) describes the font and
         other settings of the CornerAnnotation instance (GetCornerAnnotation())
         @return: vtkTextProperty
        '''
        return self.__TextProperty


    def getLookupTable(self):
        '''
         The LookupTable instance (GetLookupTable()) can be used to set a user-defined
         color-table to the viewer. Default is a linear black to white table.
         @return: vtkLookupTable
        '''
        return self.__LookupTable


    def getScalarBarActor(self):
        '''
        make this scalar bar actually follow the WindowLevel filter. It does 
        not seems to work yet
        @return: vtkScalarBarActor
        '''
        return self.__ScalarBarActor


    def getProp3DCollection(self):
        '''
        Access to the actor collection.
        @return: vtkProp3DCollection
        '''
        return self.__Prop3DCollection


    def getDataSetCollection(self):
        '''
        Access to the dataset collection.
        @return: vtkDataSetCollection
        '''
        return self.__DataSetCollection


    def getOrientationTransform(self):
        return self.__OrientationTransform


    def getShowAnnotations(self):
        '''
        Show/Hide the annotations.
        @return: int
        '''
        return self.__ShowAnnotations


    def getShowScalarBar(self):
        '''
        Show/Hide the scalarbar.
        @return: int
        '''
        return self.__ShowScalarBar


    def setOrientationMatrix(self, matrix):
        '''
        @param matrix: vtkMatrix4x4
        @return: None
        '''
        if self.__OrientationMatrix == matrix:
            return
        self.__OrientationMatrix = matrix
        self.Modified()
        
        self.__ImageActor.SetUserMatrix(self.__OrientationMatrix)
        self.__OrientationTransform.SetInput(self.__OrientationMatrix)


    def setCornerAnnotation(self, value):
        self.__CornerAnnotation = value


    def setTextProperty(self, textproperty):
        '''
        @param textproperty: vtkTextProperty
        @return: None
        '''
        if self.__TextProperty == textproperty:
            return
        self.__TextProperty = textproperty
        self.Modified()
        
        self.__CornerAnnotation.SetTextProperty(self.__TextProperty)

    def setLookupTable(self, lookuptable):
        '''
        @param lookuptable: vtkLoopupTable
        @return: None
        '''
        if self.__LookupTable == lookuptable:
            return
        self.__LookupTable = lookuptable
        self.Modified()
        
        self.__WindowLevel.SetLookupTable(self.__LookupTable)
        self.__ScalarBarActor.SetLookupTable(self.__LookupTable)
        v_min = self.GetColorLevel() - 0.5*self.GetColorWindow()
        v_max = self.GetColorLevel() + 0.5*self.GetColorWindow()
        self.getLookupTable().SetRange(v_min, v_max)


    def setScalarBarActor(self, value):
        self.__ScalarBarActor = value


    def setProp3DCollection(self, value):
        self.__Prop3DCollection = value


    def setDataSetCollection(self, value):
        self.__DataSetCollection = value


    def setOrientationTransform(self, value):
        self.__OrientationTransform = value


    def setShowAnnotations(self, value):
        '''
        Show/Hide the annotations.
        @param value:int
        @return: None 
        '''
        self.__ShowAnnotations = value
        self.__CornerAnnotation.SetVisibility(value)


    def setShowScalarBar(self, value):
        '''
         Show/Hide the scalarbar.
         @param value: int 
         @return: None
        '''
        self.__ShowScalarBar = value
        self.ScalarBarActor.SetVisibility(value)

if __name__ == '__main__':
    import sys
    from jolly.ImageSeriesReader import *
    from vtk.util.misc import vtkGetDataRoot
    sys.argv.append("C:/head")
    
    if len(sys.argv)<2:
        sys.exit("Usage:\n\t%s <image file>\nExample: \n\t%s [vtkINRIA3D_DATA_DIR]/MRI.vtk\n" 
                 % (sys.argv[0], sys.argv[0]))
    
    #===========================================================================
    # Create 3 views, each of them will have a different orientation, .i.e.
    # axial, sagittal and coronal.
    #===========================================================================
    view1 = vtkPythonViewImage()
    iren1 = vtk.vtkRenderWindowInteractor()
    view1.SetupInteractor(iren1)
    view1.SetBackground(0.0, 0.0, 0.0)
    
    reader = ImageSeriesReader(sys.argv[1])
#    v16 = vtk.vtkVolume16Reader()
#    v16.SetDataDimensions(64, 64)
#    v16.SetDataByteOrderToLittleEndian()
#    v16.SetFilePrefix(os.path.join(vtkGetDataRoot(),
#                                   "Data", "headsq", "quarter"))
#    v16.SetImageRange(1, 93)
#    v16.SetDataSpacing(3.2, 3.2, 1.5)
#    v16.Update()
#    
#    image = v16.GetOutput()
    
    image = vtk.vtkImageData()
    # must use deepcopy the convert imagedata
    image.DeepCopy(reader.ReadToVTK(".dcm"))    
    
    image.SetOrigin(0,0,0)
    view1.SetInput(image)
    
    view1.Render()

    
    iren1.Start()
    
    
        