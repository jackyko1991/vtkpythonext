# -*- coding:utf-8 -*-
"""
Created on 2009-9-17

@author: summit

vtkPythonInteractorStyle is a base class implementing the majority of motion 
control rounts and defines an event driven interface to support vtkRenderWindowIntertor
Because it's not exsit a vtk class support python to add customize the interaction,
we rewrite a new python class.
"""
import vtk
from jolly.jolly_vtk2.vtkPythonInteractorObserver import *

class vtkPythonInteractorStyle(vtkPythonInteractorObserver):
    VTKIS_START = 0
    VTKIS_NONE = 0
    VTKIS_ROTATE = 1
    VTKIS_PAN = 2
    VTKIS_SPIN = 3
    VTKIS_DOLLY = 4
    VTKIS_ZOOM = 5
    VTKIS_USCALE = 6
    VTKIS_TIMER = 7
    VTKIS_FORWARDFLY = 8
    VTKIS_REVERSEFLY = 9
    VTKIS_ANIM_OFF = 0
    VTKIS_ANIM_ON = 1
    
    def __init__(self):
        vtkPythonInteractorObserver.__init__(self)
        
        # Keep track of current state
        self.State = self.VTKIS_NONE
        self.AnimState = self.VTKIS_ANIM_OFF
        
        # Should observers be handled here, should we fire timers
        self.HandleObservers = 1
        self.UseTimers = 0
        self.TimerId = 1# keep track of the timers that are created/destroyed
        
        self.AutoAdjustCameraClippingRange = 1
        
        self.Interactor = None
        self.EventCallbackCommand = lambda obj, event: self.ProcessEvents(obj, 
                                                                        event,
                                                                        self,
                                                                        None)
        
        # These widgets are not activated with a key
        self.KeyPressActivation = 0
        
        # For picking and highlighting props
        self.Outline = vtk.vtkOutlineSource()
        self.OutlineMapper = vtk.vtkPolyDataMapper()
        self.OutlineActor = None
        
        self.OutlineMapper.SetInput(self.Outline.GetOutput())
        
        
        self.PickedRenderer = None
        self.CurrentProp = None
        self.PickedActor2D = None
        # bool: prop picked?
        self.PropPicked = 0
        # support 2D picking
        self.PickColor = [1.0, 0.0, 0.0]
        self.MouseWheelMotionFactor = 1.0
        
        # Control the timer duration in milliseconds
        self.TimerDuration = 10
        
        # Forward evets to the RenderWindowInteractor
        self.EventForwarder = None
        
       
        
    #==========================================================================
    # Description:
    # Set/Get the Interactor wrapper being controlled by this object.
    # (Satisfy superclass API.)
    #==========================================================================
    def SetInteractor(self, Interactor):
        if Interactor == self.Interactor:
            return
        
        # if we already have an Interactor then stop observing it
        if self.Interactor <> None:
            self.Interactor.RemoveObserver(self.EventCallbackCommand)
        self.Interactor = Interactor
        
        # add observers for each of the events handled in ProcessEvents
        if Interactor:
            Interactor.AddObserver("EnterEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("LeaveEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("MouseMoveEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("LeftButtonPressEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("LeftButtonReleaseEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("MiddleButtonPressEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("MiddleButtonReleaseEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("RightButtonPressEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("RightButtonReleaseEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("MouseWheelForwardEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("MouseWheelBackwardEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("ExposeEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("ConfigureEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("TimerEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("KeyPressEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("KeyReleaseEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("CharEvent", self.EventCallbackCommand,
                                   self.Priority)
            Interactor.AddObserver("DeleteEvent", self.EventCallbackCommand,
                                   self.Priority)
        if self.EventForwarder <> None:
            self.EventForwarder.SetTarget(self.Interactor)
        if self.Interactor:
            self.AddObserver("StartInteractionEvent", self.EventForwarder)
            self.AddObserver("EndInteractionEvent", self.EventForwarder)
        else:
            self.RemoveObserver(self.EventForwarder)
            
            
    
    #==========================================================================
    # Description:
    #  Turn onoff this interactor. Interactor styles operate a little
    #  bit differently than other types of interactor observers. When
    #  the SetInteractor() method is invoked, the automatically enable
    #  themselves. This is a legacy requirement, and convenient for the
    #  user.
    #==========================================================================
    def SetEnabled(self, Enabled):
        if self.Interactor == None:
            raise RuntimeError, "The interactor must be set prior to enabling/disabling widget"
        if Enabled:
            print "Enabling widget"
            if self.Enabled:    # already enabled, just return
                return
            self.Enabled = 1
            self.InvokeEvent("EnableEvent")
        else:
            print "Disabling widget"
            if not self.Enabled:    # already enabled, just return
                return
            self.Enabled = 0
            self.HighlightProp(None)
            self.InvokeEvent("DisableEvent")
    
    #==========================================================================
    # Description:
    #  If AutoAdjustCameraClippingRange is on, then before each render the
    #  camera clipping range will be adjusted to "fit" the whole scene. Clipping
    #  will still occur if objects in the scene are behind the camera or
    #  come very close. If AutoAdjustCameraClippingRange is off, no adjustment
    #  will be made per render, but the camera clipping range will still
    #  be reset when the camera is reset.
    #==========================================================================
    def SetAutoAdjustCameraClippingRange(self, AutoAdjustCameraClippingRange):
        if AutoAdjustCameraClippingRange>=0 and AutoAdjustCameraClippingRange<=1:
            self.AutoAdjustCameraClippingRange = AutoAdjustCameraClippingRange
    def GetAutoAdjustCameraClippingRange(self):
        return self.AutoAdjustCameraClippingRange
    
    def AutoAdjustCameraClippingRangeOn(self):
        self.SetAutoAdjustCameraClippingRange(1)
    
    def AutoAdjustCameraClippingRangeOff(self):
        self.SetAutoAdjustCameraClippingRange(0)
    
    #===========================================================================
    # Description:
    #   When an event occurs, we must determine which Renderer the event
    #   occurred within, since one RenderWindow may contain multiple
    #   renderers. 
    #===========================================================================
    def FindPokedRenderer(self, x, y):
        self.SetCurrentRenderer(self.Interactor.FindPokedRenderer(x,y))
    
    #===========================================================================
    # Description:
    #    Some useful information for interaction
    #===========================================================================
    def GetState(self):
        return self.State
    
    #===========================================================================
    # Description:
    #    SetGet timer hint
    #===========================================================================
    def GetUseTimes(self):
        return self.UseTimes
    def SetUseTimes(self, UseTimes):
        self.UseTimes = UseTimes
    def UseTimesOn(self):
        self.SetUseTimes(1)
    def UseTimesOff(self):
        self.SetUseTimes(0)
        
    #===========================================================================
    # Description:
    #   If using timers, specify the default timer interval (in
    #   milliseconds). Care must be taken when adjusting the timer interval from
    #   the default value of 10 milliseconds--it may adversely affect the
    #   interactors.
    #===========================================================================
    def SetTimerDuration(self, TimerDuration):
        if TimerDuration>=1 and TimerDuration<=10000:
            self.TimerDuration = TimerDuration
        
    def GetTimerDuration(self):
        return self.TimerDuration
    
    #===========================================================================
    # Description:
    #    Does ProcessEvents handle observers on this class or not
    #===========================================================================
    def SetHandleObservers(self, HandleObservers):
        self.HandleObservers = HandleObservers
    def GetHandleObservers(self):
        return self.HandleObservers
    def HandleObserversOn(self):
        self.SetHandleObservers(1)
    def HandleObserversOff(self):
        self.SetHandleObservers(0)
    
    #===========================================================================
    # Description:
    #     Generic event bindings must be overridden in subclasses            
    #===========================================================================
    def OnMouseMove(self):
        pass
    
    def OnLeftButtonDown(self):
        pass
    
    def OnLeftButtonUp(self):
        pass
    
    def OnMiddleButtonDown(self):
        pass
    
    def OnMiddleButtonUp(self):
        pass
    
    def OnRightButtonDown(self):
        pass
    
    def OnRightButtonUp(self):
        pass
    
    def OnMouseWheelForward(self):
        pass
     
    def OnMouseWheelBackward(self):
        pass
    
    #===========================================================================
    # Description:
    #    OnChar implements keyboard functions, but subclasses can override this 
    #    behavior
    #===========================================================================
    def OnChar(self):
        rwi = self.Interactor
        keyCode = rwi.GetKeyCode()
        if keyCode in ['m', 'M']:
            if self.AnimState == self.VTKIS_ANIM_OFF:
                self.StartAnimate()
            else:
                self.StopAnimate()
        elif keyCode in ['Q', 'q', 'e', 'E']:
            rwi.ExitCallback()
        elif keyCode in ['f', 'F']:
            self.AnimState = self.VTKIS_ANIM_ON
            path = None
            self.FindPokedRenderer(rwi.GetEventPosition()[0], 
                                   rwi.GetEventPosition()[1])
            rwi.GetPicker().Pick(rwi.GetEventPosition()[0], 
                                 rwi.GetEventPosition()[1],
                                 0.0,
                                 self.CurrentRenderer)
            picker = vtk.vtkAbstractPropPicker.SafeDownCast(rwi.GetPicker())
            if picker <> None:
                path = picker.GetPath()
            if path <> None:
                rwi.FlyTo(self.CurrentRenderer, picker.GetPickPosition()[0],
                          picker.GetPickPosition()[1], picker.GetPickPosition()[2])
            self.AnimState = self.VTKIS_ANIM_OFF   
        elif keyCode in ['u', 'U']:
            rwi.UserCallback()
        elif keyCode in ['r', 'R']:
            self.FindPokedRenderer(rwi.GetEventPosition()[0], 
                                   rwi.GetEventPosition()[1])
            self.CurrentRenderer.ResetCamera()
            rwi.Render()
        elif keyCode in ['w', 'W']:
            self.FindPokedRenderer(rwi.GetEventPosition()[0], 
                                   rwi.GetEventPosition()[1])
            ac = self.CurrentRenderer.GetActors()
            
            ac.InitTraversal()
            while True:
                anActor = ac.GetNextActor()
                if anActor <> None:
                    anActor.InitPathTraversal()
                    while True:
                        path = anActor.GetNextPath()
                        if path <> None:
                            aPart = path.GetLastNode().GetViewProp()
                            aPart.GetProperty().SetRepresentationToWireframe()
                        else:
                            break
                else:
                    break
                rwi.Render()
        elif keyCode in ['s', 'S']:  
            self.FindPokedRenderer(rwi.GetEventPosition()[0], 
                                   rwi.GetEventPosition()[1])
            ac = self.CurrentRenderer.GetActors()
           
            ac.InitTraversal()
            while True:
                anActor = ac.GetNextActor()
                if anActor <> None:
                    anActor.InitPathTraversal()
                    while True:
                        path = anActor.GetNextPath()
                        if path <> None:
                            aPart = path.GetLastNode().GetViewProp()
                            aPart.GetProperty().SetRepresentationToSurface()
                        else:
                            break
                else:
                    break
                rwi.Render()
        elif keyCode == '3':
            if rwi.GetRenderWindow().GetStereoRender():
                rwi.GetRenderWindow().StereoRenderOff()
            else:
                rwi.GetRenderWindow().StereoRenderOn()
            rwi.Render()
        elif keyCode in ['p', 'P']:
            if self.State == self.VTKIS_NONE:
                path = None
                eventPos = rwi.GetEventPosition()
                self.FindPokedRenderer(eventPos[0], eventPos[1])
                rwi.StartPickCallback()
                picker = vtk.vtkAbstractPicker.SafeDownCast(rwi.GetPicker())
                if picker <> None:
                    picker.Pick(eventPos[0], eventPos[1], 0.0, self.CurrentRenderer)
                    path = picker.GetPath()
                if path == None:
                    self.HighlightProp(None)
                    self.PropPicked = False
                else:
                    self.HighlightProp(path.GetFirstNode().GetViewProp())
                    self.PropPicked = True
                rwi.EndPickCallback()
            
    def OnKeyDown(self):
        pass
    
    def OnKeyUp(self):
        pass
    
    def OnKeyPress(self):
        pass
    
    def OnKeyRelease(self):
        pass
    
    #===========================================================================
    # Description:
    #    These are more esoteric events, but are useful in some cases.
    #===========================================================================
    def OnExpose(self):
        pass
    
    def OnConfigure(self):
        pass
    
    def OnEnter(self):
        pass
    
    def OnLeave(self):
        pass
    
    #===========================================================================
    # Description:
    #    OnTimer calls Rotate, Rotate etc which should be overridden by
    #    style subclasses.
    #    By overriding the Rotate, Rotate members we can
    #    use this timer routine for Joystick or Trackball - quite tidy
    #===========================================================================
    def OnTimer(self):
        rwi = self.Interactor
        if self.State == self.VTKIS_NONE:
            if self.AnimState == self.VTKIS_ANIM_ON:
                if self.UseTimers:
                    rwi.DestroyTimer(self.TimerId)
                rwi.Render()
                if self.UseTimers:
                    self.TimerId = rwi.CreateRepeatingTimer(self.TimerDuration)
        elif self.State == self.VTKIS_ROTATE:
            self.Rotate()
        elif self.State == self.VTKIS_PAN:
            self.Pan()
        elif self.State == self.VTKIS_SPIN:
            self.Spin()
        elif self.State == self.VTKIS_DOLLY:
            self.Dolly()
        elif self.State == self.VTKIS_ZOOM:
            self.Zoom()
        elif self.State == self.VTKIS_USCALE:
            self.UniformScale()
        elif self.State == self.VTKIS_TIMER:
            rwi.Render()
        else:
            pass
    #===========================================================================
    # Description:
    #    These methods for the different interactions in different modes
    #    are overridden in subclasses to perform the correct motion. Since
    #    they might be called from OnTimer, they do not have mouse coord parameters
    #    (use interactor's GetEventPosition and GetLastEventPosition)
    #===========================================================================
    def Rotate(self):
        pass
    
    def Spin(self):
        pass
    
    def Pan(self):
        pass
    
    def Dolly(self):
        pass
    
    def Zoom(self):
        pass
    
    def UniformScale(self):
        pass
    
    #===========================================================================
    # Description:
    #    utility routines used by state changes
    #===========================================================================
    def StartState(self, newstate):
        self.State = newstate
        if self.AnimState == self.VTKIS_ANIM_OFF:
            rwi = self.Interactor
            rwi.GetRenderWindow().SetDesiredUpdateRate(rwi.GetDesiredUpdateRate())
            self.InvokeEvent("StartInteractionEvent")
            self.TimerId = rwi.CreateRepeatingTimer(self.TimerDuration)
            if self.UseTimers and not self.TimerId:
                self.State = self.VTKIS_NONE
                print "Timer start failed"
            
            
    
    def StopState(self):
        self.State = self.VTKIS_NONE
        if self.AnimState == self.VTKIS_ANIM_OFF:
            rwi = self.Interactor
            rwi.GetRenderWindow().SetDesiredUpdateRate(rwi.GetStillUpdateRate())
            if self.UseTimers and not rwi.DestroyTimer(self.TimerId):
                self.State = self.VTKIS_NONE
                print "Timer stop failed"
            self.InvokeEvent("EndInteractionEvent")
            rwi.Render()
    
    #===========================================================================
    # Description:
    #    Interaction mode entry points used internally.  
    #===========================================================================
    def StartAnimate(self):
        rwi = self.Interactor
        self.AnimState = self.VTKIS_ANIM_ON
        if self.State == self.VTKIS_NONE:
            rwi.GetRenderWindow().SetDesiredUpdateRate(rwi.GetDesiredUpdateRate())
            self.TimerId = rwi.CreateRepeatingTimer(self.TimerDuration)
            if self.UseTimers and not self.TimerId:
                print "Timer start failed"
        rwi.Render()
        
    
    def StopAnimate(self):
        rwi = self.Interactor
        self.AnimState = self.VTKIS_ANIM_OFF
        if self.State == self.VTKIS_NONE:
            rwi.GetRenderWindow().SetDesiredUpdateRate(rwi.GetStillUpdateRate())
            if self.UseTimers and not rwi.DestroyTimer(self.TimerId):
                print "Timer stop failed"
        
    
    def StartRotate(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_ROTATE)
    
    def EndRotate(self):
        if self.State <> self.VTKIS_ROTATE:
            return
        self.StopState()
    
    def StartZoom(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_ZOOM)
    
    def EndZoom(self):
        if self.State <> self.VTKIS_ZOOM:
            return
        self.StopState()
    
    def StartPan(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_PAN)
    
    def EndPan(self):
        if self.State <> self.VTKIS_PAN:
            return
        self.StopState()
    
    def StartSpin(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_SPIN)
    
    def EndSpin(self):
        if self.State <> self.VTKIS_SPIN:
            return
        self.StopState()
    
    def StartDolly(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_DOLLY)
    
    def EndDolly(self):
        if self.State <> self.VTKIS_DOLLY:
            return
        self.StopState()
    
    def StartUniformScale(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_USCALE)
    
    def EndUniformScale(self):
        if self.State <> self.VTKIS_USCALE:
            return
        self.StopState()
    
    def StartTimer(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_TIMER)
    
    def EndTimer(self):
        if self.State <> self.VTKIS_NONE:
            return
        self.StartState(self.VTKIS_TIMER)
    
    #===========================================================================
    # Description:
    #  When picking successfully selects an actor, this method highlights the
    #  picked prop appropriately. Currently this is done by placing a bounding 
    #  box around a picked vtkProp3D, and using the PickColor to highlight a
    #  vtkProp2D. 
    #===========================================================================
    def HighlightProp(self, prop):
        self.CurrentProp = prop
        
        if prop <> None:
            actor2D = vtk.vtkActor2D.SafeDownCast(prop)
            prop3D=vtk.vtkProp3D.SafeDownCast(prop)
            if ( prop3D <> None):
                self.HighlightProp3D(prop3D)
            elif( actor2D <> None):
                self.HighlightActor2D(actor2D)
            else:
                # unhighlight everything, both 2D & 3D
                self.HighlightActor2D(None)
                self.HighlightProp3D(None)
            if (self.Interactor <> None):
                self.Interactor.Render()
            
    def HighlightActor2D(self, actor2D):
        # If nothing has changed, just return
        if actor2D == self.PickedActor2D:
            return
        if actor2D <> None:
            if self.PickedActor2D:
                actor2D.GetProperty().SetColor(self.PickedActor2D.GetProperty().GetColor())
                self.PickedActor2D.GetProperty().SetColor(self.PickColor)
            else:
                tmpColor = [0.0]*3
                actor2D.GetProperty().GetColor(tmpColor)
                actor2D.GetProperty().SetColor(self.PickColor)
                self.PickColor = tmpColor
        else:
            if self.PickedActor2D:
                tmpColor = [0.0]*3
                self.PickedActor2D.GetProperty().GetColor(tmpColor)
                self.PickedActor2D.GetProperty().SetColor(self.PickColor)
                self.PickColor = tmpColor
        
        self.PickedActor2D = actor2D
    
    def HighlightProp3D(self, prop3D):
        # no prop picked now 
        if prop3D <> None:
            # was there previously?
            if self.PickedRenderer <> None and self.OutlineActor <> None:
                self.PickedRenderer.RemoveActor(self.OutlineActor)
                self.PickedRenderer = None
            else: #prop picked now 
                if not self.OutlineActor:
                    # have to defer creation to get right type
                    self.OutlineActor = vtk.vtkActor()
                    self.OutlineActor.PickableOff()
                    self.OutlineActor.DragableOff()
                    self.OutlineActor.SetMapper(self.OutlineMapper)
                    self.OutlineActor.GetProperty().SetColor(self.PickColor)
                    self.OutlineActor.GetProperty().SetAmbient(1.0)
                    self.OutlineActor.GetProperty().SetDiffuse(0.0)
                
                # check if picked in different renderer to previous pick
                if self.CurrentRenderer <> self.PickedRenderer:
                    if self.PickedRenderer <> None and self.OutlineActor <> None:
                        self.PickedRenderer.RemoveActor(self.OutlineActor)
                    self.CurrentRenderer.AddActor(self.OutlineActor)
                    self.PickedRenderer = self.CurrentRenderer
                self.Outline.SetBounds(prop3D.GetBounds())
            
    
    #===========================================================================
    # Description:
    #    Set/Get the pick color (used by default to color vtkActor2D's).
    #    The color is expressed as red/green/blue values between (0.0,1.0).
    #===========================================================================
    def SetPickColor(self, PickColor):
        self.PickColor = PickColor
    
    def GetPickColor(self):
        return self.PickColor
    
    #===========================================================================
    # Description:
    #  Set/Get the mouse wheel motion factor. Default to 1.0. Set it to a 
    #  different value to emphasize or de-emphasize the action triggered by
    #  mouse wheel motion.
    #===========================================================================
    def SetMouseWheelMotionFactor(self, MouseWheelMotionFactor):
        self.MouseWheelMotionFactor = MouseWheelMotionFactor
    
    def GetMouseWheelMotionFactor(self):
        return self.MouseWheelMotionFactor
    
    #===========================================================================
    # Description:
    #    Main process event method
    #===========================================================================
    def ProcessEvents(self, object, event, clientdata, calldata):
        
        if event == "ExposeEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("ExposeEvent"):
                clientdata.InvokeEvent("ExposeEvent")
            else:
                clientdata.OnExpose()    
        elif event == "ConfigureEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("ConfigureEvent"):
                clientdata.InvokeEvent("ConfigureEvent")
            else:
                clientdata.OnConfigure()
        elif event == "EnterEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("EnterEvent"):
                clientdata.InvokeEvent("EnterEvent")
            else:
                clientdata.OnEnter()
        elif event == "LeaveEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("LeaveEvent"):
                clientdata.InvokeEvent("LeaveEvent")
            else:
                clientdata.OnLeave()
        elif event == "TimerEvent":
            # The calldata should be a timer id, but because of legacy we check
            #  and make sure that it is non-NULL.
            #timerId = 1
            #if calldata <> None:
            #    timerId = calldata
            if clientdata.HandleObservers and clientdata.HasObserver("TimerEvent"):
                clientdata.InvokeEvent("TimerEvent")
            else:
                clientdata.OnTimer()
        elif event == "MouseMoveEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("MouseMoveEvent"):
                clientdata.InvokeEvent("MouseMoveEvent")
            else:
                clientdata.OnMouseMove()
        elif event == "LeftButtonPressEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("LeftButtonPressEvent"):
                clientdata.InvokeEvent("LeftButtonPressEvent")
            else:
                clientdata.OnLeftButtonDown()
        elif event == "LeftButtonReleaseEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("LeftButtonReleaseEvent"):
                clientdata.InvokeEvent("LeftButtonReleaseEvent")
            else:
                clientdata.OnLeftButtonUp()
        elif event == "MiddleButtonPressEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("MiddleButtonPressEvent"):
                clientdata.InvokeEvent("MiddleButtonPressEvent")
            else:
                clientdata.OnMiddleButtonDown()    
        elif event == "MiddleButtonReleaseEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("MiddleButtonReleaseEvent"):
                clientdata.InvokeEvent("MiddleButtonReleaseEvent")
            else:
                clientdata.OnMiddleButtonUp()
        elif event == "RightButtonPressEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("RightButtonPressEvent"):
                clientdata.InvokeEvent("RightButtonPressEvent")
            else:
                clientdata.OnRightButtonDown()
        elif event == "RightButtonReleaseEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("RightButtonReleaseEvent"):
                clientdata.InvokeEvent("RightButtonReleaseEvent")
            else:
                clientdata.OnRightButtonUp()
        elif event == "MouseWheelForwardEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("MouseWheelForwardEvent"):
                clientdata.InvokeEvent("MouseWheelForwardEvent")
            else:
                clientdata.OnMouseWheelForward()
        elif event == "MouseWheelBackwardEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("MouseWheelBackwardEvent"):
                clientdata.InvokeEvent("MouseWheelBackwardEvent")
            else:
                clientdata.OnMouseWheelBackward()
        elif event == "KeyPressEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("KeyPressEvent"):
                clientdata.InvokeEvent("KeyPressEvent")
            else:
                clientdata.OnKeyDown()
                clientdata.OnKeyPress()
        elif event == "KeyReleaseEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("KeyReleaseEvent"):
                clientdata.InvokeEvent("KeyReleaseEvent")
            else:
                clientdata.OnKeyUp()
                clientdata.OnKeyPress()
        elif event == "CharEvent":
            if clientdata.HandleObservers and clientdata.HasObserver("CharEvent"):
                clientdata.InvokeEvent("CharEvent")
            else:
                clientdata.OnChar()
        elif event == "DeleteEvent":
            self.SetInteractor(0)
               
    def PrintSelf(self):
        pass

if __name__ == "__main__":
    pass      