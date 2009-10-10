# -*- coding:utf-8 -*-
"""
Created on 2009-9-17

@author: summit
"""

import vtk

class vtkPythonInteractorObserver(vtk.vtkObject):
    
    def __init__(self):
        # The state of the widget, whether on or off (observing events or not)
        self.Enabled = False
        # Used to associate observers with the interactor
        self.Interactor = None
        # Internal ivars for processing events
        self.CurrentRenderer = None
        self.DefaultRenderer = None
        # Priority at which events are processed
        self.Priority = 0.0
        # Keypress activation controls
        self.KeyPressActivation = 1
        self.KeyPressActivationValue = 'i'
        # Used to process events
        self.EventCallbackCommand =  None# subclasses use one
        # listens to key activation
        self.KeyPressCallbackCommand = lambda obj, event:self.ProcessEvents( obj, event, self, None) 
        # The mediator used to request resources from the interactor.
        self.ObserverMediator = None
        self.CharObserverTag = 0
        self.DeleteObserverTag = 0
        
    #===========================================================================
    # Methods for turning the interactor observer on and off, and determining
    # its state. All subclasses must provide the SetEnabled() method.
    # Enabling a vtkInteractorObserver has the side effect of adding
    # observers; disabling it removes the observers. Prior to enabling the
    # vtkInteractorObserver you must set the render window interactor (via
    # SetInteractor()). Initial value is 0.
    #===========================================================================
    def SetEnabled(self, Enabled):
        pass
    
    def GetEnabled(self):
        return self.Enabled
    
    def EnableOn(self):
        self.SetEnable(True)
    
    def EableOff(self):
        self.SetEnable(False)
    
    def On(self):
        self.SetEnable(True)
    
    def Off(self):
        self.SetEnable(False)
    
    #===========================================================================
    # This method is used to associate the widget with the render window
    # interactor.  Observers of the appropriate events invoked in the render
    # window interactor are set up as a result of this method invocation.
    # The SetInteractor() method must be invoked prior to enabling the
    # vtkInteractorObserver.
    #===========================================================================
    def SetInteractor(self, iren):
        if (iren == self.Interactor):
            return
        
        # Since the observer mediator is bound to the interactor, reset it to
        # 0 so that the next time it is requested, it is queried from the
        # new interactor.
        # Furthermore, remove ourself from the mediator queue.
        if self.ObserverMediator<>None:
            self.ObserverMediator.RemoveAllCursorShapeRequests(self)
            self.ObserverMediator = None
        
        # if we already have an Interactor then stop observing it
        if self.Interactor<>None:
            self.SetEnabled(False) # disable the old interactor
            self.Interactor.RemoveObserver(self.CharObserverTag)
            self.CharObserverTag = False
            self.Interactor.RemoveObserver(self.DeleteObserverTag)
            self.DeleteObserverTag = False
        self.Interactor = iren
        # add observers for each of the events handled in ProcessEvents
        if iren<>None:
            self.CharObserverTag = iren.AddObserver("CharEvent", 
                                                    lambda obj, event:self.ProcessEvents( obj, event, self, None) ,
                                                    self.Priority)
            self.DeleteObserverTag = iren.AddObserver("DeleteEvent", 
                                                      lambda obj, event:self.ProcessEvents( obj, event, self, None) ,
                                                      self.Priority)
    
    def GetInteractor(self):
        return self.Interactor
    
    #===========================================================================
    # Description:
    #  Set/Get the priority at which events are processed. This is used when
    #  multiple interactor observers are used simultaneously. The default value
    #  is 0.0 (lowest priority.) Note that when multiple interactor observer
    #  have the same priority, then the last observer added will process the
    #  event first. (Note: once the SetInteractor() method has been called,
    #  changing the priority does not effect event processing. You will have
    #  to SetInteractor(NULL), change priority, and then SetInteractor(iren)
    #  to have the priority take effect.)
    #===========================================================================
    def SetPriority(self, Priority):
        if Priority>=0.0 and Priority<=1.1:
            self.Priority = Priority
    
    def GetPriority(self):
        return self.Priority
    
    #==========================================================================
    # Description:
    # Enable/Disable of the use of a keypress to turn on and off the
    # interactor observer. (By default, the keypress is 'i' for "interactor
    # observer".)  Set the KeyPressActivationValue to change which key
    # activates the widget.)
    #==========================================================================
    def SetKeyPressActivation(self, KeyPressActivation):
        self.KeyPressActivation = KeyPressActivation
    
    def GetKeyPressActivation(self):
        return self.KeyPressActivation
    
    #===========================================================================
    # Description:
    #   Specify which key press value to use to activate the interactor observer
    #   (if key press activation is enabled). By default, the key press
    #   activation value is 'i'. Note: once the SetInteractor() method is
    #   invoked, changing the key press activation value will not affect the key
    #   press until SetInteractor(NULL)SetInteractor(iren) is called. 
    #===========================================================================
    def SetKeyPressActivationValue(self, KeyPressActivationValue):
        self.KeyPressActivationValue = KeyPressActivationValue
    
    def GetKeyPressActivationValue(self):
        return self.KeyPressActivationValue
    
    #==========================================================================
    # Description:
    #  SetGet the default renderer to use when activating the interactor 
    #  observer. Normally when the widget is activated (SetEnabled(1) or when 
    #  keypress activation takes place), the renderer over which the mouse
    #  pointer is positioned is used. Alternatively, you can specify the
    #  renderer to bind the interactor to when the interactor observer is
    #  activated. 
    #==========================================================================
    def SetDefaultRenderer(self, Renderer):
        pass
    
    def GetDefaultRenderer(self):
        return self.DefaultRenderer
    
    #==========================================================================
    # Description:
    #  SetGet the current renderer. Normally when the widget is activated 
    #  (SetEnabled(1) or when keypress activation takes place), the renderer
    #  over which the mouse pointer is positioned is used and assigned to
    #  this Ivar. Alternatively, you might want to set the CurrentRenderer
    #  explicitly.
    #  WARNING: note that if the DefaultRenderer Ivar is set (see above), 
    #  it will always override the parameter passed to SetCurrentRenderer,
    #  unless it is NULL.
    #  (i.e., SetCurrentRenderer(foo) = SetCurrentRenderer(DefaultRenderer).
    #==========================================================================
    def GetCurrentRenderer(self):
        return self.CurrentRenderer
    
    def SetCurrentRenderer(self, Renderer):
        if self.CurrentRenderer == Renderer:
            return None
        if self.CurrentRenderer <> None:
            self.CurrentRenderer.UnRegister(self)
        self.CurrentRenderer = Renderer
        if self.CurrentRenderer <> None:
            self.CurrentRenderer.Register(self)
        if Renderer and self.DefaultRenderer:
            return self.DefaultRenderer
        return None
    #===========================================================================
    # Description:
    # Sets up the keypress-i event. 
    #===========================================================================
    def Onchar(self):
        # catch additional keycodes otherwise
        if self.KeyPressActivation:
            if self.Interactor.GetKeyCode() == self.KeyPressActivationValue:
                if not self.Enabled:
                    self.On()
                else:
                    self.Off()
                    
    #==========================================================================
    # Description: 
    #  Convenience methods for outside classes. Make sure that the
    #  parameter "ren" is not-null.
    #==========================================================================
    def ComputeDisplayToWorld(self, ren, x, y, z):
        worldPt = [0.0]*4
        ren.SetDisplayPoint(x,y,z)
        ren.DisplayToWorld(worldPt)
        ren.GetWorldPoint(worldPt)
        if worldPt[3]:
            worldPt[0] /= worldPt[3]
            worldPt[1] /= worldPt[3]
            worldPt[2] /= worldPt[3]
            worldPt[3] = 1.0
        return worldPt
    
    def ComputeDisplayToWorld(self, x, y, z):
        if self.CurrentRenderer <> None:
            return self.ComputeDisplayToWorld(self.CurrentRenderer, x, y, z)
        return [0.0]*4
    
    def ComputeWorldToDisplay(self, ren , x, y, z):
        displayPt = [0.0]*3
        ren.SetWorldPoint(x, y, z, 1.0)
        ren.WorldToDisplay()
        ren.GetDisplayPoint(displayPt)
        return displayPt
    
    def ComputeWorldToDisplay(self, x, y, z):
        if self.CurrentRenderer <> None:
            return self.ComputeDisplayToWorld(self.CurrentRenderer, x, y, z)
        return [0.0]*3
    
    #===========================================================================
    # Description:
    #   These methods enable an interactor observer to exclusively grab all
    #   events invoked by its associated vtkRenderWindowInteractor. (This method
    #   is typically used by widgets to grab events once an event sequence
    #   begins.) The GrabFocus() signature takes up to two vtkCommands
    #   corresponding to mouse events and keypress events. (These two commands
    #   are separated so that the widget can listen for its activation keypress,
    #   as well as listening for DeleteEvents, without actually having to process
    #   mouse events.)
    #===========================================================================
    def GrabFocus(self, mouseEvents, keypressEvents=None):
        pass
    def ReleaseFocus(self):
        pass
    
    #===========================================================================
    # Description:
    #   Utility routines used to start and end interaction.
    #   For example, it switches the display update rate. It does not invoke
    #   the corresponding events.
    #===========================================================================
    def StartInteraction(self):
        self.Interactor.GetRenderWindow().SetDesiredUpdateRate(self.Interactor.GetDesiredUpdateRate())
    
    def EndInteraction(self):
        self.Interactor.GetRenderWindow().SetDesiredUpdateRate(self.Interactor.GetStillUpdateRate())
    
    #===========================================================================
    # Description:
    #    Handles the char widget activation event. Also handles the delete event.
    #===========================================================================
    def ProcessEvents(self, obj, event, clientdata, calldata):
        if (event=="CharEvent" or event=="DeleteEvent"):
            
            if clientdata:
                if event == "CharEvent":
                    clientdata.OnChar()
                else:
                    clientdata.SetInteractor(None)
            else:
                raise RuntimeError, "Process Events received a bad client data. \
                    The client data class name was %s" %(clientdata.__class__)
                    
    def RequestCursorShape(self, requestedShape):
#        if self.Interactor == None:
#            return None
#        if self.ObserverMediator<>None:
#            self.ObserverMediator = self.Interactor.GetObserverMediator()
#        status = self.ObserverMediator.RequestCursorShape(self, requestedShape)
#        if status:
#            self.InvokeEvent("CursorChangeEvent", None)
#        return status
        pass
    
    def PrintSelf(self):
        pass

if __name__ == "__main__":
    print vtkPythonInteractorObserver().ComputeDisplayToWorld(1, 2, 3)