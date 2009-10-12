# -*- coding:utf-8 -*-
"""
Created on 2009-10-6

@author: summit
"""
import vtk
import math
from vtkViewImage2D import *

class vtkViewImage2DCommand:
    def __init__(self):
        self.View = None
        self.InitialWindow = 0
        self.InitialLevel = 0
        self.WindowEventStatus = False
    
    def Execute(self,obj,event):
        if self.View.Image == None:
            return
        elif event == "KeyPressEvent":
            rwi = self.View.RenderWindow.GetInteractor()
            key = rwi.GetKeyCode()
            if (key == "i" or key == "I"):
                mode = self.View.GetInterpolationMode()
                self.View.SetInterpolationMode((mode+1)%2) 
                self.View.Render()
                return
            return
        elif event == "StartWindowLevelEvent":
            self.StartWindowing()
            return
        elif event == "EndWindowLevelEvent":
            self.EndWindowing()
            return
        elif event == "WindowLevelEvent":
            self.Windowing(obj)
            return
        elif event == "ResetWindowLevelEvent":
            self.View.ResetWindowLevel()
            self.View.SyncSetWindow(self.View.Window)
            self.View.SyncSetLevel(self.View.Level)
            self.View.Render()
            return
        elif event == "ResetPositionEvent":
            self.View.SyncResetCurrentPoint()
            self.View.Render()
            return
        elif event == "ZoomEvent":
            self.Zoom(obj)
            return
        elif event == "ResetZoomEvent":
            self.View.SyncResetZoom()
            self.View.Render()
            return
        elif event == "StartPickEvent":
            self.StartPicking(obj)
            return
        elif event == "EndPickEvent":
            self.EndPicking()
            return
        elif event == "StartMeasureEvent":
            print "StartMeasureEvent"
            return
        elif event == "MeasureEvent":
            print "MeasureEvent"
            return
        elif event == "EndMeasureEvent":
            print "EndMeasureEvent"
            return
        elif event == "StartZSliceMoveEvent":
            return
        elif event == "ZSliceMoveEvent":
            self.ChangeZSlice(obj)
            return
        elif event == "EndZSliceMoveEvent":
            return
        elif event == "FullPageEvent":
            return
        else:
            return
        
    def StartWindowing(self):
        self.InitialLevel = self.View.GetColorLevel()
        self.InitialWindow = self.View.GetColorWindow()
    
    # obj:vtkInteractorStyleImage2D
    def Windowing(self, p_isi):
        if not p_isi:
            return
        
        window = self.InitialWindow
        level = self.InitialLevel
        EPS = 0.01
        
        dx = p_isi.GetWindowStep()
        dy = p_isi.GetLevelStep()
        
        # Scale by current values
        if math.fabs(window) > EPS:
            dx = dx * window
        else:
            if window < 0:
                dx = dx * (-EPS)
            else:
                dx = dx * EPS
        if math.fabs(level) > EPS:
            dy = dy * level
        else:
            if level < 0:
                dy = dy * (-EPS)
            else:
                dy = dy * EPS
        
        # Abs so that direction does not flip
        if window < 0.0:
            dx = -1*dx
        if level < 0.0:
            dy = -1*dy
            
        # Compute new window level
        newWindow = dx + window
        newLevel = level - dy
        
        # Stay away from zero and really
        if math.fabs(newWindow) < EPS:
            if newWindow < 0:
                newWindow = -EPS
            else:
                newWindow = EPS
        if math.fabs(newLevel) < EPS:
            if newLevel < 0:
                newLevel = -EPS
            else:
                newLevel = EPS
                
        self.View.SyncSetWindow(newWindow)
        self.View.SyncSetLevel(newLevel)
        self.View.Render()
    
    def EndWindowing(self):
        pass
    
    def StartPicking(self, p_isi):
        rwi = p_isi.GetInteractor()
        path = None
        p_isi.FindPokedRenderer(rwi.GetEventPosition()[0],
                                 rwi.GetEventPosition()[1])
        rwi.GetPicker().Pick(rwi.GetEventPosition()[0], rwi.GetEventPosition()[1],
                             0.0, p_isi.GetCurrentRenderer())
        picker = rwi.GetPicker()
        if picker:
            path = picker.GetPath()
        
        if path:
            world = picker.GetPickPosition()
            pos = self.View.GetCurrentPoint()
            orientation = self.View.GetOrientation()
            conventions = self.View.GetConventions()
            
            if orientation == vtkViewImage2D.SAGITTAL_ID:
                pos[1] = world[0]  # *1.0
                pos[2] = world[1]  # *1.0
            elif orientation == vtkViewImage2D.CORONAL_ID:
                if conventions == vtkViewImage2D.RADIOLOGIC:
                    pos[0] = world[0] # *-1.0
                else:
                    pos[0] = world[0]*- 1.0
                pos[2] = world[1]
            elif orientation == vtkViewImage2D.AXIAL_ID:
                if conventions == vtkViewImage2D.RADIOLOGIC:
                    pos[0] = world[0]
                else:
                    pos[0] = world[0]*- 1.0
                pos[1] = world[1]*-1.0
            
            # Treat extrem positions
            
            for i,p in enumerate(pos):
                if p < self.View.GetWholeMinPosition(i):  
                    pos[i] = self.View.GetWholeMinPosition(i) + 0.0005
                if p > self.View.GetWholeMaxPosition(i):  
                    pos[i] = self.View.GetWholeMaxPosition(i) - 0.0005
            
            #  Set the position
            self.View.SyncSetCurrentPoint(pos)
            self.View.Render()
        
    def EndPicking(self):
        pass
    
    def ChangeZSlice(self, p_isi):
        if not p_isi:
            return
        
        p_nbSlices = p_isi.GetZSliceStep()
        current_slice = self.View.GetZSlice()
        dest_slice = current_slice + p_nbSlices
        pos = self.View.GetPositionForSlice(dest_slice, self.View.GetOrientation())
        print pos
        self.View.SyncSetPosition(pos)
        
        self.View.Render()
    
    def SetView(self, p_view):  
        self.View = p_view
    
    def Zoom(self, p_isi):
        if not p_isi:
            return
        rwi = p_isi.GetInteractor()
        p_isi.FindPokedRenderer(rwi.GetEventPosition()[0],
                                 rwi.GetEventPosition()[1])
        center = p_isi.GetCurrentRenderer().GetCenter()
        dy = rwi.GetEventPosition()[1] - rwi.GetEventPosition()[0]
        factor = 10.0 * float(dy) / float(center[1])
        self.View.SyncSetZoom(math.pow(1.1, factor)*self.View.Zoom)
        self.View.Render()
        
if __name__ == "__main__":
    pass
        