'''
Created on 2009-10-13

@author: summit
'''
import vtk
from jolly.jolly_vtk2.vtkPythonInteractorStyleImage import *


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
        
        
        self.SliceStep = 0.0
        self.RequestedPosition = [0,0]
        
        self.__LeftButtonInteraction = self.InteractionTypeWindowLevel
        self.__RightButtonInteraction = self.InteractionTypeZoom
        self.__MiddleButtonInteraction = self.InteractionTypePan
        self.__WheelButtonInteraction = self.InteractionTypeZoom
    
    def OnMouseMove(self):
        if self.GetState() == self.VTKIS_SLICE_MOVE:
            self.DefaultMoveAction()
            self.SliceMove()
            self.InvokeEvent("SliceMoveEvent")
        elif self.GetState() == self.VTKIS_NONE:
            self.InvokeEvent("RequestedValueEvent")
        else:
            vtkPythonInteractorStyleImage.OnMouseMove(self)
    
    def OnLeftButtonDown(self):
        x,y = self.Interactor.GetEventPosition()
        if self.Interactor.GetRepeatCount():
            self.RequestedPosition[0] = x
            self.RequestedPosition[1] = y
            self.InvokeEvent("RequestedPositionEvent")
            return 
        if (self.Interactor.GetShiftKey() or self.Interactor.GetControlKey()):
            self.StartSliceMove()
        else:
            if self.getLeftButtonInteraction() == self.InteractionTypeSlice:
                self.RequestedPosition[0] = x
                self.RequestedPosition[1] = y
                self.InvokeEvent("RequestedPositionEvent")
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
    
    def OnChar(self):
        pass
    
    def OnKeyDown(self):
        pass
    
    def OnKeyUp(self):
        pass
    
    def StartSliceMove(self):
        pass
    
    def SliceMove(self):
        pass
    
    def EndSliceMove(self):
        pass
    
    def DefaultMoveAction(self):
        pass
    
    
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

    
    
    
if __name__ == "__main__":
   pass
    
    
        