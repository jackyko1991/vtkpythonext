'''
Created on 2009-10-13

@author: summit
'''
import vtk
from jolly.jolly_vtk2.vtkPythonInteractorStyleImage import *
from jolly.jolly_vtk2.vtkPythonViewImage2DCommand import *


class vtkPythonInteractorStyleImage2D(vtkPythonInteractorStyleImage):
    '''
    classdocs
    '''
    
    VTKIS_SLICE_MOVE = 5051
    
    InteractionTypeNull = 0
    InteractionTypeSlice = 1
    InteractionTypeWindowLevel = 2
    InteractionTypeZoom = 3
    InteractionTypePan = 4

    def __init__(self):
        '''
        Constructor
        '''
        vtkPythonInteractorStyleImage.__init__(self)
        
        
        self.__SliceStep = 0.0
        self.__RequestedPosition = [0,0]
        
        self.__LeftButtonInteraction = self.InteractionTypeWindowLevel
        self.__RightButtonInteraction = self.InteractionTypeZoom
        self.__MiddleButtonInteraction = self.InteractionTypePan
        self.__WheelButtonInteraction = self.InteractionTypeZoom
        self.__UserEventTag = ""
    
    def OnMouseMove(self):
        
        if self.State == self.VTKIS_SLICE_MOVE:
            self.DefaultMoveAction()
            self.SliceMove()
            self.__UserEventTag = "SliceMoveEvent"
            self.InvokeEvent("UserEvent")
            return
        if self.State == self.VTKIS_NONE:
            self.__UserEventTag = "RequestedValueEvent"
            self.InvokeEvent("UserEvent")
            return
            
        vtkPythonInteractorStyleImage.OnMouseMove(self)
        return
    
    def OnLeftButtonDown(self):
        x,y = self.Interactor.GetEventPosition()
        if self.Interactor.GetRepeatCount():
            self.RequestedPosition[0] = x
            self.RequestedPosition[1] = y
            self.__UserEventTag = "RequestedPositionEvent"
            self.InvokeEvent("UserEvent")
            return 
        if (self.Interactor.GetShiftKey() or self.Interactor.GetControlKey()):
            if self.getLeftButtonInteraction() == self.InteractionTypeWindowLevel:
                self.StartSliceMove()
        else:
            if self.getLeftButtonInteraction() == self.InteractionTypeSlice:
                self.RequestedPosition[0] = x
                self.RequestedPosition[1] = y
                self.__UserEventTag = "RequestedPositionEvent"
                self.InvokeEvent("UserEvent")
                self.StartSliceMove()
            elif self.getLeftButtonInteraction() == self.InteractionTypeWindowLevel:
                vtkPythonInteractorStyleImage.OnLeftButtonDown(self)
            elif self.getLeftButtonInteraction() == self.InteractionTypeZoom:
                vtkPythonInteractorStyleImage.OnRightButtonDown(self)
            elif self.getLeftButtonInteraction() == self.InteractionTypePan:
                vtkPythonInteractorStyleImage.OnMiddleButtonDown(self)
            else:
                pass
            
    def OnLeftButtonUp(self):
        if self.GetState() == self.VTKIS_SLICE_MOVE:
            self.EndSliceMove()
        
        if self.getLeftButtonInteraction() == self.InteractionTypeSlice:
            pass
        elif self.getLeftButtonInteraction() == self.InteractionTypeZoom:
            vtkPythonInteractorStyleImage.OnRightButtonUp(self)
        elif self.getLeftButtonInteraction() == self.InteractionTypePan:
            vtkPythonInteractorStyleImage.OnMiddleButtonUp(self)
        elif self.getLeftButtonInteraction() == self.InteractionTypeWindowLevel:
            vtkPythonInteractorStyleImage.OnLeftButtonUp(self)
        else:
            pass  
          
    def OnMiddleButtonDown(self):
        x,y = self.Interactor.GetEventPosition()
        self.FindPokedRenderer(x, y)
        if not self.CurrentRenderer:
            return
        if self.getMiddleButtonInteraction() == self.InteractionTypeSlice:
            self.StartSliceMove()
        elif self.getMiddleButtonInteraction() == self.InteractionTypeWindowLevel:
            vtkPythonInteractorStyleImage.OnLeftButtonDown(self)
        elif self.getWheelButtonInteraction() == self.InteractionTypeZoom:
            vtkPythonInteractorStyleImage.OnRightButtonDown(self)
        elif self.getWheelButtonInteraction() == self.InteractionTypePan:
            vtkPythonInteractorStyleImage.OnMiddleButtonDown(self)
        else:
            pass
    
    def OnMiddleButtonUp(self):
        if self.GetState() == self.VTKIS_SLICE_MOVE:
            self.EndSliceMove()
        
        if self.getMiddleButtonInteraction() == self.InteractionTypeSlice:
            pass
        elif self.getMiddleButtonInteraction() == self.InteractionTypeZoom:
            vtkPythonInteractorStyleImage.OnRightButtonUp(self)
        elif self.getMiddleButtonInteraction() == self.InteractionTypePan:
            vtkPythonInteractorStyleImage.OnMiddleButtonUp(self)
        elif self.getMiddleButtonInteraction() == self.InteractionTypeWindowLevel:
            vtkPythonInteractorStyleImage.OnLeftButtonUp(self)
        else:
            pass  
    
    def OnRightButtonDown(self):
        if self.getRightButtonInteraction() == self.InteractionTypeSlice:
            self.StartSliceMove()
        elif self.getRightButtonInteraction() == self.InteractionTypeZoom:
            vtkPythonInteractorStyleImage.OnRightButtonDown(self)
        elif self.getRightButtonInteraction() == self.InteractionTypePan:
            vtkPythonInteractorStyleImage.OnMiddleButtonDown(self)
        elif self.getRightButtonInteraction() == self.InteractionTypeWindowLevel:
            vtkPythonInteractorStyleImage.OnLeftButtonDown(self)
        else:
            pass  
    
    def OnRightButtonUp(self):
        if self.GetState() == self.VTKIS_SLICE_MOVE:
            self.EndSliceMove()
        
        if self.getRightButtonInteraction() == self.InteractionTypeSlice:
            pass
        elif self.getRightButtonInteraction() == self.InteractionTypeZoom:
            vtkPythonInteractorStyleImage.OnRightButtonUp(self)
        elif self.getRightButtonInteraction() == self.InteractionTypePan:
            vtkPythonInteractorStyleImage.OnMiddleButtonUp(self)
        elif self.getRightButtonInteraction() == self.InteractionTypeWindowLevel:
            vtkPythonInteractorStyleImage.OnLeftButtonUp(self)
        else:
            pass  
    
    def OnMouseWheelForward(self):
        vtkPythonInteractorStyleImage.OnMouseWheelForward(self)
    
    def OnMouseWheelBackward(self):
        vtkPythonInteractorStyleImage.OnMouseWheelBackward(self)
    
    def OnChar(self):
        rwi = self.Interactor
        print rwi.GetKeySym()
        if rwi.GetKeySym() == "Up":
            self.setSliceStep(1)
            self.__UserEventTag = "SliceMoveEvent"
            self.InvokeEvent("UserEvent")
        elif rwi.GetKeySym() == "Down":
            self.setSliceStep(-1)
            self.__UserEventTag = "SliceMoveEvent"
            self.InvokeEvent("UserEvent")
        elif rwi.GetKeyCode() == 'r':
            self.__UserEventTag = "ResetViewerEvent"
            self.InvokeEvent("UserEvent")
            
        vtkPythonInteractorStyleImage.OnChar(self)
    
    def OnKeyDown(self):
#       Apparently there is a problem here.
#       The event vtkCommand::CharEvent and vtkCommand::KeyPressEvent seem
#       to mix between each other.
#       tackled by calling the charevent
#       (supposed to be called at any keyboard event)
        self.OnChar()
        vtkPythonInteractorStyleImage.OnKeyDown(self)
    
    def OnKeyUp(self):
        vtkPythonInteractorStyleImage.OnKeyUp(self)
    
    def StartSliceMove(self):
        if self.GetState()<>self.VTKIS_NONE and self.GetState()<>self.VTKIS_PICK:
            return
        self.StartState(self.VTKIS_SLICE_MOVE)
        self.__UserEventTag = "StartSliceMoveEvent"
        self.InvokeEvent("UserEvent")
       
    
    def SliceMove(self):
        rwi = self.Interactor
        dy = rwi.GetEventPosition()[1] - rwi.GetLastEventPosition()[1]
        self.setSliceStep(dy)
    
    def EndSliceMove(self):
        if self.GetState() <> self.VTKIS_SLICE_MOVE:
            return
        self.StopState()
        self.__UserEventTag = "EndSliceMoveEvent"
        self.InvokeEvent("UserEvent")
        
    
    def DefaultMoveAction(self):
        self.__UserEventTag = "DefaultMoveEvent"
        self.InvokeEvent("UserEvent")
        
    
    
    def getSliceStep(self):
        return self.__SliceStep


    def getRequestedPosition(self):
        return self.__RequestedPosition


    def getLeftButtonInteraction(self):
        return self.__LeftButtonInteraction


    def getRightButtonInteraction(self):
        return self.__RightButtonInteraction


    def getMiddleButtonInteraction(self):
        return self.__MiddleButtonInteraction


    def getWheelButtonInteraction(self):
        return self.__WheelButtonInteraction


    def setSliceStep(self, value):
        self.__SliceStep = value


    def setRequestedPosition(self, value):
        self.__RequestedPosition = value


    def setLeftButtonInteraction(self, value):
        if value < self.InteractionTypeSlice or value > self.InteractionTypeZoom:
            return
        self.__LeftButtonInteraction = value


    def setRightButtonInteraction(self, value):
        if value < self.InteractionTypeSlice or value > self.InteractionTypeZoom:
            return
        self.__RightButtonInteraction = value


    def setMiddleButtonInteraction(self, value):
        if value < self.InteractionTypeSlice or value > self.InteractionTypeZoom:
            return
        self.__MiddleButtonInteraction = value


    def setWheelButtonInteraction(self, value):
        if value < self.InteractionTypeSlice or value > self.InteractionTypeZoom:
            return
        self.__WheelButtonInteraction = value


    def getUserEventTag(self):
        return self.__UserEventTag


    def setUserEventTag(self, value):
        self.__UserEventTag = value


    
    
    
if __name__ == "__main__":
   pass
    
    
        