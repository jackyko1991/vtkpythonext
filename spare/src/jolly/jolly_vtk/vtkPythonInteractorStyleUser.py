# -*- coding:utf-8 -*-
"""
Created on 2009-9-17

@author: summit
"""

import vtk
from jolly.jolly_vtk.vtkPythonInteractorStyle import *

class vtkPythonInteractorStyleUser(vtkPythonInteractorStyle):
    VTKIS_USERINTERACTION = 8
    
    def __init__(self):
        vtkPythonInteractorStyle.__init__(self)
        # Tell the parent class not to handle observers
        # that has to be done here
        self.HandleObserversOff()
        self.LastPos = [0.0, 0.0]
        self.OldPos = [0.0, 0.0]
        
        self.ShiftKey = 0
        self.CtrlKey = 0
        self.Char = ""
        self.KeySym = ""
        self.Button = 0
    
    #===========================================================================
    # Description:
    #   Get the most recent mouse position during mouse motion.  
    #   In your user interaction method, you must use this to track
    #   the mouse movement.  Do not use GetEventPosition(), which records
    #   the last position where a mouse button was pressed.
    #===========================================================================
    def GetLastPos(self):
        return self.LastPos
    
    #===========================================================================
    # Description:
    #   Get the previous mouse position during mouse motion, or after
    #   a key press.  This can be used to calculate the relative 
    #   displacement of the mouse.
    #===========================================================================
    def GetOldPos(self):
        return self.OldPos
    
    #===========================================================================
    # Description:
    #    Test whether modifiers were held down when mouse button or key
    #    was pressed
    #===========================================================================
    def GetShiftKey(self):
        return self.ShiftKey
    
    def GetCtrlKey(self):
        return self.CtrlKey
    
    #===========================================================================
    # Description:
    #    Get the character for a Char event.
    #===========================================================================
    def GetChar(self):
        return self.Char
    
    #===========================================================================
    # Description:
    #    Get the KeySym (in the same format as Tk KeySyms) for a 
    #    KeyPress or KeyRelease method.
    #===========================================================================
    def GetKeySym(self):
        return self.KeySym
    
    #===========================================================================
    # Description:
    #    Get the mouse button that was last pressed inside the window
    #    (returns zero when the button is released).
    #===========================================================================
    def GetButton(self):
        return self.Button
    
    #===========================================================================
    # Description:
    #    Generic event bindings
    #===========================================================================
    def OnMouseMove(self):
        vtkPythonInteractorStyle.OnMouseMove(self)
        x, y = self.Interactor.GetEventPosition()
        self.ShiftKey = self.Interactor.GetShiftKey()
        self.CtrlKey = self.Interactor.GetControlKey()
        self.LastPos[0] = x
        self.LastPos[1] = y
        
        if self.HasObserver("MouseMoveEvent"):
            self.InvokeEvent("MouseMoveEvent")
        self.OldPos[0] = x
        self.OldPos[1] = y
        
    
    def OnLeftButtonDown(self):
        self.Button = 1
        if self.HasObserver("LeftButtonPressEvent"):
            x, y = self.Interactor.GetEventPosition()
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.LastPos[0] = x
            self.LastPos[1] = y
            self.InvokeEvent("LeftButtonPressEvent")
            self.OldPos[0] = x
            self.OldPos[1] = y
        else:
            vtkPythonInteractorStyle.OnLeftButtonDown(self)
    
    def OnLeftButtonUp(self):
        if self.HasObserver("LeftButtonReleaseEvent"):
            x, y = self.Interactor.GetEventPosition()
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.LastPos[0] = x
            self.LastPos[1] = y
            self.InvokeEvent("LeftButtonReleaseEvent")
            self.OldPos[0] = x
            self.OldPos[1] = y
        else:
            vtkPythonInteractorStyle.OnLeftButtonUp(self)
        if self.Button == 1:
            self.Button = 0
    
    def OnMiddleButtonDown(self):
        self.Button = 2
        if self.HasObserver("MiddleButtonPressEvent"):
            x, y = self.Interactor.GetEventPosition()
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.LastPos[0] = x
            self.LastPos[1] = y
            self.InvokeEvent("MiddleButtonPressEvent")
            self.OldPos[0] = x
            self.OldPos[1] = y
        else:
            vtkPythonInteractorStyle.OnMiddleButtonDown(self)
    
    def OnMiddleButtonUp(self):
        if self.HasObserver("MiddleButtonReleaseEvent"):
            x, y = self.Interactor.GetEventPosition()
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.LastPos[0] = x
            self.LastPos[1] = y
            self.InvokeEvent("MiddleButtonReleaseEvent")
            self.OldPos[0] = x
            self.OldPos[1] = y
        else:
            vtkPythonInteractorStyle.OnMiddleButtonUp(self)
        if self.Button == 2:
            self.Button = 0
    
    def OnRightButtonDown(self):
        self.Button = 3
        if self.HasObserver("RightButtonPressEvent"):
            x, y = self.Interactor.GetEventPosition()
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.LastPos[0] = x
            self.LastPos[1] = y
            self.InvokeEvent("RightButtonPressEvent")
            self.OldPos[0] = x
            self.OldPos[1] = y
        else:
            vtkPythonInteractorStyle.OnRightButtonDown(self)
    
    def OnRightButtonUp(self):
        if self.HasObserver("RightButtonReleaseEvent"):
            x, y = self.Interactor.GetEventPosition()
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.LastPos[0] = x
            self.LastPos[1] = y
            self.InvokeEvent("RightButtonReleaseEvent")
            self.OldPos[0] = x
            self.OldPos[1] = y
        else:
            vtkPythonInteractorStyle.OnRightButtonUp(self)
        if self.Button == 3:
            self.Button = 0
            
        
    #==========================================================================
    # Description:
    #   Keyboard functions
    #==========================================================================
    def OnChar(self):
        if self.HasObserver("CharEvent"):
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.Char = self.Interactor.GetKeyCode()
            self.InvokeEvent("CharEvent")
    
    def OnKeyPress(self):
        if self.HasObserver("KeyPressEvent"):
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.KeySym = self.Interactor.GetKeySym()
            self.Char = self.Interactor.GetKeyCode()
            self.InvokeEvent("KeyPressEvent")
    
    def OnKeyRelease(self):
        if self.HasObserver("KeyReleaseEvent"):
            self.ShiftKey = self.Interactor.GetShiftKey()
            self.CtrlKey = self.Interactor.GetControlKey()
            self.KeySym = self.Interactor.GetKeySym()
            self.Char = self.Interactor.GetKeyCode()
            self.InvokeEvent("KeyReleaseEvent")
    
    #==========================================================================
    # Description:
    #    These are more esoteric events, but are useful in some cases.
    #==========================================================================
    def OnExpose(self):
        if self.HasObserver("ExposeEvent"):
            self.InvokeEvent("ExposeEvent")
    
    def OnConfigure(self):
        if self.HasObserver("ConfigureEvent"):
            self.InvokeEvent("ConfigureEvent")
    
    def OnEnter(self):
        if self.HasObserver("ConfigureEvent"):
            self.LastPos = self.Interactor.GetEventPosition()
            self.InvokeEvent("EnterEvent")
    
    def OnLeave(self):
        if self.HasObserver("ConfigureEvent"):
            self.LastPos = self.Interactor.GetEventPosition()
            self.InvokeEvent("LeaveEvent")
    
    def OnTimer(self):
        if self.HasObserver("TimeEvent"):
            self.InvokeEvent("TimeEvent") # calldata TimeId
        if self.State == self.VTKIS_USERINTERACTION:
            if self.HasObserver("UserEvent"):
                self.InvokeEvent("UserEvent")
                self.OldPos = self.LastPos
                if self.UseTimers:
                    self.Interactor.ResetTimer(self.TimerId)
        
        elif (not self.HasObserver("MouseMoveEvent") and (self.Button == 0 or
                (self.HasObserver("LeftButtonPressEvent") and self.Button==1) or
                (self.HasObserver("MiddleButtonPressEvent") and self.Button==2) or
                (self.HasObserver("RightButtonPressEvent") and self.Button==3))):                                         
            vtkPythonInteractorStyle.OnTimer(self)
        elif self.HasObserver("TimerEvent"):
            if self.UseTimers:
                self.Interactor.ResetTimer(self.TimerId)
    
    def PrintSelf(self):
        pass
    

if __name__ == "__main__":
    import sys
    # We create an instance of vtkConeSource and set some of its
    # properties. The instance of vtkConeSource "cone" is part of a
    # visualization pipeline (it is a source process object); it produces
    # data (output type is vtkPolyData) which other filters may process.
    cone = vtk.vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)
    
    # In this example we terminate the pipeline with a mapper process
    # object.  (Intermediate filters such as vtkShrinkPolyData could be
    # inserted in between the source and the mapper.)  We create an
    # instance of vtkPolyDataMapper to map the polygonal data into
    # graphics primitives. We connect the output of the cone souece to the
    # input of this mapper.
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())
    
    # Create an actor to represent the cone. The actor orchestrates
    # rendering of the mapper's graphics primitives. An actor also refers
    # to properties via a vtkProperty instance, and includes an internal
    # transformation matrix. We set this actor's mapper to be coneMapper
    # which we created above.
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    
    # Create the Renderer and assign actors to it. A renderer is like a
    # viewport. It is part or all of a window on the screen and it is
    # responsible for drawing the actors it has.  We also set the
    # background color here.
    ren = vtk.vtkRenderer()
    ren.AddActor(coneActor)
    ren.SetBackground(0.1, 0.2, 0.4)
    
    # Finally we create the render window which will show up on the screen
    # We put our renderer into the render window using AddRenderer. We
    # also set the size to be 300 pixels by 300.
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(300, 300)
    
    # Define custom interaction.
    iren = vtk.vtkRenderWindowInteractor()
    style = vtkPythonInteractorStyleUser()
    style.SetInteractor(iren)   # and style => Interactor but not Interactor set style
    iren.SetInteractorStyle(None) # Set None 
    iren.SetRenderWindow(renWin)
    
    # Add the observers to watch for particular events. These invoke
    # Python functions.
    Rotating = 0
    Panning = 0
    Zooming = 0
    
    # Handle the mouse button events.
    def ButtonEvent(obj, event):
        global Rotating, Panning, Zooming
        if event == "LeftButtonPressEvent":
            Rotating = 1
        elif event == "LeftButtonReleaseEvent":
            Rotating = 0
        elif event == "MiddleButtonPressEvent":
            Panning = 1
        elif event == "MiddleButtonReleaseEvent":
            Panning = 0
        elif event == "RightButtonPressEvent":
            Zooming = 1
        elif event == "RightButtonReleaseEvent":
            Zooming = 0
    
    # General high-level logic
    def MouseMove(obj, event):
        global Rotating, Panning, Zooming
        global iren, renWin, ren
        lastXYpos = iren.GetLastEventPosition()
        lastX = lastXYpos[0]
        lastY = lastXYpos[1]
    
        xypos = iren.GetEventPosition()
        x = xypos[0]
        y = xypos[1]
    
        center = renWin.GetSize()
        centerX = center[0]/2.0
        centerY = center[1]/2.0
    
        if Rotating:
            Rotate(ren, ren.GetActiveCamera(), x, y, lastX, lastY,
                   centerX, centerY)
        elif Panning:
            Pan(ren, ren.GetActiveCamera(), x, y, lastX, lastY, centerX,
                centerY)
        elif Zooming:
            Dolly(ren, ren.GetActiveCamera(), x, y, lastX, lastY,
                  centerX, centerY)
      
    
    def Keypress(obj, event):
        key = obj.GetKeySym()
        print key
        if key == "e":
            obj.InvokeEvent("DeleteAllObjects")
            sys.exit()
        elif key == "w":
            Wireframe()
        elif key =="s":
            Surface() 
     
    
    # Routines that translate the events into camera motions.
    
    # This one is associated with the left mouse button. It translates x
    # and y relative motions into camera azimuth and elevation commands.
    def Rotate(renderer, camera, x, y, lastX, lastY, centerX, centerY):    
        camera.Azimuth(lastX-x)
        camera.Elevation(lastY-y)
        camera.OrthogonalizeViewUp()
        renWin.Render()
    
    
    # Pan translates x-y motion into translation of the focal point and
    # position.
    def Pan(renderer, camera, x, y, lastX, lastY, centerX, centerY):
        FPoint = camera.GetFocalPoint()
        FPoint0 = FPoint[0]
        FPoint1 = FPoint[1]
        FPoint2 = FPoint[2]
    
        PPoint = camera.GetPosition()
        PPoint0 = PPoint[0]
        PPoint1 = PPoint[1]
        PPoint2 = PPoint[2]
    
        renderer.SetWorldPoint(FPoint0, FPoint1, FPoint2, 1.0)
        renderer.WorldToDisplay()
        DPoint = renderer.GetDisplayPoint()
        focalDepth = DPoint[2]
    
        APoint0 = centerX+(x-lastX)
        APoint1 = centerY+(y-lastY)
        
        renderer.SetDisplayPoint(APoint0, APoint1, focalDepth)
        renderer.DisplayToWorld()
        RPoint = renderer.GetWorldPoint()
        RPoint0 = RPoint[0]
        RPoint1 = RPoint[1]
        RPoint2 = RPoint[2]
        RPoint3 = RPoint[3]
        
        if RPoint3 != 0.0:
            RPoint0 = RPoint0/RPoint3
            RPoint1 = RPoint1/RPoint3
            RPoint2 = RPoint2/RPoint3
    
        camera.SetFocalPoint( (FPoint0-RPoint0)/2.0 + FPoint0,
                              (FPoint1-RPoint1)/2.0 + FPoint1,
                              (FPoint2-RPoint2)/2.0 + FPoint2)
        camera.SetPosition( (FPoint0-RPoint0)/2.0 + PPoint0,
                            (FPoint1-RPoint1)/2.0 + PPoint1,
                            (FPoint2-RPoint2)/2.0 + PPoint2)
        renWin.Render()
     
    
    # Dolly converts y-motion into a camera dolly commands.
    def Dolly(renderer, camera, x, y, lastX, lastY, centerX, centerY):
        dollyFactor = pow(1.02,(0.5*(y-lastY)))
        if camera.GetParallelProjection():
            parallelScale = camera.GetParallelScale()*dollyFactor
            camera.SetParallelScale(parallelScale)
        else:
            camera.Dolly(dollyFactor)
            renderer.ResetCameraClippingRange()
    
        renWin.Render() 
    
    # Wireframe sets the representation of all actors to wireframe.
    def Wireframe():
        actors = ren.GetActors()
        actors.InitTraversal()
        actor = actors.GetNextItem()
        while actor:
            actor.GetProperty().SetRepresentationToWireframe()
            actor = actors.GetNextItem()
    
        renWin.Render() 
    
    # Surface sets the representation of all actors to surface.
    def Surface():
        actors = ren.GetActors()
        actors.InitTraversal()
        actor = actors.GetNextItem()
        while actor:
            actor.GetProperty().SetRepresentationToSurface()
            actor = actors.GetNextItem()
        renWin.Render()
    
    
    style.AddObserver("LeftButtonPressEvent", ButtonEvent)
    style.AddObserver("LeftButtonReleaseEvent", ButtonEvent)
    style.AddObserver("MiddleButtonPressEvent", ButtonEvent)
    style.AddObserver("MiddleButtonReleaseEvent", ButtonEvent)
    style.AddObserver("RightButtonPressEvent", ButtonEvent)
    style.AddObserver("RightButtonReleaseEvent", ButtonEvent)
    style.AddObserver("MouseMoveEvent", MouseMove)
    style.AddObserver("KeyPressEvent", Keypress)
    
    
    iren.Initialize()
    renWin.Render()
    iren.Start()  