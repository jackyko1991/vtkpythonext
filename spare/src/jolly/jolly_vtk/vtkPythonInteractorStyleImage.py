# -*- coding:utf-8 -*-
"""
Created on 2009-10-12

@author: summit

 vtkPythonInteractorStyleImage allows the user to interactively manipulate
 (rotate, pan, zoomm etc.) the camera. vtkInteractorStyleImage is specially
 designed to work with images that are being rendered with
 vtkImageActor. Several events are overloaded from its superclass
 vtkInteractorStyle, hence the mouse bindings are different. (The bindings
 keep the camera's view plane normal perpendicular to the x-y plane.) In
 summary the mouse events are as follows:
 + Left Mouse button triggers window level events
 + CTRL Left Mouse spins the camera around its view plane normal
 + SHIFT Left Mouse pans the camera
 + CTRL SHIFT Left Mouse dollys (a positional zoom) the camera
 + Middle mouse button pans the camera
 + Right mouse button dollys the camera.
 + SHIFT Right Mouse triggers pick events
 
"""

from jolly.jolly_vtk.vtkPythonInteractorStyleTrackballCamera import *

class vtkPythonInteractorStyleImage(vtkPythonInteractorStyleTrackballCamera):
    
    VTKIS_WINDOW_LEVEL = 1024
    VTKIS_PICK = 1025
    
    def __init__(self):
        vtkPythonInteractorStyleTrackballCamera.__init__(self)
        
        self.WindowLevelStartPosition = [0, 0]
        self.WindowLevelCurrentPosition = [0, 0]
        
    #===========================================================================
    # Description:
    #    Some useful information for handling window level
    #===========================================================================
    def GetWindowLevelStartPosition(self):
        return self.WindowLevelStartPosition
    
    def GetWindowLevelCurrentPosition(self):
        return self.WindowLevelCurrentPosition
    
    #===========================================================================
    # Description:
    #    Event bindings controlling the effects of pressing mouse buttons
    #    or moving the mouse.
    #===========================================================================
    def OnMouseMove(self):
        x, y = self.Interactor.GetEventPosition()
        
        if self.State == self.VTKIS_WINDOW_LEVEL:
            self.FindPokedRenderer(x, y)
            self.WindowLevel()
            self.InvokeEvent("InteractionEvent")
        elif self.State == self.VTKIS_PICK:
            self.FindPokedRenderer(x, y)
            self.Pick()
            self.InvokeEvent("InteractionEvent")
        else:
            pass
        
        # Call parent to handle all other states and perform additional work
        vtkPythonInteractorStyleTrackballCamera.OnMouseMove(self)
        
    
    def OnLeftButtonDown(self):
        x, y = self.Interactor.GetEventPosition()
        self.FindPokedRenderer(x, y)
        if self.CurrentRenderer == None:
            return
        
        # Redefine this button to handle windwo/level
        self.GrabFocus(self.EventCallbackCommand)
        if (not self.Interactor.GetShiftKey() and not self.Interactor.GetControlKey()):
            self.WindowLevelStartPosition[0] = x
            self.WindowLevelStartPosition[1] = y
            self.StartWindowLevel()
        
        # The rest of the button+key combinations remain the same
        else:
            vtkPythonInteractorStyleTrackballCamera.OnLeftButtonDown(self)
    
    def OnLeftButtonUp(self):
        if self.State == self.VTKIS_WINDOW_LEVEL:
            self.EndWindowLevel()
            if self.Interactor:
                self.ReleaseFocus()
        
        # Call parent to handle all other states and perform additional work
        vtkPythonInteractorStyleTrackballCamera.OnLeftButtonUp(self)
    
    def OnRightButtonDown(self):
        x, y = self.Interactor.GetEventPosition()
        
        self.FindPokedRenderer(x, y)
        if self.CurrentRenderer == None:
            return
        
        # Redefine this button + shift to handle pick
        self.GrabFocus(self.EventCallbackCommand)
        if self.Interactor.GetShiftKey():
            self.StartPick()
        # The rest of the button + key combinations remain the same
        else:
            vtkPythonInteractorStyleTrackballCamera.OnRightButtonDown(self)
            
    
    def OnRightButtonUp(self):
        if self.State == self.VTKIS_PICK:
            self.EndPick()
            if self.Interactor:
                self.ReleaseFocus()
        
        # Call parent to handle all other states and perform additional work
        vtkPythonInteractorStyleTrackballCamera.OnRightButtonUp(self)
    
    #===========================================================================
    # Description:
    #     Override the "fly-to" (f keypress) for images.
    #===========================================================================
    def OnChar(self):
        rwi = self.Interactor
        keyCode = rwi.GetKeyCode()
        
        if keyCode in ['f', 'F']:
            self.AnimState = self.VTKIS_ANIM_ON
            path = None
            self.FindPokedRenderer(rwi.GetEventPosition()[0], 
                                   rwi.GetEventPosition()[1])
            rwi.GetPicker().Pick(rwi.GetEventPosition()[0], 
                                   rwi.GetEventPosition()[1], 0.0,
                                   self.CurrentRenderer)
            picker = rwi.GetPicker()
            if picker<>None:
                path = picker.GetPath()
            if path <> None:
                rwi.FlyToImage(self.CurrentRenderer, picker.GetPickPosition()[0],
                                picker.GetPickPosition()[1])
            self.AnimState = self.VTKIS_ANIM_OFF
        elif keyCode in ['r', 'R']:
            # Allow either shift/ctrl to trigger the usual 'r' binding
            # otherwise trigger reset window level event
            if rwi.GetShiftKey() or rwi.GetControlKey():
                vtkPythonInteractorStyleTrackballCamera.OnChar(self)
            else:
                self.InvokeEvent("ResetWindowLevelEvent")
        else:
            vtkPythonInteractorStyleTrackballCamera.OnChar(self)
            
                
    
    #===========================================================================
    # These methods for the different interactions in different modes
    # are overridden in subclasses to perform the correct motion. Since
    # they might be called from OnTimer, they do not have mouse coord parameters
    # (use interactor's GetEventPosition and GetLastEventPosition)
    #===========================================================================
    def WindowLevel(self):
        rwi = self.Interactor
        self.WindowLevelCurrentPosition = rwi.GetEventPosition()
        
        self.InvokeEvent("WindowLevelEvent")
    
    def Pick(self):
        self.InvokeEvent("PickEvent")
    
    # Interaction mode entry points used internally.  
    def StartWindowLevel(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_WINDOW_LEVEL)
        self.InvokeEvent("StartWindowLevelEvent")
    
    def EndWindowLevel(self):
        if self.State <> self.VTKIS_WINDOW_LEVEL:
            return
        self.InvokeEvent("EndWindowLevelEvent")
        self.StopState()
        
    def StartPick(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_PICK)
        self.InvokeEvent("StartPickEvent")
    
    def EndPick(self):
        if self.State <> self.VTKIS_PICK:
            return
        self.InvokeEvent("EndPickEvent")
        self.StopState()
    
    def PrintSelf(self):
        pass
    
if __name__ == "__main__":
    def vtkAffineCallback(obj, event):
        global rep, imageActor
        Transform = vtk.vtkTransform()
        rep.GetTransform(Transform)
        
        imageActor.SetUserTransform(Transform)
        
    from vtk.util.misc import vtkGetDataRoot
    VTK_DATA_ROOT = vtkGetDataRoot()

    v16 = vtk.vtkVolume16Reader()
    v16.SetDataDimensions(64, 64)
    v16.SetDataByteOrderToLittleEndian()
    v16.SetImageRange(1, 93)
    v16.SetDataSpacing(3.2, 3.2, 1.5)
    v16.SetFilePrefix("%s/Data/headsq/quarter" % (VTK_DATA_ROOT,))
    v16.ReleaseDataFlagOn()
    v16.SetDataMask(0x7fff)
    v16.Update()
    
    range = v16.GetOutput().GetScalarRange()
    
    shifter = vtk.vtkImageShiftScale()
    shifter.SetShift(-1.0*range[0])
    shifter.SetScale(255.0/(range[1]-range[0]))
    shifter.SetOutputScalarTypeToUnsignedChar()
    shifter.SetInputConnection(v16.GetOutputPort())
    shifter.ReleaseDataFlagOff()
    shifter.Update()
    
    imageActor = vtk.vtkImageActor()
    imageActor.SetInput(shifter.GetOutput())
    imageActor.VisibilityOn()
    imageActor.SetDisplayExtent(0, 63, 0, 63, 46, 46)
    imageActor.InterpolateOff()
    
    bounds = imageActor.GetBounds()
    
    print imageActor
    
    # Create the RenderWindow, Renderer and both Actors
    ren1 = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    iren.SetInteractorStyle(None)
    style = vtkPythonInteractorStyleImage()
    #style = vtk.vtkInteractorStyleImage()
    style.SetInteractor(iren)
    
    # VTK widgets consist of two parts: the widget part that handles event processing;
    # and the widget representation that defines how the widget appears in the scene 
    # i.e., matters pertaining to geometry).
    
    rep = vtk.vtkAffineRepresentation2D()
    rep.SetBoxWidth(100)
    rep.SetCircleWidth(75)
    rep.SetAxesWidth(60)
    rep.DisplayTextOn()
    rep.PlaceWidget(bounds)
    
    widget = vtk.vtkAffineWidget()
    #widget.SetInteractor(iren)
    widget.SetRepresentation(rep)
    
    widget.AddObserver("InteractionEvent", vtkAffineCallback)
    widget.AddObserver("EndInteractionEvent", vtkAffineCallback)
    
    # Add the actors to the renderer, set the background and size
    ren1.AddActor(imageActor)
    ren1.SetBackground(0.1, 0.2, 0.4)
    renWin.SetSize(300, 300)
    
    iren.Initialize()
    renWin.Render()
    iren.Start()
    