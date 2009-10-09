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
    ViewImagePositionChangeEvent = 1000+1
    ViewImageWindowLevelChangeEvent = 1000+2
    ViewImageZoomChangeEvent = 1000+3
    
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
    
    def SetImage(self, image):
        assert 1, "You should not use this function here\nPlease use \
                    vtkViewImage2D or vtkViewImage3D classes instead"
    
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
        return self.Image.GetBounds()[p_axis*2]
    
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
        pos_max = self.GetWholeMaxPosition(axis)
        pos_min = self.GetWholeMinPosition(axis)
        
        #  Treat extreme position at the end of the last pixel
        if ((soft_pos > pos_max - 0.005) and (soft_pos < pos_max+0.005)):
            soft_pos = pos_max - 0.005
        if ((soft_pos > pos_min - 0.005) and (soft_pos < pos_min+0.005)):
            soft_pos = pos_min + 0.005
        return vtkrint(soft_pos-origin[axis])/spacing[axis];      
     
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
        scalar = self.Image.GetScalarPointer(coordinates)
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
        self.InvokeEvent(self.ViewImageWindowLevelChangeEvent)
        
    def SetLevel(self, level):
        self.Level = level
        self.InvokeEvent(self.ViewImageWindowLevelChangeEvent)
        
    def SetZoom(self, zoom):
        self.Zoom = zoom
        self.InvokeEvent(self.ViewImageZoomChangeEvent)
        
    def SetLookupTable(self, lut):
        self.LookupTable = lut
        self.ScalarBar.SetLookupTable(lut)
    
    def SetCurrentPoint(self, pos):
        self.CurrentPoint = pos
        self.UpdatePosition()
        self.InvokeEvent(self.ViewImagePositionChangeEvent)
    
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
            if view and view.LinkZoom():
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