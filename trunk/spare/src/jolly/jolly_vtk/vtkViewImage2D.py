# -*- coding:utf-8 -*-
"""
Created on 2009-10-6

@author: summit
"""

import vtk
from vtkViewImage import *
from vtkInteractorStyleImage2D import *
from vtkViewImage2DCommand import *


class vtkViewImage2D(vtkViewImage):
    
    # InteractionStyleIds
    NO_INTERACTION = 0
    SELECT_INTERACTION = 1
    WINDOW_LEVEL_INTERACTION = 2
    FULL_PAGE_INTERACTION = 3
    MEASURE_INTERACTION = 4
    ZOOM_INTERACTION = 5
    
    # ConventionIds
    RADIOLOGIC = 0
    NEUROLOGIC = 1
    
    # Initialize static member that controls display convention (0: radiologic,
    #                                                            1: neurologic)
    vtkViewImage2DDisplayConventions = 0
    
    def SetViewImage2DDisplayConventions(self, val):
        self.vtkViewImage2DDisplayConventions = val
    
    def GetViewImage2DDisplayConventions(self):
        return self.vtkViewImage2DDisplayConventions
    
    def __init__(self):
        vtkViewImage.__init__(self)
        
        self.FirstRender = 1
        self.FirstImage = 1
        self.ShowCurrentPoint = True
        self.ShowDirections = True
        self.ShowSliceNumber = True
        self.Orientation = vtkViewImage.AXIAL_ID
        self.InteractionStyle = self.SELECT_INTERACTION
        self.LeftButtonInteractionStyle = self.SELECT_INTERACTION
        self.MiddleButtonInteractionStyle = self.SELECT_INTERACTION
        self.RightButtonInteractionStyle = self.SELECT_INTERACTION
        self.WheelInteractionStyle = self.SELECT_INTERACTION
        
        self.Conventions = self.RADIOLOGIC
        
        self.InitialParallelScale = 1.0
        
        self.OverlappingImage = None
        
        self.ImageReslice = vtk.vtkImageReslice()
        self.ImageActor = vtk.vtkImageActor()
        self.WindowLevelForCorner = vtk.vtkImageMapToWindowLevelColors()
        self.WindowLevel = vtk.vtkImageMapToColors()
        #self.MaskFilter = vtk.vtkImageBlendWithMask()
        self.Blender = vtk.vtkImageBlend()
        
        self.HorizontalLineSource = vtk.vtkLineSource()
        self.VerticalLineSource = vtk.vtkLineSource()
        self.HorizontalLineActor = vtk.vtkActor()
        self.VerticalLineActor = vtk.vtkActor()
        
        self.DataSetCutPlane = vtk.vtkPlane()
        self.DataSetCutBox = vtk.vtkBox()
        
        self.DataSetCutPlane.SetOrigin(0,0,0)
        self.DataSetCutPlane.SetNormal(0,0,1)
        self.DataSetCutBox.SetBounds(0, 0, 0, 0, 0, 0)
        self.BoxThickness = 2
        
        self.LinkCameraFocalAndPosition = 0
        
        # set the filters properties
        self.Blender.SetBlendModeToNormal()
        self.Blender.SetOpacity(0, 0.25)
        self.Blender.SetOpacity(1, 0.75)
        
        # set up the vtk pipeline
        self.ImageReslice.SetOutputDimensionality(2)
        self.ImageReslice.InterpolateOff()
        self.ImageReslice.SetInputConnection(self.WindowLevel.GetOutputPort())
        
        self.AuxInput = self.WindowLevel.GetOutput()
        self.ResliceInput = self.WindowLevel.GetOutput()
        
        # Interactor Style
        self.InitInteractorStyle(self.SELECT_INTERACTION)
        
        # Initialize cursor lines
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.HorizontalLineSource.GetOutputPort())
        self.HorizontalLineActor.SetMapper(mapper)
        self.HorizontalLineActor.GetProperty().SetColor(1.0, 0.0, 0.0)
        #del mapper
        self.HorizontalLineActor.SetVisibility(0)
        
        mapper2 = vtk.vtkPolyDataMapper()
        mapper2.SetInputConnection(self.VerticalLineSource.GetOutputPort())
        self.VerticalLineActor.SetMapper(mapper2)
        self.VerticalLineActor.GetProperty().SetColor(1.0, 0.0, 0.0)
        #del mapper2
        self.VerticalLineActor.SetVisibility(0)
        
        self.CornerAnnotation.SetWindowLevel(self.WindowLevelForCorner)
        self.SetOrientation(vtkViewImage.AXIAL_ID)
        
        if self.GetViewImage2DDisplayConventions() == 0:
            self.SetConventionsToRadiological()
        else:
            self.SetConventionsToNeurological()
        
   
    
    # Set the type of user interaction to all mouse buttons at once.
    def SetInteractionStyle(self, style):
        if self.LeftButtonInteractionStyle == self.InteractionStyle:
            self.LeftButtonInteractionStyle = style
        if self.MiddleButtonInteractionStyle == self.InteractionStyle:
            self.MiddleButtonInteractionStyle = style
        if self.RightButtonInteractionStyle == self.InteractionStyle:
            self.RightButtonInteractionStyle = style
        if self.WheelInteractionStyle == self.InteractionStyle:
            self.WheelInteractionStyle = style
        self.InteractionStyle = style
    
    def Update(self):
        self.UpdateImageActor()
        self.UpdatePosition()
        self.InitializeImagePositionAndSize()
    
    def Initialize(self):
        vtkViewImage.Initialize(self)
        
        if self.Renderer:
            self.Renderer.TwoSidedLightingOff()
    
    def SetVisibility(self, state):
        self.ImageActor.SetVisibility(state)
    
    def GetVisibility(self):
        return self.ImageActor.GetVisibility()
    
    def UpdateImageActor(self):
        if not self.Image:
            return
        print self.ImageReslice.GetOutput()
        print self.AuxInput
        print self.WindowLevel.GetInput()
        
        self.ImageReslice.GetOutput().UpdateInformation()
        self.ImageActor.GetInput().SetUpdateExtent(self.ImageReslice.GetOutput().GetWholeExtent())
        self.ImageActor.SetDisplayExtent(self.ImageReslice.GetOutput().GetWholeExtent())
        
        self.FirstRender = 1
    
    def InitializeImagePositionAndSize(self):
        if not self.Image:
            return
        
        if self.FirstRender:
            # make sur the input is up-to-date
            self.ImageActor.GetInput().Update()
            
            self.Renderer.GetActiveCamera().OrthogonalizeViewUp()
            self.Renderer.GetActiveCamera().ParallelProjectionOn()
            
            #  Get the bounds of the image: coordinates in the real world
            bnds = self.ImageActor.GetBounds()
            
            # extension of the image:
            xs = bnds[1]-bnds[0]
            ys = bnds[2]-bnds[3]
            
            if xs<ys:
                self.InitialParallelScale = ys/2.0
            else:
                self.InitialParallelScale = xs/2.0
            
            # Somehow, when the axes are present, they screw up the ResetZoom
            # function because they are taken into account when computing the
            # bounds of all actors. We need to switch them off and on after
            # the call to ResetZoom().
            self.VerticalLineActor.SetVisibility(0)
            self.HorizontalLineActor.SetVisibility(0)
            
            self.ResetZoom()
            
            self.VerticalLineActor.SetVisibility(1)
            self.HorizontalLineActor.SetVisibility(1)
            
            self.FirstRender = 0
    
    def InitInteractorStyle(self, p_style):
        interactor = vtkInteractorStyleImage2D()
        interactor.SetView(self)
        cbk = vtkViewImage2DCommand()
        cbk.SetView(self)
        interactor.AddObserver("KeyPressEvent", 
                               lambda obj, event: cbk.Execute(obj, "KeyPressEvent"))
        interactor.AddObserver("WindowLevelEvent", 
                               lambda obj, event: cbk.Execute(obj, "WindowLevelEvent"))
        interactor.AddObserver("StartWindowLevelEvent", 
                               lambda obj, event: cbk.Execute(obj, "StartWindowLevelEvent"))
        interactor.AddObserver("ResetWindowLevelEvent", 
                               lambda obj, event: cbk.Execute(obj, "ResetWindowLevelEvent"))
        interactor.AddObserver("EndWindowLevelEvent", 
                               lambda obj, event: cbk.Execute(obj, "EndWindowLevelEvent"))
        interactor.AddObserver("PickEvent", 
                               lambda obj, event: cbk.Execute(obj, "PickEvent"))
        interactor.AddObserver("StartPickEvent", 
                               lambda obj, event: cbk.Execute(obj, "StartPickEvent"))
        interactor.AddObserver("EndPickEvent", 
                               lambda obj, event: cbk.Execute(obj, "EndPickEvent"))
        interactor.AddObserver("ResetZoomEvent", 
                               lambda obj, event: cbk.Execute(obj, "ResetZoomEvent"))
        interactor.AddObserver("ResetPositionEvent", 
                               lambda obj, event: cbk.Execute(obj, "ResetPositionEvent"))
        interactor.AddObserver("StartZSliceMoveEvent", 
                               lambda obj, event: cbk.Execute(obj, "StartZSliceMoveEvent"))
        interactor.AddObserver("ZSliceMoveEvent", 
                               lambda obj, event: cbk.Execute(obj, "ZSliceMoveEvent"))
        interactor.AddObserver("EndZSliceMoveEvent", 
                               lambda obj, event: cbk.Execute(obj, "EndZSliceMoveEvent"))
        interactor.AddObserver("StartMeasureEvent", 
                               lambda obj, event: cbk.Execute(obj, "StartMeasureEvent"))
        interactor.AddObserver("MeasureEvent", 
                               lambda obj, event: cbk.Execute(obj, "MeasureEvent"))
        interactor.AddObserver("EndMeasureEvent", 
                               lambda obj, event: cbk.Execute(obj, "EndMeasureEvent"))
        interactor.AddObserver("FullPageEvent", 
                               lambda obj, event: cbk.Execute(obj, "FullPageEvent"))
        interactor.AddObserver("ZoomEvent", 
                               lambda obj, event: cbk.Execute(obj, "ZoomEvent"))
        self.SetInteractorStyle(interactor)
        
    def SetShowDirections(self, p_showDirections):
        self.ShowDirections = p_showDirections
        
    def SetShowCurrentPoint(self, p_showCurrentPoint):
        self.ShowCurrentPoint = p_showCurrentPoint
        if not self.ShowCurrentPoint:
            self.HorizontalLineSource.SetPoint1(0, 0, 0.001)
            self.HorizontalLineSource.SetPoint2(0, 0, 0.001)
            self.VerticalLineSource.SetPoint1(0, 0, 0.001)
            self.VerticalLineSource.SetPoint2(0, 0, 0.001)
    
    def SetShowSliceNumber(self, p_showSliceNumber):
        self.ShowSliceNumber = p_showSliceNumber
        if not self.ShowSliceNumber:
            self.SetUpRightAnnotation("")
    
    def GetWholeZMin(self):
        return 0
    
    def GetWholeZMax(self):
        if not self.Image:
            return 0
        ext = self.Image.GetWholeExtent()
        
        assert self.Orientation < vtkViewImage.NB_DIRECTION_IDS, "plan's index should be a unsigned integer less than %s" %(vtkViewImage.NB_DIRECTION_IDS)
        axis = self.GetOrthogonalAxis(self.Orientation)
        return ext[2*axis+1]
    
    def GetZSlice(self):
        return self.GetSlice(self.Orientation)
    
    def SetZSlice(self, p_zslice):
        self.SetSlice(self.Orientation, p_zslice)
    
    def UpdatePosition(self):
        if not self.Image:
            return
        x = 0.0
        y = 0.0
        max_x = 0.0
        max_y = 0.0
        min_x = 0.0
        min_y = 0.0
        pos = self.GetCurrentPoint()
        
        spacing = self.Image.GetSpacing()
        origin = self.Image.GetOrigin()
        imBounds = self.Image.GetBounds()
        
        # check if pos lies inside image bounds
        if (pos[0]<imBounds[0] or pos[0]> imBounds[1] or
            pos[1]<imBounds[2] or pos[1]> imBounds[3] or
            pos[2]<imBounds[4] or pos[2]> imBounds[5]):
            # we are outside image bounds
            return
            
        pos[0] = float(vtkrint((pos[0]-origin[0])/spacing[0]))*spacing[0]+origin[0]
        pos[1] = float(vtkrint((pos[1]-origin[1])/spacing[1]))*spacing[1]+origin[1]
        pos[2] = float(vtkrint((pos[2]-origin[2])/spacing[2]))*spacing[2]+origin[2]
    
        if self.Orientation == vtkViewImage.SAGITTAL_ID:
            self.ImageReslice.SetResliceAxesOrigin(pos[0], 0, 0)
            x = pos[1]
            y = pos[2]
            max_x = self.GetWholeMaxPosition(1)
            max_y = self.GetWholeMaxPosition(2)
            min_x = self.GetWholeMinPosition(1)
            min_y = self.GetWholeMinPosition(2)
        elif self.Orientation == vtkViewImage.CORONAL_ID:
            self.ImageReslice.SetResliceAxesOrigin(0, pos[1], 0)
            if self.Conventions == self.RADIOLOGIC:
                x = float(pos[0])
                max_x = self.GetWholeMaxPosition(0)
                min_x = self.GetWholeMinPosition(0)
            else:
                x = float(pos[0])*-1.0
                max_x = self.GetWholeMaxPosition(0)*-1.0
                min_x = self.GetWholeMinPosition(0)*-1.0
            y = float(pos[2])
            max_y = self.GetWholeMaxPosition(2)
            min_y = self.GetWholeMinPosition(2)
        elif self.Orientation == vtkViewImage.AXIAL_ID:
            self.ImageReslice.SetResliceAxesOrigin(0,0,pos[2])
            if self.Conventions == self.RADIOLOGIC:
                x = float(pos[0])
                max_x = self.GetWholeMaxPosition(0)
                min_x = self.GetWholeMinPosition(0)
            else:
                x = float(pos[0])*-1.0
                max_x = self.GetWholeMaxPosition(0)*-1.0
                min_x = self.GetWholeMinPosition(0)*-1.0
            y = float(pos[1])*-1.0
            max_y = self.GetWholeMaxPosition(1)*-1.0
            min_y = self.GetWholeMinPosition(1)*-1.0
        
        if (self.ShowCurrentPoint):
            self.HorizontalLineSource.SetPoint1(min_x, y, 0.001)
            self.HorizontalLineSource.SetPoint2(max_x, y, 0.001)  
            self.VerticalLineSource.SetPoint1(x, min_y, 0.001) 
            self.VerticalLineSource.SetPoint2(x, max_y, 0.001)
        
        self.ImageReslice.Update() # needed to update input Extent
        
        if (self.ShowAnnotations):
            # Update annotations
            if (self.Image and self.ShowSliceNumber):
                imCoor = self.GetCurrentVoxelCoordinates()
                dims = self.Image.GetDimensions()
                annotation = "Slice: "
                if self.Orientation == vtkViewImage.SAGITTAL_ID:
                    annotation += str(imCoor[0]) +" / " + str(dims[0]-1)+"\n"
                elif self.Orientation == vtkViewImage.CORONAL_ID:
                    annotation += str(imCoor[1]) +" / " + str(dims[1]-1)+"\n"
                elif self.Orientation == vtkViewImage.AXIAL_ID:
                    annotation += str(imCoor[2]) +" / " + str(dims[2]-1)+"\n"
            annotation += "Value: " + str(self.GetCurrentPointDoubleValue())+"\n"
            annotation += "<window>\n<level>"
            self.SetUpRightAnnotation(annotation)
        self.SetDownLeftAnnotation(self.GetAboutData())
        direction = self.GetOrthogonalAxis(self.Orientation)
        if direction == vtkViewImage.X_ID:
            self.DataSetCutPlane.SetOrigin(pos[0], 0, 0)
            self.DataSetCutPlane.SetNormal(1, 0, 0)
            self.DataSetCutBox.SetBounds( self.DataSetCutPlane.GetOrigin()[0],
                                          self.DataSetCutPlane.GetOrigin()[1]+self.BoxThickness, 
                                          self.GetWholeMinPosition(1), 
                                          self.GetWholeMaxPosition(1), 
                                          self.GetWholeMinPosition(2),
                                          self.GetWholeMaxPosition(2))
        elif direction == vtkViewImage.Y_ID:
            self.DataSetCutPlane.SetOrigin(0, pos[0], 0)
            self.DataSetCutPlane.SetNormal(0, 1, 0)
            self.DataSetCutBox.SetBounds( self.GetWholeMinPosition(0),
                                          self.GetWholeMaxPosition(0), 
                                          self.DataSetCutPlane.GetOrigin()[0], 
                                          self.DataSetCutPlane.GetOrigin()[1]+self.BoxThickness, 
                                          self.GetWholeMinPosition(2),
                                          self.GetWholeMaxPosition(2))
        elif direction == vtkViewImage.Z_ID:
            self.DataSetCutPlane.SetOrigin(0, 0, pos[0])
            self.DataSetCutPlane.SetNormal(0, 0, 1)
            self.DataSetCutBox.SetBounds( self.GetWholeMinPosition(0),
                                          self.GetWholeMaxPosition(0),
                                          self.GetWholeMinPosition(1), 
                                          self.GetWholeMaxPosition(1), 
                                          self.DataSetCutPlane.GetOrigin()[0], 
                                          self.DataSetCutPlane.GetOrigin()[1]+self.BoxThickness
                                          )
          
        if len(self.DataSetList):
            self.ResetAndRestablishZoomAndCamera()
            #=========================================================================
            # We need to correct for the origin of the actor. Indeed, the ImageActor
            # has always position 0 in Z in axial view, in X in sagittal view and
            # in Y in coronal view. The projected dataset have an origin that depends
            # on the required slice and can be negative. In that case, the projected
            # data are behind the image actor and thus not visible. Here, we correct
            # this by translating the actor so that it becomes visible.
            #=========================================================================
            for actor in self.DataSetActorList:
                Pos = actor.GetPosition()
                if direction == vtkViewImage.X_ID:
                    Pos[0] = -1.0*pos[0] + 1.0
                elif direction == vtkViewImage.Y_ID:
                    Pos[1] = -1.0*pos[1] + 1.0
                elif direction == vtkViewImage.Z_ID:
                    Pos[2] = -1.0*pos[2] + 1.0
                actor.SetPosition(Pos)
                
    def SetWindow(self, w):           
        if w<0.0:
            w = 0.0
        shiftScaleWindow = self.Shift + w*self.Scale
        vtkViewImage.SetWindow(self, shiftScaleWindow)
        v_min = self.Level - 0.5*self.Window
        v_max = self.Level + 0.5+self.Window
        
        if self.LookupTable:
            self.LookupTable.SetRange((v_min-0.5*self.Shift)/self.Scale,
                                      (v_max-1.5*self.Shift)/self.Scale)
            self.WindowLevel.GetLookupTable().SetRange(v_min, v_max)
    
    def SetLevel(self, l):
        shiftScaleLevel = self.Shift + l*self.Scale
        vtkViewImage.SetLevel(self, shiftScaleLevel)
        self.WindowLevelForCorner.SetLevel(shiftScaleLevel)
        v_min = self.Level - 0.5*self.Window
        v_max = self.Level + 0.5+self.Window
        if self.LookupTable:
            self.LookupTable.SetRange((v_min-0.5*self.Shift)/self.Scale,
                                      (v_max-1.5*self.Shift)/self.Scale)
            self.WindowLevel.GetLookupTable().SetRange(v_min, v_max)
    
    def GetColorWindow(self):
        return self.Window
    
    def GetColorLevel(self):
        return self.Level
    
    def SetTransform(self, p_transform):
        self.ImageReslice.SetResliceTransform(p_transform)
        
    def SetImage(self, image):
        if not image:
            return
        
        self.RegisterImage(image)
        
        # check if there is a mask image. If yes, then we check
        # if the new image size and spacing agrees with the mask image.
        # If not, we remove the mask image
        if self.MaskImage:
            dims = image.GetDimensions()
            spacing = image.GetSpacing()
            maskDims = self.MaskImage.GetDimensions()
            maskSpacing = self.MaskImage.GetSpacing()
           
            if ( dims <> maskDims or spacing <> maskSpacing):
                self.RemoveMaskImage()
        
        # should check also the overlapping image
        if (image.GetScalarType() == vtk.VTK_UNSIGNED_CHAR and 
            ( image.GetNumberOfScalarComponents()==3 or 
              image.GetNumberOfScalarComponents()==4)):
            self.AuxInput = image
        else:
            self.AuxInput = self.WindowLevel.GetOutput()
            self.WindowLevel.SetInput(image)
            range = image.GetScalarRange()
            if self.WindowLevel.GetLookupTable():
                self.WindowLevel.GetLookupTable().SetRange(range)
        if self.OverlappingImage:
            self.Blender.SetInput(0, self.AuxInput)
        else:
            if self.MaskImage:
                #self.MaskFilter.SetImageInput(self.AuxInput)
                pass
            else:
                self.ImageReslice.SetInput(self.AuxInput)
                self.ResliceInput = self.AuxInput
        
        self.ImageActor.SetInput(self.ImageReslice.GetOutput())
       
        self.AddActor(self.HorizontalLineActor)
        
        self.AddActor(self.VerticalLineActor)
        
        self.AddActor(self.ImageActor)
        
        # save the camera focal and position, and zoom, before calling Update (in SetOrientation())
     
        pos,focal  = self.GetCameraFocalAndPosition()
        zoom = self.Zoom
        self.SetOrientation(self.Orientation)
        self.SetWindow(self.Window)
        self.SetLevel(self.Level)
        
        if not self.FirstImage:
            self.Zoom = zoom
            self.SetCameraFocalAndPosition(focal, pos)
        
        self.FirstImage = 0
    
    def SetLookupTable(self, lut):
        if not lut:
            return
        vtkViewImage.SetLookupTable(self, lut)
        v_min = self.Level - 0.5*self.Window
        v_max = self.Level + 0.5+self.Window
        
        #==========================================================================
        #   In the case of a shift/scale, one must set the lut range to values
        # without this shift/scale, because the object can be shared by different
        # views.
        #==========================================================================
        lut.SetRange( (v_min-0.5*self.Shift)/self.Scale,
                      (v_max-1.5*self.Shift)/self.Scale)
        
        #==========================================================================
        #     Due to the same problem as above (shift/scale), one must copy the lut
        # so that it does not change values of the shared object.
        #==========================================================================
        realLut = vtk.vtkLookupTable.SafeDownCast(lut)
        if not realLut:
            raise RuntimeError, "Error: Cannot cast vtkScalarsToColors to vtkLookupTable."
        newLut = vtk.vtkLookupTable()
        newLut.DeepCopy(realLut)
        newLut.SetRange(v_min, v_max)
        self.WindowLevel.SetLookupTable(newLut)
        del newLut
        
    def SetOrientation(self, p_orientation):
        if p_orientation >vtkViewImage.NB_PLAN_IDS-1:
            return
        self.Orientation = p_orientation
        
        if not self.Image:
            return
        self.SetupAnnotations()
        direction = self.GetOrthogonalAxis(self.Orientation)
        if direction == vtkViewImage.X_ID:
            self.DataSetCutPlane.SetNormal(1,0,0)
        elif direction == vtkViewImage.Y_ID:
            self.DataSetCutPlane.SetNormal(0,1,0)
        elif direction == vtkViewImage.Z_ID:
            self.DataSetCutPlane.SetNormal(0,0,1)
        else:
            pass
        self.ImageReslice.Modified()
        self.Update()
        
    def SetInterpolationMode(self,i):
        self.ImageActor.SetInterpolate(i)
    
    def GetInterpolationMode(self):
        return self.ImageActor.GetInterpolate()
    
    def SetMaskImage(self, mask, lut):
        if (not self.Image or not mask or not lut):
            return
        
        self.SetMaskImage(self, mask, lut)
        # check if the mask dimensions match the image dimensions
        dim1 = [0.0]*3
        dim2 = [0.0]*3
        self.Image.GetDimensions(dim1)
        mask.GetDimensions(dim2)
        if dim1<>dim2:
            raise RuntimeError, "Dimensions of the mask image do not match"
        
        # check if the scalar range match the number of entries in the LUT
        range = mask.GetScalarRange(range)
        numLut = lut.GetNumberOfTableValues()
        if numLut < int(range[1])+1:
            raise RuntimeError, "The number of LUT entries is less than the range of the mask."
        
        if self.OverlappingImage:
            #self.MaskFilter.SetImageInput(self.Blender.GetOutput())
            pass
        else:
            #self.MaskFilter.SetImageInput(self.AuxInput)
            pass
        #self.MaskFilter.SetMaskInput(mask)
        #self.MaskFilter.SetLookupTable(lut)
        # ids = vtk.vtkImageDataStreamer()
        # ids.SetInput(self.MaskFilter.GetOutput())
        # ids.SetNumberOfStreamDivisions(40)
        # ids.UpdateWholeExtent()
        #self.MaskFilter.Update()
        #self.ImageReslice.SetInputConnection(self.MaskFilter.GetOutputPort())
        #self.ResliceInput = self.MaskFilter.GetOutput()
        # def ids
    
    def RemoveMaskImage(self):
        if self.OverlappingImage:
            self.ImageReslice.SetInputConnection(self.Blender.GetOutputPort())
            self.ResliceInput = self.Blender.GetOutput()
        else:
            self.ImageReslice.SetInput(self.AuxInput)
            self.ResliceInput = self.AuxInput
        vtkViewImage.SetMaskImage(self, 0, 0)
    
    def SetOverlappingImage(self, image):
        if not self.Image or not image:
            return
        self.OverlappingImage = image
        self.Blender.RemoveAllInputs()
        self.Blender.AddInput(self.AuxInput)
        self.Blender.AddInput(image)
        
        if self.MaskImage:
            #self.MaskFilter.SetInputConnection(self.Blender.GetOutputPort())
            pass
        else:
            self.ImageReslice.SetInputConnection(self.Blender.GetOutputPort())
            self.ResliceInput = self.Blender.GetOutput()
    
    def RemoveOverlappingImage(self):
        if self.MaskImage:
            #self.MaskFilter.SetInput(self.AuxInput)
            pass
        else:
            self.ImageReslice.SetInput(self.AuxInput)
            self.ResliceInput = self.AuxInput
        self.OverlappingImage = None
    
    def AddDataSet(self, dataset, property):
        doit = True
        if not dataset:
            doit = False
        
        if self.HasDataSet(dataset):
            doit = False
        
        imagedata = vtk.vtkImageData.SafeDownCast(dataset)
        if imagedata:
            self.SetImage(imagedata)
        else:
            if not self.Image:
                doit=False
        
            if doit:
                matrix = vtk.vtkMatrix4x4()
                for i in range(3):
                    for j in range(3):
                        matrix.SetElement(i,j,self.ImageReslice.GetResliceAxes().GetElement(j,i))
                    matrix.SetElement(i, 3, 0)
                matrix.SetElement(3, 3, 1)
                
                cutter = vtk.vtkCutter()
                cutter.SetCutFunction(self.DataSetCutPlane)
                
                # Very strangely in some cases (ex : landmarks)
                # the cutter increments the RefCount of the input dataset by 2
                # making some memory leek...
                # I could not manage to know what is wrong here
                cutter.SetInput(dataset)
                cutter.Update()
                
                if not cutter.GetOutput():
                    print "Unable to cut this dataset..."
                    del matrix
                    del cutter
                    return None
                
                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInput(cutter.GetOutput())
                
                actor = vtk.vtkActor()
                actor.SetUseMatrix(matrix)
                actor.SetMapper(mapper)
                if property:
                    actor.SetProperty(property)
                actor.PickableOff()  
                self.AddActor(actor)
                self.DataSetList.append(dataset)
                self.DataSetActorList.append(actor)
                
                self.ResetAndRestablishZoomAndCamera()
                del actor
                del mapper
                del matrix
                del cutter
        return self.GetDataSetActor(dataset)
    
    def SyncAddPolyData(self, polydata, property, thickness):
        if self.IsLocked():
            return None
        
        actor = self.AddPolyData(polydata, property, thickness)
        
        self.Lock()
        for view in self.Children:
            view = vtkViewImage2D.SaftDownCast(view)
            if view:
                view.SyncAddPolyData(polydata, property, thickness)
        
        self.UnLock()
        return actor
    
    def AddPolyData(self, polydata, property, thickness):
        doit = True
        if (not polydata or self.HasDataSet(polydata) or not self.Image):
            doit = False
        
        if doit:
            if thickness:
                self.BoxThickness = thickness
            
            clipper = vtk.vtkClipDataSet()
            clipper.GenerateClippedOutputOff()
            clipper.InsideOutOn()
            clipper.SetInput(polydata)
            
            direction = self.GetOrthogonalAxis(self.Orientation)
            if direction == vtkViewImage.X_ID:
           
                self.DataSetCutBox.SetBounds( self.DataSetCutPlane.GetOrigin()[0]-0.5*self.BoxThickness,
                                          self.DataSetCutPlane.GetOrigin()[1]+0.5*self.BoxThickness, 
                                          self.GetWholeMinPosition(1), 
                                          self.GetWholeMaxPosition(1), 
                                          self.GetWholeMinPosition(2),
                                          self.GetWholeMaxPosition(2))
            elif direction == vtkViewImage.Y_ID:
               
                self.DataSetCutBox.SetBounds( self.GetWholeMinPosition(0),
                                              self.GetWholeMaxPosition(0), 
                                              self.DataSetCutPlane.GetOrigin()[0]-0.5*self.BoxThickness, 
                                              self.DataSetCutPlane.GetOrigin()[1]+0.5*self.BoxThickness, 
                                              self.GetWholeMinPosition(2),
                                              self.GetWholeMaxPosition(2))
            elif direction == vtkViewImage.Z_ID:
               
                self.DataSetCutBox.SetBounds( self.GetWholeMinPosition(0),
                                              self.GetWholeMaxPosition(0),
                                              self.GetWholeMinPosition(1), 
                                              self.GetWholeMaxPosition(1), 
                                              self.DataSetCutPlane.GetOrigin()[0]-0.5*self.BoxThickness, 
                                              self.DataSetCutPlane.GetOrigin()[1]+0.5*self.BoxThickness
                                              )
            clipper.SetClipFunction(self.DataSetCutBox)
            clipper.Update()
            matrix = vtk.vtkMatrix4x4()
            for i in range(3):
                for j in range(3):
                    matrix.SetElement(i,j,self.ImageReslice.GetResliceAxes().GetElement(j,i))
               
            matrix.SetElement(3, 3, 1)
            
            mapper= vtk.vtkDataSetMapper()
            mapper.SetInput(clipper.GetOutput())
            
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.SetUseMatrix(matrix)
            if property:
                actor.SetProperty(property)
            
            self.AddActor(actor)
            self.DataSetList.append(polydata)
            self.DataSetActorList.append(actor)
            
            self.ResetAndRestablishZoomAndCamera()
            
            del actor
            del mapper
            del matrix
            del clipper
        return self.GetDataSetActor(polydata)
    
    def ResetZoom(self): 
        vtkViewImage.ResetZoom(self)
        self.SetZoom(1.0)
    
    def Show2DAxis(self, show):
        self.HorizontalLineActor.SetVisibility(show)
        self.VerticalLineActor.SetVisibility(show)
    
    def SetZoom(self, factor):
        if self.Renderer == None:
            return
        vtkViewImage.SetZoom(self, factor)
        
        camera = self.Renderer.GetActiveCamera()
        camera.SetParallelScale(self.InitialParallelScale / self.Zoom );
        
        if self.RenderWindowInteractor.GetLightFollowCamera():
            self.Renderer.UpdateLightsGeometryToFollowCamera()
    
    def SetConventionsToRadiological(self):
        self.Conventions = self.RADIOLOGIC
        self.SetupAnnotations()
        self.UpdatePosition()
        self.ResetAndRestablishZoomAndCamera()
    
    def SetConventionsToNeurological(self):
        self.Conventions = self.NEUROLOGIC
        self.SetupAnnotations()
        self.UpdatePosition()
        self.ResetAndRestablishZoomAndCamera()
    
    def SetupAnnotations(self): 
        if self.Image == None:
            return
        dims = self.Image.GetDimensions()
        spacing = self.Image.GetSpacing()
        
        annotations = "Image Size: "
        if self.Orientation == vtkViewImage.AXIAL_ID:
            if self.Conventions == self.RADIOLOGIC:
                self.ImageReslice.SetResliceAxesDirectionCosines(1, 0, 0,
                                                             0, -1, 0,
                                                             0, 0, 1)
            else:
                self.ImageReslice.SetResliceAxesDirectionCosines(-1, 0, 0,
                                                             0, -1, 0,
                                                             0, 0, 1)
            annotations += str(dims[0]) + " x " + str(dims[1]) + "\n"
            annotations += "Voxel Size: " + str(spacing[0]) + " x " + str(spacing[1]) + " mm"
            if self.ShowDirections:
                # self.SetNorthAnnotation("A")
                # self.SetSouthAnnotation("P")
                if self.Conventions == self.RADIOLOGIC:
                    # self.SetEastAnnotation("L")
                    # self.SetWestAnnotation("R")
                    pass
                else:
                    # self.SetEastAnnotation("R")
                    # self.SetWestAnnotation("L")
                    pass
                pass
            self.HorizontalLineActor.GetProperty().SetColor (0.0,1.0,0.0)
            self.VerticalLineActor.GetProperty().SetColor (0.0,0.0,1.0)
        elif self.Orientation == vtkViewImage.SAGITTAL_ID:
            self.ImageReslice.SetResliceAxesDirectionCosines(0, 1, 0,
                                                             0, 0, 1,
                                                             1, 0, 0)
            annotations += str(dims[1]) + " x " + str(dims[2]) + "\n"
            annotations += "Voxel Size: " + str(spacing[1]) + " x " + str(spacing[2]) + " mm"
            self.HorizontalLineActor.GetProperty().SetColor (1.0,0.0,0.0)
            self.VerticalLineActor.GetProperty().SetColor (0.0,1.0,0.0)
            if self.ShowDirections:
                self.SetNorthAnnotation("S")    
                self.SetSouthAnnotation("I")   
                self.SetEastAnnotation ("P")  
                self.SetWestAnnotation("A")
                pass
        elif self.Orientation == vtkViewImage.CORONAL_ID:
            if self.Conventions == self.RADIOLOGIC:
                self.ImageReslice.SetResliceAxesDirectionCosines(1, 0, 0,
                                                             0, 0, 1,
                                                             0, 1, 0)
            else:
                self.ImageReslice.SetResliceAxesDirectionCosines(-1, 0, 0,
                                                             0, 0, 1,
                                                             0, 1, 0)
            annotations += str(dims[0]) + " x " + str(dims[2]) + "\n"
            annotations += "Voxel Size: " + str(spacing[0]) + " x " + str(spacing[2]) + " mm"
            if self.ShowDirections:
                # self.SetNorthAnnotation("S")
                # self.SetSouthAnnotation("I")
                if self.Conventions == self.RADIOLOGIC:
                    # self.SetEastAnnotation("L")
                    # self.SetWestAnnotation("R")
                    pass
                else:
                    # self.SetEastAnnotation("R")
                    # self.SetWestAnnotation("L")
                    pass
                pass
            self.HorizontalLineActor.GetProperty().SetColor (1.0,0.0,0.0)
            self.VerticalLineActor.GetProperty().SetColor (0.0,0.0,1.0) 
            self.SetSizeData(annotations)
            if self.ShowAnnotations:
                self.SetUpLeftAnnotation(self.GetSizeData())
            self.SetDownLeftAnnotation(self.GetSizeData())
               
    def ResetAndRestablishZoomAndCamera(self):
        if not self.Renderer:
            return
        zoom = self.Zoom
        camera = self.Renderer.GetActiveCamera()
        c_position = camera.GetPosition()
        focal = camera.GetFocalPoint()
        self.ResetZoom()
        
        focal2 = 0.0
        camera.GetFocalPoint(focal2)
        pos2 = camera.GetPosition()
        
        camera.SetFocalPoint(focal[0], focal[1], focal2[2])
        camera.SetPosition(c_position[0], c_position[1], pos2[2])
        
        self.SetZoom(zoom/self.Zoom)
        
    def SetCameraFocalAndPosition(self, focal, pos):
        if not self.Renderer:
            return
        camera = self.Renderer.GetActiveCamera()
        c_position = camera.GetPosition()
        c_focal = camera.GetFocalPoint()
        
        camera.SetFocalPoint(focal[0], focal[1], c_focal[2])
        camera.SetPosition(pos[0], pos[1], c_position[2])
     
    def GetCameraFocalAndPosition(self):
        if not self.Renderer:
            return
        camera = self.Renderer.GetActiveCamera()
        return camera.GetPosition(), camera.GetFocalPoint()
    
    
    def SyncSetCameraFocalAndPosition(self, focal, pos):
        if self.IsLocked():
            return
        
        if self.LinkCameraFocalAndPosition:
            self.SetCameraFocalAndPosition(focal, pos)
        self.Lock()
        for view in self.Children:
            view = vtkViewImage2D.SafeDownCast(view)
            if view:
                view.SyncSetCameraFocalAndPosition(focal, pos)
                if not view.RendererWindow.GetNeverRendered():
                    view.Render()
        
        self.UnLock()
    
    def SetLeftButtonInteractionStyle(self, style):
        self.LeftButtonInteractionStyle = style
        
    def SetMiddleButtonInteractionStyle(self, style):
        self.MiddleButtonInteractionStyle = style 
    
    def SetWheelInteractionStyle(self, style):
        self.WheelInteractionStyle = style
    
    def SetRightButtonInteractionStyle(self, style):
        self.RightButtonInteractionStyle = style
    
    
     
        
if __name__ == "__main__":
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
    view1 = vtkViewImage2D()
    view2 = vtkViewImage2D()
    view3 = vtkViewImage2D()
    
    iren1 = vtk.vtkRenderWindowInteractor()
    iren2 = vtk.vtkRenderWindowInteractor()
    iren3 = vtk.vtkRenderWindowInteractor()
    
    rwin1 = vtk.vtkRenderWindow()
    rwin2 = vtk.vtkRenderWindow()
    rwin3 = vtk.vtkRenderWindow()
    
    renderer1 = vtk.vtkRenderer()
    renderer2 = vtk.vtkRenderer()
    renderer3 = vtk.vtkRenderer()
    
    iren1.SetRenderWindow(rwin1)
    iren2.SetRenderWindow(rwin2)
    iren3.SetRenderWindow(rwin3)
    
    rwin1.AddRenderer(renderer1)
    rwin2.AddRenderer(renderer2)
    rwin3.AddRenderer(renderer3)
    
    view1.SetRenderWindow(rwin1)
    view2.SetRenderWindow(rwin2)
    view3.SetRenderWindow(rwin3)
    
    view1.SetRenderer(renderer1)
    view2.SetRenderer(renderer2)
    view3.SetRenderer(renderer3)
    
    # One can also associate to each button (left, middle, right and even wheel)
    # a specific interaction like this:
    
    view1.SetLeftButtonInteractionStyle(vtkViewImage2D.ZOOM_INTERACTION)
    view1.SetMiddleButtonInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view1.SetWheelInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view1.SetRightButtonInteractionStyle(vtkViewImage2D.WINDOW_LEVEL_INTERACTION)
    
    view2.SetLeftButtonInteractionStyle(vtkViewImage2D.ZOOM_INTERACTION)
    view2.SetMiddleButtonInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view2.SetWheelInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view2.SetRightButtonInteractionStyle(vtkViewImage2D.WINDOW_LEVEL_INTERACTION)
    
    view3.SetLeftButtonInteractionStyle(vtkViewImage2D.ZOOM_INTERACTION)
    view3.SetMiddleButtonInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view3.SetWheelInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view3.SetRightButtonInteractionStyle(vtkViewImage2D.WINDOW_LEVEL_INTERACTION)
    
    view1.SetLinkZoom(True)  
    view2.SetLinkZoom(True)
    view3.SetLinkZoom(True)
    
    view1.SetOrientation(vtkViewImage2D.AXIAL_ID)
    view2.SetOrientation(vtkViewImage2D.CORONAL_ID)
    view3.SetOrientation(vtkViewImage2D.SAGITTAL_ID)
    
    view1.SetBackgroundColor(0.0, 0.0, 0.0)
    view2.SetBackgroundColor(0.0, 0.0, 0.0)
    view3.SetBackgroundColor(0.0, 0.0, 0.0)
    
    view1.SetAboutData("Powered by summit & jolly")
    view2.SetAboutData("Powered by summit & jolly")
    view3.SetAboutData("Powered by summit & jolly")
    
    # Link the views together for synchronization.
    view1.AddChild(view2)
    view2.AddChild(view3)
    view3.AddChild(view1)
    
    reader = ImageSeriesReader(sys.argv[1])
    v16 = vtk.vtkVolume16Reader()
    v16.SetDataDimensions(64, 64)
    v16.SetDataByteOrderToLittleEndian()
    v16.SetFilePrefix(os.path.join(vtkGetDataRoot(),
                                   "Data", "headsq", "quarter"))
    v16.SetImageRange(1, 93)
    v16.SetDataSpacing(3.2, 3.2, 1.5)
    v16.Update()
    
    image = v16.GetOutput()
    
    WindowLevel = vtk.vtkImageMapToColors()
    WindowLevel.SetInput(image)
    WindowLevel.Update()
    print WindowLevel.GetOutput()
    view1.SetImage(image)
    view2.SetImage(image)
    view3.SetImage(image)
    
    #  Reset the window/level and the current position.
    view1.SyncResetCurrentPoint()
    view1.SyncResetWindowLevel()
    
    rwin1.Render()
    rwin2.Render()
    rwin3.Render()
    
    iren1.Start()
    
    view1.Detach()
    view2.Detach()
    view3.Detach()
    