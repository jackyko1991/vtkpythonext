# -*- coding:utf-8 -*-
"""
Created on 2009-10-12

@author: summit
"""

# -*- coding:utf-8 -*-
"""
Created on 2009-10-6

@author: summit
"""
import vtk 
from jolly.jolly_vtk.vtkPythonInteractorStyleImage import *
from jolly.jolly_vtk.vtkViewImage2D import *
import math


class vtkPythonInteractorStyleImage2D(vtkPythonInteractorStyleImage):
    # Motion flags
    VTKIS_WINDOW_LEVEL=1024
    VTKIS_PICK=1025
    VTKIS_MEASURE=5050
    VTKIS_ZSLICE_MOVE=5051
    VTKIS_DOLLY=4
    VTKIS_PAN=2
    VTKIS_NONE=0
    
    
    def __init__(self):
        vtkPythonInteractorStyleImage.__init__(self) 
         
        self.View = None
        self.ZSliceStep = 0
        self.LevelStep = 0.0
        self.WindowStep = 0.0
    
    def SetView(self, view):
        self.View = view
    
    def OnMouseMove(self):
        x,y = self.Interactor.GetEventPosition()
        self.State = self.GetState()
        if self.State == self.VTKIS_WINDOW_LEVEL:
            self.FindPokedRenderer(x,y)
            self.WindowLevel()
            self.InvokeEvent("InteractionEvent")
        elif self.State == self.VTKIS_PICK:
            # No Drag is allowed for picking. Toggle to ZSliceMove state
            # We force StartZSliceMove without ending the picking.
            # We don't want to pick at all
            self.StopState()
            self.StartZSliceMove()
            # There we don't break to let the hand to ZSliceMove
            
        elif self.State == self.VTKIS_ZSLICE_MOVE:
            self.FindPokedRenderer(x,y)
            self.ZSliceMove()
            self.InvokeEvent("InteractionEvent")
            
        elif self.State == self.VTKIS_DOLLY:
            self.FindPokedRenderer(x,y)
            self.InvokeEvent("ZoomEvent")
        
        elif self.State == self.VTKIS_PAN:
            self.FindPokedRenderer(x,y)
            self.Pan()
            self.PropagateCameraFocalAndPosition()
            self.InvokeEvent("InteractionEvent")
        else:
            pass
    
    def PropagateCameraFocalAndPosition(self):
        if not self.View:
            return
        if not self.View.Renderer:
            return
        
        camera = self.View.Renderer.GetActiveCamera()
        focal = camera.GetFocalPoint()
        pos = camera.GetPosition()
        
        # save the flags
        LinkCamera = self.GetLinkCameraFocalAndPosition()
        self.View.SetLinkCameraFocalAndPosition(False)
        self.View.SyncSetCameraFocalAndPosition(focal, pos)
        self.View.SetLinkCameraFocalAndPosition(LinkCamera)
    
    def OnLeftButtonDown(self):
        x,y = self.Interactor.GetEventPosition()
        self.FindPokedRenderer(x,y)
        self.CurrentRenderer = self.GetCurrentRenderer()
        if not self.CurrentRenderer:
            return
        
        style =  self.View.LeftButtonInteractionStyle
        print style
        if style == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
            self.WindowLevelStartPosition[0]=x
            self.WindowLevelStartPosition[1]=y
            self.StartWindowLevel()
        elif style == vtkViewImage2D.SELECT_INTERACTION:
            self.StartPick()
        elif style == vtkViewImage2D.FULL_PAGE_INTERACTION:
            self.FullPage()
        elif style == vtkViewImage2D.MEASURE_INTERACTION:
            self.StatrMeasure()
        elif style == vtkViewImage2D.ZOOM_INTERACTION:
            self.Interactor = self.GetInteractor()
            if self.Interactor.GetShiftKey():
                self.StartPan()
            else:
                self.StartDolly() # continuous zoom
    
    def OnMiddleButtonDown(self):
        x,y = self.Interactor.GetEventPosition()
        self.FindPokedRenderer(x,y)
        self.CurrentRenderer = self.GetCurrentRenderer()
        if not self.CurrentRenderer:
            return
        
        style =  self.View.MiddleButtonInteractionStyle
        if style == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
            self.WindowLevelStartPosition[0]=x
            self.WindowLevelStartPosition[1]=y
            self.StartWindowLevel()
        elif style == vtkViewImage2D.SELECT_INTERACTION:
            self.StartPick()
        elif style == vtkViewImage2D.FULL_PAGE_INTERACTION:
            self.FullPage()
        elif style == vtkViewImage2D.MEASURE_INTERACTION:
            self.StatrMeasure()
        elif style == vtkViewImage2D.ZOOM_INTERACTION:
            self.Interactor = self.GetInteractor()
            if self.Interactor.GetShiftKey():
                self.StartPan()
            else:
                self.StartDolly() # continuous zoom
    
    def OnMiddleButtonUp(self):
        self.State = self.GetState()
        if self.State == self.VTKIS_ZSLICE_MOVE:
            self.EndZSliceMove()
        elif self.State == self.VTKIS_WINDOW_LEVEL:
            self.EndWindowLevel()
        elif self.State == self.VTKIS_PICK:
            self.EndPick()
        elif self.State == self.VTKIS_MEASURE:
            self.EndMeasure()
        elif self.State == self.VTKIS_PAN:
            self.EndPan()
        elif self.State == self.VTKIS_DOLLY:
            self.EndDolly() # continuous zoom
    
    def OnLeftButtonUp(self):
        self.State = self.GetState()
        if self.State == self.VTKIS_ZSLICE_MOVE:
            self.EndZSliceMove()
        elif self.State == self.VTKIS_WINDOW_LEVEL:
            self.EndWindowLevel()
        elif self.State == self.VTKIS_PICK:
            self.EndPick()
        elif self.State == self.VTKIS_MEASURE:
            self.EndMeasure()
        elif self.State == self.VTKIS_PAN:
            self.EndPan()
        elif self.State == self.VTKIS_DOLLY:
            self.EndDolly() # continuous zoom
    
    def OnRightButtonDown(self):
        x,y = self.Interactor.GetEventPosition()
        self.FindPokedRenderer(x,y)
        self.CurrentRenderer = self.GetCurrentRenderer()
        if not self.CurrentRenderer:
            return
        
        style =  self.View.MiddleButtonInteractionStyle
        if style == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
            self.WindowLevelStartPosition[0]=x
            self.WindowLevelStartPosition[1]=y
            self.StartWindowLevel()
        elif style == vtkViewImage2D.SELECT_INTERACTION:
            self.StartPick()
        elif style == vtkViewImage2D.FULL_PAGE_INTERACTION:
            self.FullPage()
        elif style == vtkViewImage2D.MEASURE_INTERACTION:
            self.StatrMeasure()
        elif style == vtkViewImage2D.ZOOM_INTERACTION:
            self.Interactor = self.GetInteractor()
            if self.Interactor.GetShiftKey():
                self.StartPan()
            else:
                self.StartDolly() # continuous zoom
    
    def OnRightButtonUp(self):
        self.State = self.GetState()
        if self.State == self.VTKIS_ZSLICE_MOVE:
            self.EndZSliceMove()
        elif self.State == self.VTKIS_WINDOW_LEVEL:
            self.EndWindowLevel()
        elif self.State == self.VTKIS_PICK:
            self.EndPick()
        elif self.State == self.VTKIS_MEASURE:
            self.EndMeasure()
        elif self.State == self.VTKIS_PAN:
            self.EndPan()
        elif self.State == self.VTKIS_DOLLY:
            self.EndDolly() # continuous zoom
        else:
            pass
        
    def OnChar(self):
        rwi = self.GetInteractor()
        factor = 0.0
        size = self.View.RenderWindow.GetSize()
        
        key_sym = rwi.GetKeySym()
        if key_sym == "Up" or key_sym == "KP_Up":
            if self.View.InteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
                self.StartWindowLevel()
                self.SetWindowStep(0.0)
                self.SetLevelStep(4.0/size[1])
                self.InvokeEvent("WindowLevelEvent")
                self.EndWindowLevel()
            elif self.View.InteractionStyle == vtkViewImage2D.SELECT_INTERACTION: 
                self.StartZSliceMove()
                self.ZSliceStep = 1
                self.InvokeEvent("ZSliceMoveEvent")  
                self.EndZSliceMove()
            elif self.View.InteractionStyle == vtkViewImage2D.ZOOM_INTERACTION:
                self.StartDolly()
                factor=2.0
                self.View.SyncSetZoom(math.pow(1.1, factor)*self.View.Zoom)
                self.EndDolly()
            else:
                pass
        elif key_sym == "Right" or key_sym == "KP_Right":
            if self.View.InteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
                self.StartWindowLevel()
                self.SetLevelStep(0.0)
                self.SetWindowStep(4.0/size[1])
                self.InvokeEvent("WindowLevelEvent")
                self.EndWindowLevel()
            else:
                pass
        elif key_sym == "Left" or key_sym == "KP_Left":
            if self.View.InteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
                self.StartWindowLevel()
                self.SetWindowStep(-4.0/size[1])
                self.SetLevelStep(0.0)
                self.InvokeEvent("WindowLevelEvent")
                self.EndWindowLevel()
            else:
                pass
        elif key_sym == "Down" or key_sym == "KP_Down":
            if self.View.InteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
                self.StartWindowLevel()
                self.SetWindowStep(0.0)
                self.SetLevelStep(-4.0/size[1])
                self.InvokeEvent("WindowLevelEvent")
                self.EndWindowLevel()
            elif self.View.InteractionStyle == vtkViewImage2D.SELECT_INTERACTION: 
                self.StartZSliceMove()
                self.ZSliceStep = -1
                self.InvokeEvent("ZSliceMoveEvent")  
                self.EndZSliceMove()
            elif self.View.InteractionStyle == vtkViewImage2D.ZOOM_INTERACTION:
                self.StartDolly()
                factor=-2.0
                self.View.SyncSetZoom(math.pow(1.1, factor)*self.View.Zoom)
                self.EndDolly()
            else:
                pass
        elif key_sym == "Page_Down" or key_sym == "KP_Page_Down":
            if self.View.InteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
                self.StartWindowLevel()
                self.SetWindowStep(0.0)
                self.SetLevelStep(-40.0/size[1])
                self.InvokeEvent("WindowLevelEvent")
                self.EndWindowLevel()
            elif self.View.InteractionStyle == vtkViewImage2D.SELECT_INTERACTION: 
                self.StartZSliceMove()
                self.ZSliceStep = -10
                self.InvokeEvent("ZSliceMoveEvent")  
                self.EndZSliceMove()
            elif self.View.InteractionStyle == vtkViewImage2D.ZOOM_INTERACTION:
                self.StartDolly()
                factor=-20.0
                self.View.SyncSetZoom(math.pow(1.1, factor)*self.View.Zoom)
                self.EndDolly()
            else:
                pass
        if key_sym == "Page_Up" or key_sym == "KP_Page_Up":
            if self.View.InteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
                self.StartWindowLevel()
                self.SetWindowStep(0.0)
                self.SetLevelStep(40.0/size[1])
                self.InvokeEvent("WindowLevelEvent")
                self.EndWindowLevel()
            elif self.View.InteractionStyle == vtkViewImage2D.SELECT_INTERACTION: 
                self.StartZSliceMove()
                self.ZSliceStep = 10
                self.InvokeEvent("ZSliceMoveEvent")  
                self.EndZSliceMove()
            elif self.View.InteractionStyle == vtkViewImage2D.ZOOM_INTERACTION:
                self.StartDolly()
                factor=20.0
                self.View.SyncSetZoom(math.pow(1.1, factor)*self.View.Zoom)
                self.EndDolly()
            else:
                pass
        
        path = None
        picker = None
        self.CurrentRenderer = self.GetCurrentRenderer()
        if rwi.GetKeyCode() in ['f', 'F']:
            # self.AnimState = self.VTKIS_ANIM_ON
            self.FindPokedRenderer(rwi.GetEventPosition()[0], rwi.GetEventPosition()[1])
            rwi.GetPicker().Pick(rwi.GetEventPosition()[0], 
                                 rwi.GetEventPosition()[1],
                                 0.0,
                                 self.CurrentRenderer)
            picker=rwi.GetPicker()
            if picker:
                path = picker.GetPath()
            if path:
                rwi.FlyToImage(self.CurrentRenderer, picker.GetPickPosition())
            # self.AnimState = self.VTKIS_ANIM_ON   
        elif rwi.GetKeyCode() in ['r', 'R']:
            if (self.View.LeftButtonInteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION
                or self.View.RightButtonInteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION
                or self.View.MiddleButtonInteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION
                or self.View.WheelInteractionStyle == vtkViewImage2D.WINDOW_LEVEL_INTERACTION
                ):
                self.InvokeEvent("ResetWindowLevelEvent")
            if (self.View.LeftButtonInteractionStyle == vtkViewImage2D.SELECT_INTERACTION
                or self.View.RightButtonInteractionStyle == vtkViewImage2D.SELECT_INTERACTION
                or self.View.MiddleButtonInteractionStyle == vtkViewImage2D.SELECT_INTERACTION
                or self.View.WheelInteractionStyle == vtkViewImage2D.SELECT_INTERACTION
                ):
                self.InvokeEvent("ResetPositionEvent")
            if (self.View.LeftButtonInteractionStyle == vtkViewImage2D.ZOOM_INTERACTION
                or self.View.RightButtonInteractionStyle == vtkViewImage2D.ZOOM_INTERACTION
                or self.View.MiddleButtonInteractionStyle == vtkViewImage2D.ZOOM_INTERACTION
                or self.View.WheelInteractionStyle == vtkViewImage2D.ZOOM_INTERACTION
                ):
                self.InvokeEvent("ResetZoomEvent")
        else:
            pass

    def StartZSliceMove(self):
        self.State = self.GetState()
        if ((self.State <> self.VTKIS_NONE) and (self.State <> self.VTKIS_PICK)):
            self.StartState(self.VTKIS_ZSLICE_MOVE)
            self.InvokeEvent("StartZSliceMoveEvent")
    
    def ZSliceMove(self):
        rwi = self.GetInteractor()
        dy = rwi.GetEventPosition()[1] - rwi.GetLastEventPosition()[1]
        self.ZSliceStep = dy
        self.InvokeEvent("ZSliceMoveEvent")
    
    def ZSliceWheelForward(self):
        dy = self.GetMouseWheelMotionFactor()
        self.ZSliceStep = dy
        self.InvokeEvent("ZSliceMoveEvent")
    
    def ZSliceWheelBackward(self):
        dy = int(-1.0*self.GetMouseWheelMotionFactor())
        self.ZSliceStep = dy
        self.InvokeEvent("ZSliceMoveEvent")
    
    def EndZSliceMove(self):
        if self.GetState() <> self.VTKIS_ZSLICE_MOVE:
            return
        self.InvokeEvent("EndZSliceMoveEvent")
        self.StopState()
    
    def FullPage(self):
        self.InvokeEvent("FullPageEvent")
    
    def StartMeasure(self):
        if self.GetState() <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_MEASURE)
        self.InvokeEvent("StartMeasureEvent")
    
    def Measure(self):
        self.InvokeEvent("Measure")
    
    def EndMeasure(self):
        if self.GetState() <> self.VTKIS_MEASURE:
            return
        self.InvokeEvent("EndMeasureEvent")
        self.StopState()
    
    def WindowLevel(self):
        # vtkInteractorStyleImage2D.WindowLevel()
        rwi = self.GetInteractor()
        # self.WindowLevelCurrentPosition = rwi.GetEventPosition()
        size = self.View.RenderWindow.GetSize()
        
        # Compute normalized delta
        dx = 4.0 * (rwi.GetEventPosition()[0]-
                    self.GetWindowLevelStartPosition[0])/size[0]
        dy = 4.0 * (self.GetWindowLevelStartPosition[1]-
                    rwi.GetEventPosition()[1])/size[1]
        self.WindowStep = dx
        self.SetLevelStep = dy
        self.InvokeEvent("WindowLevelEvent")
    
    def WindowLevelWheelForward(self):
        size = self.View.RenderWindow.GetSize()
        dy = 4.0*float(self.GetMouseWheelMotionFactor())/size[1]
        self.WindowStep = 0.0
        self.SetLevelStep = dy
        self.InvokeEvent("WindowLevelEvent")
    
    def WindowLevelWheelBackward(self):
        size = self.View.RenderWindow.GetSize()
        dy = -4.0*float(self.GetMouseWheelMotionFactor())/size[1]
        self.WindowStep = 0.0
        self.SetLevelStep = dy
        self.InvokeEvent("WindowLevelEvent")
    
    def OnMouseWheelForward(self):
        x,y = self.Interactor.GetEventPosition()
        factor = 0.0
        self.FindPokedRenderer(x,y)
        self.CurrentRenderer = self.GetCurrentRenderer()
        if not self.CurrentRenderer:
            return
        style =  self.View.WheelInteractionStyle
        if style == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
            self.StartWindowLevel()
            self.WindowLevelWheelForward()
            self.EndWindowLevel()
        elif style == vtkViewImage2D.SELECT_INTERACTION:
            self.StartZSliceMove()
            self.ZSliceWheelForward()
            self.EndZSliceMove()
        elif style == vtkViewImage2D.FULL_PAGE_INTERACTION:
            pass
        elif style == vtkViewImage2D.MEASURE_INTERACTION:
            pass
        elif style == vtkViewImage2D.ZOOM_INTERACTION:
            self.StartDolly()
            factor = 10.0*0.2*self.GetMouseWheelMotionFactor()
            self.View.SyncSetZoom(math.pow(1.1, factor)*self.View.Zoom)
            self.EndDolly()
        else:
            pass
        
    def OnMouseWheelBackward(self):
        x,y = self.Interactor.GetEventPosition()
        factor = 0.0
        self.FindPokedRenderer(x,y)
        self.CurrentRenderer = self.GetCurrentRenderer()
        if not self.CurrentRenderer:
            return
        style =  self.View.WheelInteractionStyle
        if style == vtkViewImage2D.WINDOW_LEVEL_INTERACTION:
            self.StartWindowLevel()
            self.WindowLevelWheelBackward()
            self.EndWindowLevel()
        elif style == vtkViewImage2D.SELECT_INTERACTION:
            self.StartZSliceMove()
            self.ZSliceWheelBackward()
            self.EndZSliceMove()
        elif style == vtkViewImage2D.FULL_PAGE_INTERACTION:
            pass
        elif style == vtkViewImage2D.MEASURE_INTERACTION:
            pass
        elif style == vtkViewImage2D.ZOOM_INTERACTION:
            self.StartDolly()
            factor = 10.0*-0.2*self.GetMouseWheelMotionFactor()
            self.View.SyncSetZoom(math.pow(1.1, factor)*self.View.Zoom)
            self.EndDolly()
        else:
            pass
    
    def GetWindowStep(self):
        return self.WindowStep
    
    def SetWindowStep(self, step):
        self.WindowStep = step
    
    def GetLevelStep(self):
        return self.LevelStep
    
    def SetLevelStep(self, step):
        self.LevelStep = step
        
    def GetZSliceStep(self):
        return self.ZSliceStep
    
    def SetZSliceStep(self, step):
        self.ZSliceStep = step
    

        
        
if __name__ == "__main__":
    x = vtkInteractorStyleImage2D()
    
    x.WindowLevelCurrentPosition = [1.0,2.0]
    print x.WindowLevelStartPosition