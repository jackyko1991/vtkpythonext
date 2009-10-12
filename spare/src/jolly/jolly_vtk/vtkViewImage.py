# -*- coding:utf-8 -*-
"""
Created on 2009-10-6

@author: summit
@copyright: summit,jolly
@contact: choicice.summit@gamil.com
"""

import vtk
from vtkSynchronizedView import *

class vtkViewImage(vtkSynchronizedView):
    # Indices use in Vtk referentials corresponding to the standard x, y 
    # and z unitary vectors.
    X_ID = 0
    Y_ID = 1
    Z_ID = 2
    NB_DIRECTION_IDS = 3 # The number of DirectionIds
    
    # Ids of the 2D plan displayed in the view. Each 2D plan is defined 
    # with regard to one of the 3 directions (x,y,z).
    SAGITTAL_ID = 0
    CORONAL_ID = 1
    AXIAL_ID = 2
    NB_PLAN_IDS = 3 # The number of PlanIds
    
    # vtkCommand::UserEvent = 1000
#    ViewImagePositionChangeEvent = 1000+1
#    ViewImageWindowLevelChangeEvent = 1000+2
#    ViewImageZoomChangeEvent = 1000+3

    FullRange = 0
    UserDefinedPercentage = 1
    
    def __init__(self):
        vtkSynchronizedView.__init__(self)
        self.Image = None
        self.MaskImage = None
        self.MaskLUT = None
        self.Transform = None
        self.LookupTable = None
        self.LinkWindowLevel = True
        self.LinkPosition = True
        self.LinkZoom = False
        self.Shift = 0.0
        self.Scale = 1.0
        self.Level = 128.0
        self.Window = 255.0
        self.Zoom = 1.0
        
        self.DataSetList = []   #vtkDataSet
        self.DataSetActorList = []
        
        self.ScalarBar = vtk.vtkScalarBarActor()
        self.ScalarBar.GetLabelTextProperty().SetColor(1.0, 1.0, 1.0)
        self.ScalarBar.GetTitleTextProperty().SetColor(1.0, 1.0, 1.0)
        self.ScalarBar.GetLabelTextProperty().BoldOff()
        self.ScalarBar.GetLabelTextProperty().ShadowOff()
        self.ScalarBar.GetLabelTextProperty().ItalicOff()
        self.ScalarBar.SetNumberOfLabels(3)
        self.ScalarBar.GetLabelTextProperty().SetFontSize(1)
        self.ScalarBar.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
        self.ScalarBar.SetWidth(0.1)
        self.ScalarBar.SetHeight(0.5)
        self.ScalarBar.VisibilityOff()
        
        self.CurrentPoint = [0.0] * 3
        self.SetAboutData("")
        # Increase polygon offsets to support some OpenGL drivers
        vtk.vtkMapper.SetResolveCoincidentTopologyToPolygonOffset()
        vtk.vtkMapper.SetResolveCoincidentTopologyPolygonOffsetParameters(10, 10)
    
    #===========================================================================
    # General Get Methods about the image
    # Get the begining position of the first pixel in the given axis. Note : the
    # position (0,0,0) is the center of the first pixel (0,0,0) so the return 
    # value can be
    # negative, depending of the origin of the image.
    #===========================================================================
    def GetWholeMinPosition(self, p_axis):
        pass
    
    #===========================================================================
    # Get the end position of the last pixel in the given axis.
    #===========================================================================
    def GetWholeMaxPosition(self, p_axis):
        pass
    
    #==========================================================================
    # Get the id of the axis orthogonal to the given plan
    # (x for sagittal, y for coronal and z for axial).
    #==========================================================================
    def GetOrthogonalAxis(self, p_plan):
        pass
    
    #===========================================================================
    # Return the voxel coordinates of the point pos.
    #===========================================================================
    def GetVoxelCoordinates(self, pos, p_coordinates):
        pass
    
    #==========================================================================
    # Fill the p_coordinates parameter with the coordinates of the voxel
    # corresponding to the current point.
    #==========================================================================
    def GetCurrentVoxelCoordinates(self, p_coordinates):
        pass
    
    #===========================================================================
    # Get the image value of the current point in double.
    #===========================================================================
    def GetCurrentPointDoubleValue(self):
        pass
    
    #==========================================================================
    # Get the current image.
    #==========================================================================
    def GetImage(self):
        return self.Image
    
    #===========================================================================
    # Set the current image.
    #===========================================================================
     
    def SetImage(self, image):
        assert 1, "You should not use this function here\nPlease use \
                    vtkViewImage2D or vtkViewImage3D classes instead"
    
    #==========================================================================
    # Ensure that the displayed point is up to date. Should be overriden by subclasses.
    #==========================================================================
    def UpdatePosition(self): 
        pass
    
    #===========================================================================
    # Get/Set the transformation to be applied to the image.
    #===========================================================================
    def SetTransform(self, Transform):
        pass
    
    def GetTransform(self):
        pass
    
    #===========================================================================
    # Get the ScalarBarActor.
    #===========================================================================
    def GetScalarBar(self):
        return self.ScalarBar
    
    #===========================================================================
    # Set/Get the scalar bar visibility
    #===========================================================================
    def SetScalarBarVisibility(self, v):
        self.ScalarBar.SetVisibility(v)
        self.Modified()
    
    def GetScalarBarVisibility(self):
        return self.ScalarBar.GetVisibility()
    
    def ScalarBarVisibilityOn(self):
        self.SetScalarBarVisibility(True)
    
    def ScalarBarVisibilityOff(self):
        self.SetScalarBarVisibility(False)
        
    #===========================================================================
    # Set/Get a user-defined lookup table. This method is synchronized.
    #===========================================================================
    def SetLookupTable(self, lut):
        self.LookupTable = lut
        self.ScalarBar.SetLookupTable(lut)
        self.Modified()
    
    def SyncSetLookupTable(self, lut):
        pass
    
    def GetLookupTable(self):
        return self.LookupTable
    
    #===========================================================================
    # Set/Get the window/level/zoom parameter.
    # This method is synchronized , except it LinkWindowLevel if set to 0.
    #===========================================================================
    def SetWindow(self, win):
        self.Window = win
        self.InvokeEvent("ViewImageWindowLevelChangeEvent")
        self.Modified()
    
    def GetWindow(self):
        return self.Window
    
    def SyncSetWindow(self, w):
        pass
    
    #===========================================================================
    # This method is called just before windowing. Subclass should give it a meaning.
    #===========================================================================
    def StartWindowing(self):
        pass
    
    def SyncStartWindowing(self):
        pass
    
    #===========================================================================
    # This method is called just after windowing. Subclass should give it a meaning.
    #===========================================================================
    def EndWindowing(self):
        pass
    
    def SyncEndWindowing(self):
        pass
    
    #==========================================================================
    # Set/Get the window/level/zoom parameter.
    # This method is synchronized , except it LinkWindowLevel if set to 0.
    #==========================================================================
    def SetLevel(self, lev):
        self.Level = lev
        self.InvokeEvent("ViewImageWindowLevelChangeEvent")
        self.Modified()
    
    def GetLevel(self):  
        return self.Level
    
    def SyncSetLevel(self, l):
        pass
    #===========================================================================
    # Reset window level to calculated default value.
    # This method is synchronized , except it LinkWindowLevel if set to 0.
    #===========================================================================
    def ResetWindowLevel(self):
        pass
    
    def SyncResetWindowLevel(self):
        pass
    
    #===========================================================================
    # Set (copy) the windows level from given view window level. 
    #===========================================================================
    def SetWindowLevelFrom(self, p_view):
        pass
    
    #===========================================================================
    # Set/Get the window/level/zoom parameter.
    # This method is synchronized unless LinkZoom is set to 0.
    #===========================================================================
    def SetZoom(self, zoom):
        self.Zoom = zoom
        self.InvokeEvent("ViewImageZoomChangeEvent")
        self.Modified()
    
    def GetZoom(self):
        return self.Zoom
    
    def SyncSetZoom(self, factor):
        pass
    
    #===========================================================================
    # Reset the current zoom factor.
    #===========================================================================
    def ResetZoom(self):
        pass
    
    def SyncResetZoom(self):
        pass
    
    #===========================================================================
    # Return the Z slice for the given position pos in real world coordinates. The Z slice is
    # relative to a given orientation.
    #===========================================================================
    def GetSliceForPosition(self, pos, p_orientation):
        pass
    
    #===========================================================================
    # Given a slice and an orientation, returns the real world coordinates.
    #===========================================================================
    def GetPositionForSlice(self, slice, orientation, pos):
        pass
    
    #===========================================================================
    # Set/Get the slice number within the current point is
    # param p_slice : the desired slice
    # param p_orientation : the desired slice type AXIAL, SAGITTAL, CORONAL. 
    #===========================================================================
    def SetSlice(self, p_orientation, p_slice):
        pass
    
    def SyncSetSlice(self, p_orientation, p_slice):
        pass
    
    def GetSlice(self, p_orientation):
        pass
    
    #==========================================================================
    # Set the Slice to display. Z is relative to the displayed plan.
    #==========================================================================
    def SetZSlice(self, p_slice):
        self.Modified() 
    
    def SyncSetZSlice(self, p_slice):
        pass
    
    #==========================================================================
    # Change the current position of the image. This method is synchronized.
    #==========================================================================
    def SetCurrentPoint(self, p_point): 
        pass
    
    def SyncSetCurrentPoint(self, p_point):
        pass
    
    #===========================================================================
    # Synonym to SetCurrentPoint().
    #===========================================================================
    
    def SetPosition(self, p_point):
        self.SetCurrentPoint(p_point)
    def SyncSetPosition(self, p_point):
        self.SyncSetCurrentPoint(p_point)
        
    #===========================================================================
    # Returns the current point.
    #===========================================================================
    def GetCurrentPoint(self):
        return self.CurrentPoint
    
    #==========================================================================
    # Reset the current point to the center of the image in the 3 axes.
    # This method is synchronized.
    #==========================================================================
    def ResetCurrentPoint(self):
        pass
    
    def SyncResetCurrentPoint(self):
        pass
    
    #===========================================================================
    # Synonym to SyncResetCurrentPoint().
    #===========================================================================
    def SyncResetPosition(self):
        self.SyncResetCurrentPoint()
    
    #===========================================================================
    # Reset Window-Level, current point and zoom. This method is synchronized.
    #===========================================================================
    def Reset(self):
        self.ResetWindowLevel()
        self.ResetCurrentPoint()
        self.ResetZoom()
    
    def SyncReset(self):
        pass
    
    #===========================================================================
    # Set the color window/level link ON or OFF.
    #===========================================================================
    def SetLinkWindowLevel(self, LinkWindowLevel):
        self.LinkWindowLevel = LinkWindowLevel
    
    def GetLinkWindowLevel(self):
        return self.LinkWindowLevel
    
    #===========================================================================
    # Set the position link ON or OFF.
    #===========================================================================
    def SetLinkPosition(self, LinkPosition):
        self.LinkPosition = LinkPosition
        
    def GetLinkPosition(self):
        return self.LinkPosition
    
    #==========================================================================
    # Set the zoom link ON or OFF.
    #==========================================================================
    def SetLinkZoom(self, LinkZoom):
        self.LinkZoom = LinkZoom
        
    def GetLinkZoom(self):
        return self.LinkZoom
    
    #===========================================================================
    # Shift/Scale are used to get the true image intensity if the image
    # was scaled before being inputed to the view.
    #===========================================================================
    def SetShift(self, Shift):
        self.Shift = Shift
    
    def GetShift(self, Shift):
        return self.Shift
    
    #==========================================================================
    # Shift/Scale are used to get the true image intensity if the image
    # was scaled before being inputed to the view.
    #==========================================================================
    def SetScale(self, Scale):
        self.Scale = Scale
        
    def GetScale(self):
        return self.Scale
    
    #===========================================================================
    # Set/Get the image visibility.
    #===========================================================================
    def SetVisibility(self, Visibility):
        self.Visibility = Visibility
    
    def GetVisibility(self):
        return self.Visibility
    
    #===========================================================================
    # Set/Get method for setting the size data. Size data consists in the
    # slice number and voxel size + window/level and is displayed at the
    # top left corner of the window.
    #===========================================================================
    def SetSizeData(self, str):
        pass
    
    def GetSizeData(self):
        return self.SizeData
    
    #===========================================================================
    # Set/Get the size data visibility.
    #===========================================================================
    def SetSizeDataVisibility(self, val):
        pass
    
    def SizeDataVisibilityOn(self):
        self.SetSizeDataVisibility(True)
    
    def SizeDataVisibilityOff(self):
        self.SetSizeDataVisibility(False)
        
    def GetSizeDataVisibility(self):
        return self.SizeDataVisibility
    
    def SetPatientNameData(self, str):
        pass
    
    def GetPatientNameData(self):
        self.PatientNameData
    
    def SetStudyNameData(self, str):
        pass
    
    def GetStudyNameData(self):
        return self.StudyNameData
    
    def SetSerieNameData(self, str):
        pass
    
    def GetSerieNameData(self):
        return self.SerieNameData
    
    #==========================================================================
    # Set/Get a mask image and its corresponding LookupTable. The mask image will
    # be overlapped to the current image, and the lookup table is used to assess
    # the color of the label: label 0 will have color given by entry 0 of the LUT, etc.
    # The image has to be of type unsigned char.
    # This method is synchronized.
    # 
    #==========================================================================
     
    def SetMaskImage(self, mask, lut):
        self.MaskImage = mask
        self.MaskLUT = lut
        self.Modified()
    
    #===========================================================================
    # Remove the mask image (if any)
    #===========================================================================
    def RemoveMaskImage(self):
        pass
    
    def SyncRemoveMaskImage(self):
        pass
    
    #===========================================================================
    # Set an overlapping second image. It uses an internal LUT to assess the color.
    # It does not need to be of type unsigned char.
    # This method is synchronized.
    #===========================================================================
    def SetOverlappingImage(self, image):
        self.OverlappingImage = image
        self.Modified()
    
    def SyncSetOverlappingImage(self, image):
        pass
    
    def GetOverlappingImage(self):
        return self.OverlappingImage
    
    #===========================================================================
    # Remove the overlapping image (if any)
    #===========================================================================
    def RemoveOverlappingImage(self):
        pass
    
    def SyncRemoveOverlappingImage(self):
        pass
    
    #===========================================================================
    # Add a dataset to the view (polydata or grid).
    # The dataset will be cut by planes defining the current slice displayed.
    # This results in a loss of dimensionality, i.e. tetrahedron will be displayed
    # as triangles, triangles as lines, lines as points.
    # A vtkProperty of the dataset can be specified.
    # This method is synchronized.
    #===========================================================================
    def AddDataSet(self, dataset, property=None):
        pass
    
    def SyncAddDataSet(self, dataset, property=None):
        pass
    
    #===========================================================================
    # This method allows you to remove a previously added dataset off the view.
    # It simply removes the actor from the renderer.
    # This method is synchronized.
    #===========================================================================
    def RemoveDataSet(self, dataset):
        pass
    
    def SyncRemoveDataSet(self, dataset):
        pass
    
    def RemoveAllDataSet(self):
        pass
    
    def SyncRemoveAllDataSet(self):
        pass
    
    #===========================================================================
    # Test if the dataset was already passed to the view.
    #===========================================================================
    def HasDataSet(self, dataset):
        pass
    
    def GetDataSet(self, ind):
        pass
    
    def GetDataSetFromActor(self, actor):
        pass
    
    def GetDataSetActor(self, ind):
        pass
    
    def GetDataSetActor(self, dataset):
        pass
    
    #===========================================================================
    # This method colorizes a given dataset (previously added with AddDataSet()) by one of its arrays
    # It doesn't handle colorization by a specific component yet. If the array contains multi-component scalars,
    # it takes the norm of the vector.
    # This method is synchronized.
    #===========================================================================
    def ColorDataSetByArray(self, dataset, arrayname, transfer):
        pass
    
    def SyncColorDataSetByArray(self, dataset, arrayname, transfer):
        pass
    
    #===========================================================================
    # This method changes the actors associated with a given dataset (previously added with AddDataSet())
    # to switch between the use of cell array or point data array. Used for switch between color and direction based
    # colors of fiber bundles projections.
    # This method is synchronized. 
    #===========================================================================
    def ModifyActors(self, dataset, cellColors):
        pass
    
    def SyncModifyActors(self, dataset, cellColors):
        pass
    
    #===========================================================================
    # Specify how the ResetWindowLevel() method behaves. If set to FullRange,
    # ResetWindowLevel() sets the contrast to match the full range of the image
    # i.e: 0:range[0] and 255: range[1].
    # If set to UserDefinedPercentage, the X% highest and lowest voxels are
    # removed to calculate the range. It is more robust to outliers that have
    # a very high and low intensity compared to the main element of the image.
    # The percentage is set with SetWindowLevelPercentage() (default: 0.1).
    #===========================================================================
    def SetResetWindowLevelMode(self, mode):
        self.ResetWindowLevelMode = mode
        self.Modified()
    
    def SetResetWindowLevelModeToFullRange(self):
        self.ResetWindowLevelMode = self.FullRange
        self.Modified()
    
    def SetResetWindowLevelModeToUserDefinedPercentage(self):
        self.ResetWindowLevelMode = self.UserDefinedPercentage
        self.Modified()
        
    #===========================================================================
    # Set the percentage of voxels used to reset the window/level range when
    # the reset window/level mode is set to UserDefinedPercentage.
    #===========================================================================
    def SetWindowLevelPercentage(self, WindowLevelPercentage):
        self.WindowLevelPercentage = WindowLevelPercentage
    
    def GetWindowLevelPercentage(self):
        return self.WindowLevelPercentage
    
    #===========================================================================
    # derived from vtkSynchronizedView
    #===========================================================================
    def Initialize(self):
        pass
    
    def Uninitialize(self):
        pass
    
    #===========================================================================
    # Register the image. Internal Use Only.
    #===========================================================================
    def RegisterImage(self, image):
        pass
    
    def Initialize(self):
        vtkSynchronizedView.Initialize(self)
        bwLut = vtk.vtkLookupTable()
        bwLut.SetTableRange(0, 1)
        bwLut.SetSaturationRange(0, 0)
        bwLut.SetHueRange(0, 0)
        bwLut.SetValueRange(0, 1)
        bwLut.Build()
        
        self.SetLookupTable(bwLut)
        self.AddActor(self.ScalarBar)
        
        del bwLut
    
    def RegisterImage(self, image):
        if not image:
            return
        if image <> self.Image:
            if self.Image <> None:
                self.Image.UnRegister(self)
            self.Image = image
            self.Image.Register(self)
    
    def GetWholeMinPosition(self, p_axis):
        if not self.Image:
            return -vtk.VTK_LARGE_FLOAT
        return self.Image.GetBounds()[p_axis*2]
    
    def GetWholeMaxPosition(self, p_axis):
        if not self.Image:
            return vtk.VTK_LARGE_FLOAT
        return self.Image.GetBounds()[p_axis*2+1]
    
    def GetOrthogonalAxis(self, p_plan):
        assert (p_plan<self.NB_DIRECTION_IDS), \
                "plan's index should be a unsigned integer less than %s" %(vtkViewImage.NB_DIRECTION_IDS)
        if p_plan == self.SAGITTAL_ID:
            return self.X_ID
        elif p_plan == self.CORONAL_ID:
            return self.Y_ID
        elif p_plan == self.AXIAL_ID:
            return self.Z_ID
        else:
            return 0
    
    def GetSliceForPoint(self, pos, p_plan):
        if not self.Image:
            return 0
        assert (p_plan<self.NB_DIRECTION_IDS), \
                "plan's index should be a unsigned integer less than %s" %(vtkViewImage.NB_DIRECTION_IDS)
        spacing = self.Image.GetSpacing()
        origin = self.Image.GetOrigin()
        
        axis = self.GetOrthogonalAxis(p_plan)
        soft_pos = pos[axis]
#        pos_max = self.GetWholeMaxPosition(axis)
#        pos_min = self.GetWholeMinPosition(axis)
#        print origin[axis],": ",spacing[axis],": " ,soft_pos, ": ", pos_max, ": ", pos_min
#        #  Treat extreme position at the end of the last pixel
#        if ((soft_pos > pos_max - 0.005) and (soft_pos < pos_max+0.005)):
#            soft_pos = pos_max - 0.005
#        if ((soft_pos > pos_min - 0.005) and (soft_pos < pos_min+0.005)):
#            soft_pos = pos_min + 0.005
        return vtk.vtkMath.Round((soft_pos-origin[axis])/spacing[axis])
     
    def GetSlice(self, p_plan):
        pos = self.CurrentPoint
        return self.GetSliceForPoint(pos, p_plan)
    
    def SetSlice(self, p_plan, p_zslice):
        self.SetCurrentPoint( self.GetPositionForSlice(p_zslice, p_plan) )
        
    def GetPositionForSlice(self, p_zslice, orientation):
        if not self.Image:
            return 
        axis = self.GetOrthogonalAxis(orientation)
        spacing = self.Image.GetSpacing()
        extent = self.Image.GetWholeExtent()
        origin = self.Image.GetOrigin()
        slice = p_zslice
        
        dims = []
        dims.append(extent[1])
        dims.append(extent[3])
        dims.append(extent[5])
        
        if slice>=dims[axis]:
            slice=dims[axis]
        
        if slice<0:
            slice=0
        
        pos = self.CurrentPoint
        pos[axis]=origin[axis]+slice*spacing[axis]
        return pos
    
    def SyncSetSlice(self, p_plan, p_zslice):
        if self.IsLocked():
            return
        self.SetSlice(p_plan, p_zslice)
        self.Lock()
        for view in self.Children:
            if (view and view.LinkPosition):
                view.SyncSetSlice(p_plan, p_zslice)
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()   
    
    def SyncSetZSlice(self, p_zslice):
        if self.IsLocked():
            return
        self.SetZSlice(p_zslice)
        self.Lock()
        for view in self.Children:
            if (view and view.LinkPosition):
                view.SyncSetZSlice(p_zslice)
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def GetVoxelCoordinates(self, pos):
        if not self.Image:
            return
        p_coordinates = [0]*3
        p_coordinates[self.GetOrthogonalAxis(self.SAGITTAL_ID)] = \
                        self.GetSliceForPoint(pos, self.SAGITTAL_ID)
        p_coordinates[self.GetOrthogonalAxis(self.CORONAL_ID)] = \
                        self.GetSliceForPoint(pos, self.CORONAL_ID)
        p_coordinates[self.GetOrthogonalAxis(self.AXIAL_ID)] = \
                        self.GetSliceForPoint(pos, self.AXIAL_ID)            
        return p_coordinates
    
    def GetCurrentVoxelCoordinates(self):
        p_coordinates = [0]*3
        p_coordinates[self.GetOrthogonalAxis(self.SAGITTAL_ID)] = \
                        self.GetSlice(self.SAGITTAL_ID)
        p_coordinates[self.GetOrthogonalAxis(self.CORONAL_ID)] = \
                        self.GetSlice(self.CORONAL_ID)
        p_coordinates[self.GetOrthogonalAxis(self.AXIAL_ID)] = \
                        self.GetSlice(self.AXIAL_ID)
        return p_coordinates
    
    def SyncSetCurrentPoint(self, p_point):
        if self.IsLocked():
            return
        self.SetCurrentPoint(p_point)
        
        # this boolean is used so that the other observe won't call
        # SetCurrentPoint again and again and again...
        self.Lock()
        for view in self.Children:
            if (view and view.LinkPosition):
                view.SyncSetCurrentPoint(p_point)
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def GetCurrentPointDoubleValue(self):
        if not self.Image:
            return -1.0
        
        coordinates = self.GetCurrentVoxelCoordinates()
        print coordinates
        scalar = self.Image.GetScalarComponentAsDouble(coordinates[0],coordinates[1],
                                                        coordinates[2], 0)
        if not scalar:
            return -1.0
        return scalar
    
    def SyncResetCurrentPoint(self):   
        if self.IsLocked():
            return
        self.ResetCurrentPoint()
        self.Lock()
        for view in self.Children:
            if (view and view.LinkPosition):
                view.SyncResetCurrentPoint()
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def ResetCurrentPoint(self):
        if not self.Image:
            return
        
        bounds = self.Image.GetBounds()
        
        pos = [(bounds[0]+bounds[1])/2.0, (bounds[2]+bounds[3])/2.0, 
               (bounds[4]+bounds[5])/2.0,]
        self.SetCurrentPoint(pos)
    
    def SyncSetWindow(self, w):
        if self.IsLocked():
            return
        
        self.SetWindow(w)
        
        # this boolean is used so that the other observe won't call
        # SetCurrentPoint again and again and again...
        self.Lock()
        for view in self.Children:
            if (view and view.LinkWindowLevel):
                view.SyncSetWindow(w)
                if view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
        
    def SyncSetLevel(self, l):
        if self.IsLocked():
            return
        self.SetLevel(l)
        
        # this boolean is used so that the other observe won't call
        # SetCurrentPoint again and again and again...
        self.Lock()
        for view in self.Children:
            if (view and view.LinkWindowLevel):
                view.SyncSetLevel(l)
                if view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
        
    # Set/Get window/level for mapping pixels to colors. 
    def GetColorWindow(self):
        return -1.0
    
    def GetColorLevel(self):
        return -1.0
    
    def SetWindowLevelFrom(self, p_view):
        if p_view:
            self.SetWindow(p_view.GetColorWindow())
            self.SetLevel(p_view.GetColorLevel())
            
    
    def SyncResetWindowLevel(self):
        if self.IsLocked():
            return
        self.ResetWindowLevel()
        self.Lock()
        for view in self.Children:
            if (view and view.LinkWindowLevel):
                view.SyncResetWindowLevel()
                if view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def ResetWindowLevel(self):
        if self.IsLocked():
            return
        
        if self.Image:
            return
        
        self.Image.UpdateInformation()
        self.Image.SetUpdateExtent(self.Image.GetWholeExtent())
        self.Image.Update()
        
        if (self.Image.GetScalarType() == vtk.VTK_UNSIGNED_CHAR and 
            (self.Image.GetNumberOfScalarComponents() == 3 or 
             self.Image.GetNumberOfScalarComponents() == 4 )):
            return
        range = self.Image.GetScalarRange()
        histogram = vtk.vtkImageAccumulate()
        histogram.SetInput(self.Image)
        
        histogram.SetComponentExtent(0, 1000, 0, 0, 0, 0)
        histogram.SetComponentSpacing((range[1]-range[0])/1000.0, 0.0, 0.0)
        histogram.SetComponentOrigin(range[0], 0.0, 0.0)
        histogram.Update()
        
        output = histogram.GetOutput()
        ptData = output.GetPointData().GetScalars()
        if ptData:
            raise RuntimeError, "Error: Cannot cast point data to integers."
        numVox = histogram.GetVoxelCount()
        onePercent = numVox/100.0
        
        start = 1
        currentPercent = 0.0
        while (currentPercent<0.1 and start<999):
            ptData.GetTuple(start, tuple)
            currentPercent = currentPercent + tuple/onePercent
            start = start+1
            
        currentPercent = 0.0
        end = 999
        while (currentPercent<0.1 and end>0):
            ptData.GetTuple(start, tuple)
            currentPercent = currentPercent + tuple/onePercent
            end = end-1
        
        window = (end-start)*(range[1]-range[0])/1000.0
        level = 0.5*(start + end)*(range[1]-range[0])/1000.0
        window = (window-self.Shift)/self.Scale
        level = (level-self.Shift)/self.Scale
        
        self.SetWindow(window)
        self.SetLevel(level)
        del histogram
        
    def HasDataSet(self, dataset):
        if not dataset:
            return False
        if dataset in self.DataSetList:
            return True
        return False
    
    def SyncAddDataSet(self, dataset, property):
        if self.IsLocked():
            return None
        actor = self.AddDataSet(dataset, property)
        
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncAddDataSet(dataset, property)
        self.UnLock()
        return actor
    
    def AddDataSet(self, dataset, property):
        assert 1, "You should not use this function here\nPlease use \
        vtkViewImage2D or vtkViewImage3D classes instead (or any derived class)."
    
    def SyncRemoveDataSet(self, dataset):  
        if self.IsLocked():
            return 
        self.RemoveDataSet(dataset)
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncRemoveDataSet(dataset)
        self.UnLock()
    
    def RemoveDataSet(self, dataset):
        if not dataset:
            return
        try:
            ind = self.DataSetList.index(dataset)
            self.RemoveActor(self.DataSetActorList[ind])
            self.DataSetActorList.remove(self.DataSetActorList[ind])
            self.DataSetList.remove(self.DataSetList[ind])
        except ValueError:
            return
    
    def SyncRemoveAllDataSet(self):
        if self.IsLocked():
            return
        self.RemoveAllDataSet()
        
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncRemoveAllDataSet()
        self.UnLock()
        
    def RemoveAllDataSet(self):
        for actor in self.DataSetActorList:
            self.RemoveActor(actor)
        self.DataSetActorList = []
        self.DataSetList = []
    
    def SyncModifyActors(self, dataset, cellColors):
        if self.IsLocked():
            return
        self.ModifyActors(dataset, cellColors)
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncModifyActors(dataset, cellColors)
        self.UnLock()
    
    def ModifyActors(self, dataset, cellColors):
        doit = True
        
        if not dataset:
            doit = False
        
        mapper = None
        
        if doit:
            try:
                ind = self.DataSetList.index(dataset)
                mapper = self.DataSetActorList[ind].GetMapper()
            except ValueError:
                doit = False
        if doit:
            mapper.Modified()
            if cellColors:
                mapper.SetScalarModeToUseCellData()
            else:
                mapper.SetScalarModeToUsePointData()
    
    def SyncColorDataSetByArray(self, dataset, arrayname, transfer):
        if self.IsLocked():
            return
        self.ColorDataSetByArray(dataset, arrayname, transfer)
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncColorDataSetByArray(dataset, arrayname, transfer)
        self.UnLock()
    
    def ColorDataSetByArray(self, dataset, arrayname, transfer):
        doit = True
        if not dataset:
            doit = False
        
        array = None
        mapper = None
        if doit:
            try:
                ind = self.DataSetList.index(dataset)
                mapper = self.DataSetActorList[ind].GetMapper()
            except ValueError:
                doit = False
        if doit:
            mapper.Modified()
            if dataset.GetCellData():
                array = dataset.GetCellData().GetArray(arrayname)
                if array:
                    mapper.SetScalarModeToUseCellFieldData()
            if (not array and dataset.GetPointData()):
                array = dataset.GetPointData().GetArray(arrayname)
                if array:
                    mapper.SetScalarModeToUsePointFieldData()
            if not array:
                mapper.SetScalarModeToDefault()
                mapper.SetInterpolateScalarsBeforeMapping()
                doit = False
        
        if doit:
            mapper.SetLookupTable(transfer)
            mapper.SetScalarRange(array.GetRange())
            mapper.SetInterpolateScalarsBeforeMapping(1)
            mapper.SelectColorArray(array.GetName())
        
    def GetDataSet(self, i):
        try:
            return self.DataSetList[i]
        except IndexError:
            return None
    
    def GetDataSetFromActor(self, actor):
        try:
            ind = self.DataSetActorList.index(actor)
            return self.DataSetList[ind]
        except ValueError:
            return None
        
    def GetDataSetActor(self, i):
        if isinstance(i, int):
            try:
                return self.DataSetActorList[i]
            except IndexError:
                return None
        else:
            try:
                ind = self.DataSetList.index(i)
                return self.DataSetActorList[ind]
            except ValueError:
                return None    
        return None
    
    def SyncSetZoom(self, factor):
        if self.IsLocked():
            return
        self.SetZoom(factor)
        self.Lock()
        for view in self.Children:
            if (view and view.LinkZoom):
                view.SyncSetZoom(factor)
        self.UnLock()
    
    def SetWindow(self, window):
        self.Window = window
        self.InvokeEvent("ViewImageWindowLevelChangeEvent")
        
    def SetLevel(self, level):
        self.Level = level
        self.InvokeEvent("ViewImageWindowLevelChangeEvent")
        
    def SetZoom(self, zoom):
        self.Zoom = zoom
        self.InvokeEvent("ViewImageZoomChangeEvent")
        
    def SetLookupTable(self, lut):
        self.LookupTable = lut
        self.ScalarBar.SetLookupTable(lut)
    
    def SetCurrentPoint(self, pos):
        self.CurrentPoint = pos
        self.UpdatePosition()
        self.InvokeEvent("ViewImagePositionChangeEvent")
    
    def SyncSetPosition(self, p_point): 
        self.SyncSetCurrentPoint(p_point)
    
    def SyncResetPosition(self):
        self.SyncResetCurrentPoint()
    
    def Reset(self):
        self.ResetWindowLevel()
        self.ResetCurrentPoint()
        self.ResetZoom()
    
    def SetMaskImage(self, mask, lut):
        self.MaskImage = mask
        self.MaskLUT = lut
        
    def SyncSetLookupTable(self, lut):
        if self.IsLocked():
            return
        self.SetLookupTable(lut)
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncSetLookupTable(lut)
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def SyncResetZoom(self):
        if self.IsLocked():
            return
        self.ResetZoom()
        self.Lock()
        for view in self.Children:
            if view and view.LinkZoom:
                view.SyncResetZoom()
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def ResetZoom(self):
        self.ResetCamera()
        self.Zoom = 1.0
    
    def SyncReset(self):
        if self.IsLocked():
            return
        self.Reset()
        self.Lock()
        for view in self.Children:
            if view:
                view.Reset()
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def SyncSetMaskImage(self, mask, lut):
        if self.IsLocked():
            return
        self.SetMaskImage(mask, lut)
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncSetMaskImage(mask, lut)
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def SyncSetOverlappingImage(self, image):
        if self.IsLocked():
            return
        self.SetOverlappingImage(image)
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncSetOverlappingImage(image)
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def SyncRemoveMaskImage(self):
        if self.IsLocked():
            return
        self.RemoveMaskImage()
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncRemoveMaskImage()
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def SyncRemoveOverlappingImage(self):
        if self.IsLocked():
            return
        self.RemoveOverlappingImage()
        self.Lock()
        for view in self.Children:
            if view:
                view.SyncRemoveOverlappingImage()
                if not view.GetRenderWindow().GetNeverRendered():
                    view.Render()
        self.UnLock()
    
    def RemoveOverlappingImage(self):
        pass
    
    def RemoveMaskImage(self):
        pass
    
    def SetLinkZoom(self, value):
        self.LinkZoom = value
    
    def GetCurrentPoint(self):
        return self.CurrentPoint
    
    def SetSizeData(self, str):
        self.SizeData = str
    
    def GetSizeData(self):
        return self.SizeData
        
    
if __name__ == "__main__":
    print [1,2,3][3]
    print vtkViewImage().GetOrthogonalAxis(4)