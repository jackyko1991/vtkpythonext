'''
Created on 2009-10-14

@author: summit
'''
import vtk
from jolly.jolly_vtk2.vtkPythonViewImage import *
from jolly.jolly_vtk2.vtkPythonImage3DCroppingBoxCallback import *
from jolly.jolly_vtk2.vtkPythonInteractorStyleTrackballCamera2 import *

class vtkPythonViewImage3D(vtkPythonViewImage):
    '''
    classdocs
    '''
    #===========================================================================
    # 2 rendering modes are possible
    #===========================================================================
    VOLUME_RENDERING = 0
    PLANAR_RENDERING = 1

    def __init__(self):
        '''
        Constructor
        '''
        vtkPythonViewImage.__init__(self)
        
#        texture mapper in 3D: vtkVolumeMapper
        self.__VolumeMapper = None
#        texture mapper in 3D: vtkVolumeTextureMapper3D
        self.__VolumeTextureMapper = vtk.vtkVolumeTextureMapper3D()
#        volume ray cast mapper vtkFixedPointVolumeRayCastMapper
        self.__VolumeRayCastMapper = vtk.vtkFixedPointVolumeRayCastMapper()
#        volume property: vtkVolumeProperty
        self.__VolumeProperty = vtk.vtkVolumeProperty()
#        volume actor: vtkVolume
        self.__VolumeActor = vtk.vtkVolume()
#        opacity transfer function: vtkPiecewiseFunction
        self.__OpacityFunction = vtk.vtkPiecewiseFunction()
#        color transfer function: vtkColorTransferFunction
        self.__ColorFunction = vtk.vtkColorTransferFunction()
        
#        vtkProp3DCollection
        self.__PhantomCollection = vtk.vtkProp3DCollection()
#        blender: vtkImageBlend
        self.__Blender = None
        
#        image 3D cropping box callback: vtkImage3DCroppingBoxCallback
        self.__Callback = vtkPythonImage3DCroppingBoxCallback()
#        box widget: vtkOrientedBoxWidget
#        self.__BoxWidget = vtkOrientedBoxWidget()    # Now I could not wrap vtkOrientedBoxWidget
        self.__BoxWidget = vtk.vtkBoxWidget()
#        vtkPlane widget: vtkPlaneWidget
        self.__PlaneWidget = vtk.vtkPlaneWidget()
#        annotated cube actor: vtkAnnotatedCubeActor, vtkOrientationMarkerWidget
        self.__Cube = vtk.vtkAnnotatedCubeActor()
        self.__Marker = vtk.vtkOrientationMarkerWidget()
        
        self.SetupVolumeRendering()
        self.SetupWidgets()
        
        self.ShowAnnotationsOn()
        self.getTextProperty().SetColor(0, 0, 0)
        self.SetBackground(0.9, 0.9, 0.9) # white
        
        self.__FirstRender = 1
        self.__RenderingMode = self.PLANAR_RENDERING
        self.__VRQuality = 1
        
        self.__InteractorStyleSwitcher = None

    


    def SetVolumeMapperToTexture(self):
        '''
        @return: None
        '''
        self.__VolumeMapper = self.__VolumeTextureMapper
        self.__VolumeActor.SetMapper(self.__VolumeTextureMapper)
        self.__Callback.SetVolumeMapper(self.__VolumeTextureMapper)
        self.SetupTextureMapper()
        
    def SetVolumeMapperToRayCast(self):
        '''
        @return: None
        '''
        self.__VolumeMapper = self.__VolumeRayCastMapper
        self.__VolumeActor.SetMapper(self.__VolumeRayCastMapper)
        self.__Callback.SetVolumeMapper(self.__VolumeRayCastMapper)
    
    def SetVolumeRayCastFunctionToComposite(self):
        '''
        @return: None
        '''
        self.__VolumeRayCastMapper.SetBlendModeToComposite()
    
    def SetVolumeRayCastFunctionToMIP(self):
        '''
        @return: None
        '''
        self.__VolumeMapper.SetBlendModeToMaximumItensity()
        
    def SetBoxWidgetVisibility(self, a):
        '''
        Set the box widget visibility 
        @param a: int 
        @return: None
        '''
        if self.GetInteractor():
            self.__BoxWidget.SetEnabled(a)
    
    def GetBoxWidgetVisibility(self):
        '''
        @return: bool
        '''
        return self.__BoxWidget.GetEnabled()
    
    def BoxWidgetVisibilityOn(self):
        self.SetBoxWidgetVisibility(True)
    
    def BoxWidgetVisibilityOff(self):
        self.SetBoxWidgetVisibility(False)
    
    def SetPlaneWidgetVisibility(self,a):
        '''
        Set the plane widget on
        @param a: int
        @return: None 
        '''
        if self.GetInteractor:
            self.__PlaneWidget.SetEnable(a)
    
    def GetPlaneWidgetVisibility(self):
        '''
        @return: bool
        '''
        return self.__PlaneWidget.GerEnabled()
    
    def PlaneWidgetVisibilityOn(self):
        self.SetPlaneWidgetVisibility(True)
    
    def PlaneWidgetVisibilityOff(self):
        self.SetPlaneWidgetVisibility(False)
        
    def SetCubeVisibility(self, a):
        '''
        Set the cube widget on
        @param a: int
        @return: None
        '''
        if self.GetInteractor():
            self.__Marker.SetEnabled(a)
    def GetCubeVisibility(self):
        return self.__Marker.GetEnabled()
    
    def CubeVisibilityOn(self):
        self.SetCubeVisibility(True)
    
    def CubeVisibilityOff(self):
        self.SetCubeVisibility(False)
    
    def SetShade(self, a):
        '''
        @param a: int
        @return: None 
        '''
        self.__VolumeProperty.SetShade(a)
    
    def GetShade(self):
        '''
        @return: int
        '''
        return self.__VolumeProperty.GetShade()
    
    def ShadeOn(self):
        self.SetShade(True)
    
    def ShadeOff(self):
        self.SetShade(False)
    
    def SetRenderingModeToVR(self):
        '''
        Set the rendering mode to volume rendering (VR).
        @return: None 
        '''
        self.setRenderingMode(self.VOLUME_RENDERING)
    
    def SetRenderingModeToPlanar(self):
        '''
        Set the rendering mode to planar views
        @return: None
        '''
        self.setRenderingMode(self.PLANAR_RENDERING)
    
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
        @return: vtkActor
        '''
        if not dataset or self.getDataSetCollection().IsItemPresent(dataset):
            return None
        
        if vtk.vtkImageData.SafeDownCast(dataset):
            self.SetInput(vtk.vtkImageData.SafeDownCast(dataset))
            return None
        
        geometryextractor = vtk.vtkDataSetSurfaceFilter()
        normalextractor = vtk.vtkPolyDataNormals()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        
        normalextractor.SetFeatureAngle(90)
#        try to skip the normal extraction filter in order to enhance the visualization speed when the data is time sequence.
        
        geometryextractor.SetInput(dataset)
        normalextractor.SetInput(geometryextractor.GetOutput())
        mapper.SetInput(normalextractor.GetOutput())
        actor.SetMapper(mapper)
        if property:
            actor.SetProperty(property)
        
        self.GetRenderer().AddViewProp(actor)
        self.getDataSetCollection().AddItem(dataset)
        self.getProp3DCollection().AddItem(actor)
        
        self.GetRenderer().AddViewProp(actor)
        
        del mapper
        del normalextractor
        del geometryextractor
        del actor
    
    def SetSlice(self, s):
        '''
        Set/Get the current slice to display (depending on the orientation 
         this can be in X, Y or Z).
    
         This method has been overriden in order to generalize the use of this class
         to 2D AND 3D scene visualization. In the 3D case, this method does not do
         anything.
        @param s: int 
        '''
        pass
    
    def SetSliceOrientation(self, orientation):
        '''
        @param orientation: int 
        '''
        pass
    
    def SetWorldCoordinates(self, pos):
        '''
        @param pos: double[3]
        '''
        pass
    
    def UpdateDisplayExtent(self):
        pass
    
    def SetInput(self, input):
        '''
        @param input: vtkImageData 
        '''
        vtkPythonViewImage.SetInput(self, image)
        
        if not image:
            return
        
        size = image.GetDimensions()
        if ((size[0]<2) or (size[1]<2) or (size[2]<2)):
            print "Cannot do volume rendering for a single slice, skipping"
            return
        
        self.__VolumeTextureMapper.SetInput(self.GetInput())
        self.__VolumeRayCastMapper.SetInput(self.GetInput())
        
        if (vtk.vtkVolumeTextureMapper3D.SafeDownCast(self.__VolumeMapper) or
            vtk.vtkVolumeTextureMapper2D.SafeDownCast(self.__VolumeMapper)):
            self.SetupTextureMapper()
        
        self.__BoxWidget.SetInput(self.GetInput())
        self.__BoxWidget.PlaceWidget()
        
        self.__PlaneWidget.SetInput(self.GetInput())
        self.__PlaneWidget.PlaceWidget()
        
        self.GetImageActor().SetVisibility(False)
            
    def SetOrientationMatrix(self, matrix):
        vtkPythonViewImage.SetOrientationMatrix(self, matrix)
        self.__VolumeActor.SetUserMatrix(matrix)
        self.__BoxWidget.SetOrientationMatrix(matrix)
    
    def SetColorWindow(self, s):
        '''
        Description:
        Set window and level for mapping pixels to colors.
        @param s: double 
        '''
        vtkPythonViewImage.SetColorWindow(self, s)
        self.UpdateVolumeFunctions()
    
    def SetColorLevel(self, s):
        '''
        Description:
        Set window and level for mapping pixels to colors.
        @param s: double 
        '''
        vtkPythonViewImage.SetColorLevel(self, s)
        self.UpdateVolumeFunctions()
    
    def SetLookupTable(self, lookuptable):
        '''
        Set a user-defined lookup table
        @param vtkLookupTable: 
        '''
        vtkPythonViewImage.setLookupTable(self, lookuptable)
        self.UpdateVolumeFunctions()
    
    def Add2DPhantom(self, input):
        '''
        @param input: vtkImageActor 
        '''
        if not self.GetRenderer():
            return
        
        cbk = ImageActorCallback()
        actor = vtk.vtkImageActor()
        cbk.setActor(actor)
        actor.SetInput(input.GetInput())
        actor.SetDisplayExtent(input.GetDisplayExtent())
        actor.SetUserMatrix(input.GetUserMatrix())
        actor.SetInterpolate(input.GetInterpolate())
        actor.SetOpacity(input.GetOpacity())
        
        input.AddObserver("ModifiedEvent", lambda obj, even: cbk.Execute(obj, "ModifiedEvent", None))
        
        self.GetRenderer().AddActor(actor)
        actor.SetVisibility(self.__RenderingMode == self.PLANAR_RENDERING)
        
        self.__PhantomCollection.AddItem(actor)
        
#        del actor
#        del cbk
        
#===============================================================================
#       Adding a 2D actor in the 3D scene should be as simple as the next line
#       instead of the code above...
# 
#       Unfortunately it does not seem to work properly. But this is something
#       we should investigate in because it would be much simpler
#===============================================================================
#        self.GetRenderer().AddActor(input)
        
    def SetCameraPosition(self, p):
        '''
        @param p: double 
        '''
        cam = None
        if self.GetRenderer():
            cam = self.GetRenderer().GetActiveCamera()
        if not cam:
            return
        
        cam.SetPosition(p)
    
    def SetCameraFocalPoint(self, p):
        '''
        @param p: double 
        '''
        cam = None
        if self.GetRenderer():
            cam = self.GetRenderer().GetActiveCamera()
        if not cam:
            return
        
        cam.SetFocalPoint(p)
    
    def SetCameraViewUp(self, p):
        '''
        @param p: double
        '''
        cam = None
        if self.GetRenderer():
            cam = self.GetRenderer().GetActiveCamera()
        if not cam:
            return
        
        cam.SetViewUp(p)
        
    def SetVRQualityToLow(self):
        self.setVRQuality(0)
    
    def SetVRQualityToMed(self):
        self.setVRQuality(1)
    
    def SetVRQualityToHigh(self):
        self.setVRQuality(2)
    
    def InstallPipeline(self):
        if (self.GetRenderWindow() and self.GetRenderer()):
            self.GetRenderWindow().AddRenderer(self.GetRenderer())
        if self.GetInteractor():
            self.__InteractorStyleSwitcher = vtkPythonInteractorStyleTrackballCamera2()
            
            self.GetInteractor().SetInteractorStyle(None)
            self.__InteractorStyleSwitcher.SetInteractor(self.GetInteractor())
            
            self.__BoxWidget.SetInteractor(self.GetInteractor())
            self.__PlaneWidget.SetInteractor(self.GetInteractor())
            self.__Marker.SetInteractor(self.GetInteractor())
            self.GetInteractor().SetRenderWindow(self.GetRenderWindow())
            
            self.__Marker.On()
            self.__Marker.InteractiveOff()
            
    
    def UpdateOrientation(self):
        pass
    
    def SetupVolumeRendering(self):
        self.__VolumeTextureMapper.SetSampleDistance(1.0)
        self.__VolumeTextureMapper.SetPreferredMethodToNVidia()
        self.__VolumeTextureMapper.CroppingOn()
        self.__VolumeTextureMapper.SetCroppingRegionFlags(0x7ffdfff)
        
        self.__VolumeRayCastMapper.SetSampleDistance(1.0)
        self.__VolumeRayCastMapper.CroppingOn()
        self.__VolumeRayCastMapper.SetCroppingRegionFlags(0x7ffdfff)
        self.__VolumeRayCastMapper.LockSampleDistanceToInputSpacingOn()
        self.__VolumeRayCastMapper.SetMinimumImageSampleDistance(1.0)
        
        self.__VolumeMapper = self.__VolumeTextureMapper
        
        self.__OpacityFunction.AddPoint(0, 0.0)
        self.__OpacityFunction.AddPoint(255, 1.0)
        self.__ColorFunction.AddRGBPoint(0, 0.0, 0.0, 0.0)
        self.__ColorFunction.AddRGBPoint(255, 1.0, 1.0, 1.0)
        
        self.__VolumeProperty.IndependentComponentsOff()
        self.__VolumeProperty.SetInterpolationTypeToLinear()
        self.__VolumeProperty.ShadeOff()
        self.__VolumeProperty.SetDiffuse(0.9)
        self.__VolumeProperty.SetAmbient(0.15)
        self.__VolumeProperty.SetSpecular(0.3)
        self.__VolumeProperty.SetSpecularPower(15.0)
        self.__VolumeProperty.SetScalarOpacity(self.__OpacityFunction)
        self.__VolumeProperty.SetColor(self.__ColorFunction)
        
        self.__VolumeActor.SetProperty(self.__VolumeProperty)
        self.__VolumeActor.SetMapper(self.__VolumeMapper)
        self.__VolumeActor.PickableOff()
        self.__VolumeActor.DragableOff()
        self.__VolumeActor.SetVisibility(False)
        
        self.__Callback.SetVolumeMapper(self.__VolumeMapper)
        
        self.GetRenderer().AddViewProp(self.__VolumeActor)
    
    def SetupWidgets(self):
#        Create an annotated cube actor (directions)
        self.__Cube.SetXPlusFaceText("L")
        self.__Cube.SetXMinusFaceText("R")
        self.__Cube.SetYPlusFaceText("P")
        self.__Cube.SetYMinusFaceText("A")
        self.__Cube.SetZPlusFaceText("S")
        self.__Cube.SetZMinusFaceText("I")
        self.__Cube.SetZFaceTextRotation(90)
        self.__Cube.SetFaceTextScale(0.65)
        self.__Cube.GetCubeProperty().SetColor(0.5, 1, 1)
        self.__Cube.GetTextEdgesProperty().SetLineWidth(1)
        self.__Cube.GetTextEdgesProperty().SetDiffuse(0)
        self.__Cube.GetTextEdgesProperty().SetAmbient(1)
        self.__Cube.GetTextEdgesProperty().SetColor(0.18, 0.28, 0.23)
        
        #  VTK_MAJOR_VERSION==5 && VTK_MINOR_VERSION>=1
        self.__Cube.SetTextEdgesVisibility(True)
        self.__Cube.SetCubeVisibility(True)
        self.__Cube.SetFaceTextVisibility(True)
        
        # else
#        self.__Cube.TextEdgesOn()
#        self.__Cube.FaceTextOn()
#        self.__Cube.CubeOn()
        
        self.__Cube.GetXPlusFaceProperty().SetColor (1, 0, 0)
        self.__Cube.GetXPlusFaceProperty().SetInterpolationToFlat()
        self.__Cube.GetXMinusFaceProperty().SetColor (1, 0, 0)
        self.__Cube.GetXMinusFaceProperty().SetInterpolationToFlat()
        self.__Cube.GetYPlusFaceProperty().SetColor (0, 1, 0)
        self.__Cube.GetYPlusFaceProperty().SetInterpolationToFlat()
        self.__Cube.GetYMinusFaceProperty().SetColor (0, 1, 0)
        self.__Cube.GetYMinusFaceProperty().SetInterpolationToFlat()
        self.__Cube.GetZPlusFaceProperty().SetColor (0, 0, 1)
        self.__Cube.GetZPlusFaceProperty().SetInterpolationToFlat()
        self.__Cube.GetZMinusFaceProperty().SetColor (0, 0, 1)
        self.__Cube.GetZMinusFaceProperty().SetInterpolationToFlat()
        
        self.__Marker.SetOutlineColor(0.93, 0.57, 0.13)
        self.__Marker.SetOrientationMarker(self.__Cube)
        self.__Marker.SetViewport(0.0, 0.05, 0.15, 0.15)
        
        self.__BoxWidget.RotationEnabledOff()
        self.__BoxWidget.SetPlaceFactor(0.5)
        self.__BoxWidget.SetKeyPressActivationValue('b')
        self.__BoxWidget.AddObserver("InteractionEvent", lambda obj, event: self.__Callback.Execute(obj, event, None))
        
        self.__PlaneWidget.SetKeyPressActivationValue('p')
#        self.__PlaneWidget.NormalToZAxisOn()
        
    
    def SetupTextureMapper(self):
        if not self.GetInput():
            return
        
        mapper3D = vtk.vtkVolumeTextureMapper3D.SafeDownCast(self.__VolumeTextureMapper)
        if mapper3D and not self.GetRenderWindow().GetNeverRendered():
            if not mapper3D.IsRenderSupported(self.__VolumeProperty):
#               try the ATI fragment program implementation
                mapper3D.SetPreferredMethodToFragmentProgram()
                if not mapper3D.IsRenderSupported(self.__VolumeProperty):
                    print "Warning: 3D texture volume rendering is not supported by your hardware, switching to 2D texture rendering."
                    newMapper = vtk.vtkVolumeTextureMapper2D()
                    newMapper.CroppingOn()
                    newMapper.SetCroppingRegionFlags (0x7ffdfff)
                    
                    range = self.GetInput().GetScalarRange()
                    shift = 0 - range[0]
                    scale = 65535.0 / (range[1]-range[0])
                    
                    scaler = vtk.vtkImageShiftScale()
                    scaler.SetInput(self.GetInput())
                    scaler.SetShift(shift)
                    scaler.SetScale(scale)
                    scaler.SetOutputScalarTypeToUnsignedShort()
                    scaler.Update()
                    newMapper.SetInput(scaler.GetOutput())
#                    del scaler
                    self.__Callback.SetVolumeMapper(newMapper)
                    self.__VolumeMapper = newMapper
                    self.__VolumeMapper.SetMapper(newMapper)
#                    def newMapper
    
    def UpdateVolumeFunctions(self):
        v_min = self.GetColorLevel() - 0.5*self.GetColorWindow()
        v_max = self.GetColorLevel() + 0.5*self.GetColorWindow()
        scaleOpacity = 1.4
        
        if self.getLookupTable():
            self.__ColorFunction.RemoveAllPoints()
            
            numColors = self.getLookupTable().GetNumberOfTableValues()
#            self.__OpacityFunction.AddPoint(0.0, 0.0)
#            self.__OpacityFunction.AddPoint(v_min, 0.0)
            for i in range(numColors):
                color = self.getLookupTable().GetTableValue(i)
                self.__ColorFunction.AddRGBPoint(v_min + float(i)*(v_max-v_min)/(numColors-1), color[0], color[1], color[2])
        self.__OpacityFunction.RemoveAllPoints()
        self.__OpacityFunction.AddPoint(0.0, 0.0)
        self.__OpacityFunction.AddPoint(v_min, 0.0)
        self.__OpacityFunction.AddPoint(v_max, 1.0/scaleOpacity)
        
    def getVolumeMapper(self):
        return self.__VolumeMapper


    def getVolumeTextureMapper(self):
        return self.__VolumeTextureMapper


    def getVolumeRayCastMapper(self):
        return self.__VolumeRayCastMapper


    def getVolumeProperty(self):
        return self.__VolumeProperty


    def getVolumeActor(self):
        return self.__VolumeActor


    def getOpacityFunction(self):
        return self.__OpacityFunction


    def getColorFunction(self):
        return self.__ColorFunction


    def getPhantomCollection(self):
        return self.__PhantomCollection


    def getBlender(self):
        return self.__Blender


    def getCallback(self):
        return self.__Callback


    def getBoxWidget(self):
        return self.__BoxWidget


    def getPlaneWidget(self):
        return self.__PlaneWidget


    def getMarker(self):
        return self.__Marker


    def getRenderingMode(self):
        '''
        Get the current rendering mode.
        '''
        return self.__RenderingMode


    def getVRQuality(self):
        return self.__VRQuality


    def setVolumeMapper(self, value):
        self.__VolumeMapper = value


    def setVolumeTextureMapper(self, value):
        self.__VolumeTextureMapper = value


    def setVolumeRayCastMapper(self, value):
        self.__VolumeRayCastMapper = value


    def setVolumeProperty(self, value):
        self.__VolumeProperty = value


    def setVolumeActor(self, value):
        self.__VolumeActor = value


    def setOpacityFunction(self, value):
        self.__OpacityFunction = value


    def setColorFunction(self, value):
        self.__ColorFunction = value


    def setPhantomCollection(self, value):
        self.__PhantomCollection = value


    def setBlender(self, value):
        self.__Blender = value


    def setCallback(self, value):
        self.__Callback = value


    def setBoxWidget(self, value):
        self.__BoxWidget = value


    def setPlaneWidget(self, value):
        self.__PlaneWidget = value


    def setMarker(self, value):
        self.__Marker = value


    def setRenderingMode(self, arg):
        self.__RenderingMode = arg
        self.__VolumeActor.SetVisibility(arg == self.VOLUME_RENDERING)
        
        self.__PhantomCollection.InitTraversal()
        actor = self.__PhantomCollection.GetNextProp3D()
        while actor:
            actor.SetVisibility( arg==self.PLANAR_RENDERING )
            actor = self.__PhantomCollection.GetNextProp3D()


    def setVRQuality(self, v):
        self.__VRQuality = v
        distance = 0
        number = 0
        if v == 0: #low
            distance = 5.0
            number = 64
        elif v == 1: # med
            distance = 2.5
            number = 128
        elif v == 2: #high
            distance = 1.0
            number = 256
        else:
            pass
        mapper = vtk.vtkFixedPointVolumeRayCastMapper.SafeDownCast(self.__VolumeMapper)
        if mapper:
            mapper.SetMinimumImageSampleDistance(distance)
        mapper = vtk.vtkVolumeTextureMapper3D.SafeDownCast(self.__VolumeMapper)
        if mapper:
            mapper.SetSampleDistance(distance)
        mapper = vtk.vtkVolumeTextureMapper2D.SafeDownCast(self.__VolumeMapper)
        if mapper:
            mapper.SetMaximumNumberOfPlanes(number)
        self.__VRQuality = v

    def getInteractorStyleSwitcher(self):
        return self.__InteractorStyleSwitcher


    def setInteractorStyleSwitcher(self, value):
        self.__InteractorStyleSwitcher = value
        
class ImageActorCallback(vtk.vtkObject):
    
    def __init__(self):
        self.__Actor = None

  

    def getActor(self):
        return self.__Actor


    def setActor(self, value):
        self.__Actor = value

    
    def Execute(self, caller, event, callData):
        if not self.__Actor:
            return
        
        imagecaller = vtk.vtkImageActor.SafeDownCast(caller)
        if imagecaller and event=="ModifiedEvent":
            self.__Actor.SetInput(imagecaller.GetInput())
            self.__Actor.SetInterpolate(imagecaller.GetInterpolate())
            self.__Actor.SetOpacity(imagecaller.GetOpacity())
            self.__Actor.SetDisplayExtent(imagecaller.GetDisplayExtent())
            self.__Actor.SetUserMatrix(imagecaller.GetUserMatrix())

        
if __name__=="__main__":
    import sys
    from jolly.ImageSeriesReader import *
    from jolly.jolly_vtk2.vtkPythonViewImage2D import *
    from jolly.jolly_vtk2.vtkPythonViewImageCollection import *
    
    from vtk.util.misc import vtkGetDataRoot
    sys.argv.append("C:/S70")
    matrix = vtk.vtkMatrix4x4()
    matrix.DeepCopy([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1])
#    matrix.Identity()
#    matrix.SetElement(0, 0, 1)
#    matrix.SetElement(0, 1, 1)
#    matrix.SetElement(0, 2, 1)
#    matrix.SetElement(1, 0, 1)
#    matrix.SetElement(1, 1, 1)
#    matrix.SetElement(1, 2, 1)
#    matrix.SetElement(2, 0, 1)
#    matrix.SetElement(2, 1, 1)
#    matrix.SetElement(2, 2, 1)
#    matrix.SetElement(3, 0, 1)
#    matrix.SetElement(3, 1, 1)
#    matrix.SetElement(3, 2, 1)
    
    
    if len(sys.argv)<2:
        sys.exit("Usage:\n\t%s <image file>\nExample: \n\t%s [vtkINRIA3D_DATA_DIR]/MRI.vtk\n" 
                 % (sys.argv[0], sys.argv[0]))
        
    pool = vtkPythonViewImageCollection()
    reader = ImageSeriesReader(sys.argv[1])
    image = vtk.vtkImageData()
    image.DeepCopy(reader.ReadToVTK(""))
    image.SetOrigin(0,0,0)
    

    view3d = vtkPythonViewImage3D()
    iren3d = vtk.vtkRenderWindowInteractor()
    view3d.SetupInteractor(iren3d)
    
    pool.AddItem(view3d)
    
    view = vtkPythonViewImage2D()
    iren = vtk.vtkRenderWindowInteractor()
    view.SetupInteractor(iren)
    view.SetInput(image)
    view.SetAboutData("C:/S70")
    view.SetInteractorStyleTypeToNavigation()
    view.setViewOrientation(vtkPythonViewImage2D.VIEW_ORIENTATION_AXIAL) 
    view.setOrientationMatrix(matrix)
    pool.AddItem(view) # "AddItem" function should be invoke at last
    view3d.Add2DPhantom(view.GetImageActor())
    print view.getOrientationMatrix()
    

    view2 = vtkPythonViewImage2D()
    iren2 = vtk.vtkRenderWindowInteractor()
    view2.SetupInteractor(iren2)
    view2.SetInput(image)
    view2.SetAboutData("C:/S70")
    view2.setViewOrientation(vtkPythonViewImage2D.VIEW_ORIENTATION_SAGITTAL)
    view2.SetInteractorStyleTypeToNavigation()
#    view2.setOrientationMatrix(matrix)
    pool.AddItem(view2)
    view3d.Add2DPhantom(view2.GetImageActor())
    print view2.getOrientationMatrix()
    
    view3 = vtkPythonViewImage2D()
    iren3 = vtk.vtkRenderWindowInteractor()
    view3.SetupInteractor(iren3)
    view3.SetInput(image)
    view3.SetAboutData("C:/S70")
    view3.setViewOrientation(vtkPythonViewImage2D.VIEW_ORIENTATION_CORONAL)
    view3.SetInteractorStyleTypeToNavigation()
#    view3.setOrientationMatrix(matrix)
    pool.AddItem(view3)
    view3d.Add2DPhantom(view3.GetImageActor())
    print view3.getOrientationMatrix()
    
    firstview = pool.GetItem(1)
    if firstview:
        view3d.SetInput(firstview.GetInput())
#        view3d.setOrientationMatrix(matrix)
#        view3d.SetRenderingModeToPlanar()
        view3d.SetRenderingModeToVR()
        view3d.InstallPipeline()
    
    
    pool.SyncSetSize([400,400])
    pool.InstallCrossAxes()
#    pool.SyncSetRefWindowLevel(1650,-1350)
    pool.SyncReset()
    pool.SyncRender()
    
    #pool.InstallCrossAxes()
    pool.SyncStart() # // Starts all the render interactors related to the pool
    
        