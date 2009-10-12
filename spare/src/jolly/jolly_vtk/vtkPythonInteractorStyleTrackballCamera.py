# -*- coding:utf-8 -*-
"""
Created on 2009-9-17

@author: summit

 vtkPythonInteractorStyleTrackballCamera allows the user to interactively
 manipulate (rotate, pan, etc.) the camera, the viewpoint of the scene.  In
 trackball interaction, the magnitude of the mouse motion is proportional
 to the camera motion associated with a particular mouse binding. For
 example, small left-button motions cause small changes in the rotation of
 the camera around its focal point. For a 3-button mouse, the left button
 is for rotation, the right button for zooming, the middle button for
 panning, and ctrl + left button for spinning.  (With fewer mouse buttons,
 ctrl + shift + left button is for zooming, and shift + left button is for
 panning.)
"""

import vtk
from jolly.jolly_vtk.vtkPythonInteractorStyle import *
import math

class vtkPythonInteractorStyleTrackballCamera(vtkPythonInteractorStyle):
    
    def __init__(self):
        
        vtkPythonInteractorStyle.__init__(self)
        
        self.MotionFactor = 10.0
    
    #===========================================================================
    # Description:
    # Event bindings controlling the effects of pressing mouse buttons
    # or moving the mouse.
    #===========================================================================
    def OnMouseMove(self):
        x, y = self.Interactor.GetEventPosition()
        
        if self.State == self.VTKIS_ROTATE:
            self.FindPokedRenderer(x, y)
            self.Rotate()
            self.InvokeEvent("InteractionEvent")
        elif self.State == self.VTKIS_PAN:
            self.FindPokedRenderer(x, y)
            self.Pan()
            self.InvokeEvent("InteractionEvent")
        elif self.State == self.VTKIS_DOLLY:
            self.FindPokedRenderer(x, y)
            self.Dolly()
            self.InvokeEvent("InteractionEvent")
        elif self.State == self.VTKIS_SPIN:
            self.FindPokedRenderer(x, y)
            self.Spin()
            self.InvokeEvent("InteractionEvent")
    
    def OnLeftButtonDown(self):
        self.FindPokedRenderer(self.Interactor.GetEventPosition()[0],
                               self.Interactor.GetEventPosition()[1])
        if self.CurrentRenderer == None:
            return
      
        self.GrabFocus(self.EventCallbackCommand)
        if self.Interactor.GetShiftKey():
            if self.Interactor.GetControlKey():
                self.StartDolly()
            else:
                self.StartPan()
        else:
            if self.Interactor.GetControlKey():
                self.StartSpin()
            else:
                self.StartRotate()
    
    def OnLeftButtonUp(self):
        if self.State == self.VTKIS_DOLLY:
            self.EndDolly()
        elif self.State == self.VTKIS_PAN:
            self.EndPan()
        elif self.State == self.VTKIS_SPIN:
            self.EndSpin()
        elif self.State == self.VTKIS_ROTATE:
            self.EndRotate()
        else:
            pass
        if self.Interactor <> None:
            self.ReleaseFocus()
    
    def OnMiddleButtonDown(self):
        self.FindPokedRenderer(self.Interactor.GetEventPosition()[0],
                               self.Interactor.GetEventPosition()[1])
        if self.CurrentRenderer == None:
            return
        self.GrabFocus(self.EventCallbackCommand)
        self.StartPan()
    
    def OnMiddleButtonUp(self):
        if self.State == self.VTKIS_PAN:
            self.EndPan()
            if self.Interactor <> None:
                self.ReleaseFocus()
    
    def OnRightButtonDown(self):
        self.FindPokedRenderer(self.Interactor.GetEventPosition()[0],
                               self.Interactor.GetEventPosition()[1])
        if self.CurrentRenderer == None:
            return
        self.GrabFocus(self.EventCallbackCommand)
        self.StartDolly()
    
    def OnRightButtonUp(self):
        if self.State == self.VTKIS_DOLLY:
            self.EndDolly()
            if self.Interactor <> None:
                self.ReleaseFocus()
    
    def OnMouseWheelForward(self):
        self.FindPokedRenderer(self.Interactor.GetEventPosition()[0],
                               self.Interactor.GetEventPosition()[1])
        if self.CurrentRenderer == None:
            return
        self.GrabFocus(self.EventCallbackCommand)
        self.StartDolly()
        factor = self.MotionFactor*0.2*self.MouseWheelMotionFactor
        self.Dolly2(math.pow(1.1, factor))
        self.EndDolly()
        self.ReleaseFocus()
    
    def OnMouseWheelBackward(self):
        self.FindPokedRenderer(self.Interactor.GetEventPosition()[0],
                               self.Interactor.GetEventPosition()[1])
        if self.CurrentRenderer == None:
            return
        self.GrabFocus(self.EventCallbackCommand)
        self.StartDolly()
        factor = self.MotionFactor*-0.2*self.MouseWheelMotionFactor
        self.Dolly2(math.pow(1.1, factor))
        self.EndDolly()
        self.ReleaseFocus()
    
    #===========================================================================
    # These methods for the different interactions in different modes
    # are overridden in subclasses to perform the correct motion. Since
    # they are called by OnTimer, they do not have mouse coord parameters
    # (use interactor's GetEventPosition and GetLastEventPosition)
    #===========================================================================
    def Rotate(self):
        if self.CurrentRenderer == None:
            return
        
        rwi = self.Interactor
        
        dx = rwi.GetEventPosition()[0] - rwi.GetLastEventPosition()[0]
        dy = rwi.GetEventPosition()[1] - rwi.GetLastEventPosition()[1]
        
        size = self.CurrentRenderer.GetRenderWindow().GetSize()
        
        delta_elevation = -20.0/size[1]
        delta_azimuth = -20.0/size[0]
        
        rxf = dx*delta_azimuth*self.MotionFactor
        ryf = dy*delta_elevation*self.MotionFactor
        
        camera = self.CurrentRenderer.GetActiveCamera()
        camera.Azimuth(rxf)
        camera.Elevation(ryf)
        camera.OrthogonalizeViewUp()
        
        if self.AutoAdjustCameraClippingRange:
            self.CurrentRenderer.ResetCameraClippingRange()
        if rwi.GetLightFollowCamera():
            self.CurrentRenderer.UpdateLightsGeometryToFollowCamera()
        
        rwi.Render()
    
    def Spin(self):
        if self.CurrentRenderer == None:
            return 
        rwi = self.Interactor
        center = self.CurrentRenderer.GetCenter()
        
        newAngle = vtk.vtkMath.DegreesFromRadians(math.atan2(rwi.GetEventPosition()[1]-center[1],
                                                        rwi.GetEventPosition()[0]-center[0]
                                                        ))
        oldAngle = vtk.vtkMath.DegreesFromRadians(math.atan2(rwi.GetLastEventPosition()[1]-center[1],
                                                        rwi.GetLastEventPosition()[0]-center[0]
                                                        ))
        camera = self.CurrentRenderer.GetActiveCamera()
        camera.Roll(newAngle - oldAngle)
        camera.OrthogonalizeViewUp()
        
        rwi.Render()
    
    def Pan(self):
        if self.CurrentRenderer == None:
            return
        
        rwi = self.Interactor
        viewFocus = [0.0]*4
        newPickPoint = [0.0]*4
        oldPickPoint = [0.0]*4
        motionVector = [0.0]*3
        
        camera = self.CurrentRenderer.GetActiveCamera()
        viewFocus = camera.GetFocalPoint()
        self.ComputeWorldToDisplay(viewFocus[0], viewFocus[1], viewFocus[2], viewFocus)
        
        focalDepth = viewFocus[2]
        
        newPickPoint = self.ComputeDisplayToWorld(rwi.GetEventPosition()[0], 
                                   rwi.GetEventPosition()[1], focalDepth, newPickPoint)
        
        # Has to recalc old mouse point since the viewport has moved,
        # so can't move it outside the loop
        oldPickPoint = self.ComputeDisplayToWorld(rwi.GetLastEventPosition()[0], 
                                   rwi.GetLastEventPosition()[1], focalDepth, oldPickPoint)
        
        
        
        # Camera motion is reversed
        motionVector[0] = oldPickPoint[0] - newPickPoint[0]
        motionVector[1] = oldPickPoint[1] - newPickPoint[1]
        motionVector[2] = oldPickPoint[2] - newPickPoint[2]
        
        viewFocus = camera.GetFocalPoint()
        viewPoint = camera.GetPosition()
        camera.SetFocalPoint(motionVector[0]+viewFocus[0],
                             motionVector[1]+viewFocus[1],
                             motionVector[2]+viewFocus[2])
        camera.SetPosition(motionVector[0]+viewPoint[0],
                           motionVector[1]+viewPoint[1],
                           motionVector[2]+viewPoint[2])
        if rwi.GetLightFollowCamera():
            self.CurrentRenderer.UpdateLightsGeometryToFollowCamera()
        rwi.Render()
        
    def Dolly(self):
        if self.CurrentRenderer == None:
            return
        
        rwi = self.Interactor
        center = self.CurrentRenderer.GetCenter()
        dy = rwi.GetEventPosition()[1] - rwi.GetLastEventPosition()[1]
        dyf = self.MotionFactor * dy / center[1]
        
        self.Dolly2(math.pow(1.1, dyf))
        
    
    #===========================================================================
    # Description:
    #    Set the apparent sensitivity of the interactor style to mouse motion.
    #===========================================================================
    def SetMotionFactor(self, MotionFactor):
        self.MotionFactor = MotionFactor
        
    def GetMotionFactor(self):
        return self.MotionFactor

    def Dolly2(self, factor):
        if self.CurrentRenderer == None:
            return
        camera = self.CurrentRenderer.GetActiveCamera()
        if camera.GetParallelProjection():
            camera.SetParallelScale(camera.GetParallelScale()/factor)
        else:
            camera.Dolly(factor)
            if self.AutoAdjustCameraClippingRange:
                self.CurrentRenderer.ResetCameraClippingRange()
        if self.Interactor.GetLightFollowCamera():
            self.CurrentRenderer.UpdateLightsGeometryToFollowCamera()
        self.Interactor.Render()
    
    def PrintSelf(self):
        pass

if __name__=="__main__":
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
    style = vtkPythonInteractorStyleTrackballCamera()
    style.SetInteractor(iren)   # and style => Interactor but not Interactor set style
    iren.SetInteractorStyle(None)
    #iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera()) # Set None 
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
    
    
#    style.AddObserver("LeftButtonPressEvent", ButtonEvent)
#    style.AddObserver("LeftButtonReleaseEvent", ButtonEvent)
#    style.AddObserver("MiddleButtonPressEvent", ButtonEvent)
#    style.AddObserver("MiddleButtonReleaseEvent", ButtonEvent)
#    style.AddObserver("RightButtonPressEvent", ButtonEvent)
#    style.AddObserver("RightButtonReleaseEvent", ButtonEvent)
#    style.AddObserver("MouseMoveEvent", MouseMove)
#    style.AddObserver("KeyPressEvent", Keypress)
    print dir(vtk.vtkObject)
    
    iren.Initialize()
    renWin.Render()
    iren.Start()