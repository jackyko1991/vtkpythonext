'''
Created on 2009-10-14

@author: summit
'''
import math
import vtk

class vtkPythonViewImage2DCommand(vtk.vtkObject):
    '''
    classdocs
    '''
    
    SliceMoveEvent = 1001   # vtkCommand::UserEvent = 1000
    StartSliceMoveEvent = 1002
    EndSliceMoveEvent = 1003
    RequestedPositionEvent = 1004
    RequestedValueEvent = 1005
    ResetViewerEvent = 1006
    DefaultMoveEvent = 1007
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__Viewer = None#vtkViewImage2D
        self.__InitialWindow = 0
        self.__InitialLevel = 0
        self.__InitialSlice = 0
        
        self.__DistanceWidget = vtk.vtkDistanceWidget()
        self.__DistanceWidget.KeyPressActivationOff()
        self.__DistanceWidget.CreateDefaultRepresentation()
        self.__DistanceWidget.SetKeyPressActivationValue('d')
        
        
        rep1 = vtk.vtkDistanceRepresentation2D.SafeDownCast(self.__DistanceWidget.GetRepresentation())
        rep1.GetAxis().SetTickLength(6)
        
        self.__AngleWidget = vtk.vtkAngleWidget()
        self.__AngleWidget.SetKeyPressActivationValue('a')
        self.__AngleWidget.KeyPressActivationOff()
        self.__AngleWidget.CreateDefaultRepresentation()
        rep2 = vtk.vtkAngleRepresentation2D.SafeDownCast(self.__AngleWidget.GetRepresentation())
        rep2.GetRay1().GetProperty().SetColor(0,1,0)
        rep2.GetRay2().GetProperty().SetColor(0,1,0)
        rep2.GetArc().GetProperty().SetColor(0,1,0)

    def Execute(self, obj, event, callData=None):
        '''
        Description:
           Satisfy the superclass API for callbacks. Recall that the caller is
           the instance invoking the event; eid is the event id (see
           vtkCommand.h); and calldata is information sent when the callback
           was invoked (e.g., progress value in the vtkCommand::ProgressEvent).
        @param obj: vtkObject
        @param event: vtkEvent or string
        @param calldata: vtkInteractorStyleImage2D
        @return: None
        '''
        isi = callData
        print event, ":", isi.getUserEventTag()
        if not isi or not self.__Viewer or not self.__Viewer.GetInput():
            return
        
        # Reset
        if event == "UserEvent" and isi.getUserEventTag()=="ResetViewerEvent":
            self.__Viewer.Reset()
            self.__Viewer.Render()
            return
        # Reset
        if event == "ResetWindowLevelEvent":
            self.__Viewer.ResetWindowLevel()
            self.__Viewer.Render()
            return
            
        # Statr
        if event == "StartWindowLevelEvent":
            self.__InitialWindow = self.__Viewer.GetColorWindow()
            self.__InitialLevel = self.__Viewer.GetColorLevel()
            return
        # Adjust the window level here
        if event == "WindowLevelEvent":
            size = self.__Viewer.GetRenderWindow().GetSize()
            window = self.__InitialWindow
            level = self.__InitialLevel
            
            # Compute normalized delta
            dx = 4.0 * (isi.GetWindowLevelCurrentPosition()[0]-
                        isi.GetWindowLevelStartPosition()[0])/size[0]
            dy = 4.0 * (isi.GetWindowLevelCurrentPosition()[1]-
                        isi.GetWindowLevelStartPosition()[1])/size[1]      
              
            # Scale by current values
            if math.fabs(window) > 0.01:
                dx = dx*window
            else:
                if window < 0:
                    dx = dx*-0.01
                else:
                    dx = dx*0.01
            if math.fabs(level) > 0.01:
                dy = dy * level
            else:
                if level < 0:
                    dy = dy*-0.01
                else:
                    dy = dy*0.01
            # Abs so that direction does not flip
            if window<0.0:
                dx = -1*dx
            if level<0.0:
                dy = -1*dy
            # Compute new window level
            newWindow = dx+window
            newLevel = level-dy
            
            # Stay away from zero and really
            if math.fabs(newWindow) < 0.01:
                if newWindow<0:
                    newWindow = -0.01
                else:
                    newWindow = 0.01
            if math.fabs(newLevel) < 0.01:
                if newLevel<0:
                    newLevel = -0.01
                else:
                    newLevel = 0.01
            
            self.__Viewer.SetColorWindow(newWindow)
            self.__Viewer.SetColorLevel(newLevel)
            self.__Viewer.Render()
            return
        if event == "CharEvent":
            rwi = self.__Viewer.GetRenderWindow().GetInteractor()
            if rwi.GetKeyCode() == 't':
                self.__Viewer.SetSliceOrientation((self.__Viewer.GetSliceOrientation()+1)%3)
                self.__Viewer.Render()
            elif rwi.GetKeyCode() == 'i':
                self.__Viewer.SetInterpolate((self.__Viewer.GetInterpolate()+1)%2)   
                self.__Viewer.Render()
            elif rwi.GetKeyCode() == 'd':
                self.__DistanceWidget.SetInteractor(rwi)
                self.__DistanceWidget.SetEnabled(not self.__DistanceWidget.GetEnabled())
                # Becase we could not have GrapFouce in Python , So we only end the message by StopState
                self.__DistanceWidget.AddObserver("StartInteractionEvent", lambda obj, event: isi.StopState()) 
            elif rwi.GetKeyCode() == 'a':    
                self.__AngleWidget.SetInteractor(rwi)
                self.__AngleWidget.SetEnabled(not self.__AngleWidget.GetEnabled())
                self.__AngleWidget.AddObserver("StartInteractionEvent", lambda obj, event: isi.StopState()) 
            return
        # Start Slice Move 
        if event == "UserEvent" and isi.getUserEventTag()=="StartSliceMoveEvent":    
            return
        # End Slice Move
        if event == "UserEvent" and isi.getUserEventTag()=="EndSliceMoveEvent":
            return
        # Move Slice
        if event == "UserEvent" and isi.getUserEventTag()=="SliceMoveEvent":
            step = isi.getSliceStep()
            print step
            self.__Viewer.SetSlice(self.__Viewer.GetSlice()+step)
            self.__Viewer.Render()
            return
        # Position requested
        if event == "UserEvent" and isi.getUserEventTag()=="RequestedPositionEvent":
            position = self.__Viewer.GetWorldCoordinatesFromDisplayPosition(isi.getRequestedPosition())
            self.__Viewer.SetWorldCoordinates(position)
            self.__Viewer.Render()
            return
        # default move : align cursor   
        if event == "UserEvent" and isi.getUserEventTag()=="DefaultMoveEvent":
            rwi = self.__Viewer.GetRenderWindow().GetInteractor()
            XY = rwi.GetEventPosition()
            self.__Viewer.UpdateCursor(XY)
            return
        if event == "UserEvent" and isi.getUserEventTag()=="RequestedValueEvent":
            rwi = self.__Viewer.GetRenderWindow().GetInteractor()
            XY = rwi.GetEventPosition()
            self.__Viewer.UpdateCursor(XY)
            self.__Viewer.Render()
            return

       
    def getViewer(self):
        return self.__Viewer


    def getInitialWindow(self):
        return self.__InitialWindow


    def getInitialLevel(self):
        return self.__InitialLevel


    def getInitialSlice(self):
        return self.__InitialSlice


    def getDistanceWidget(self):
        return self.__DistanceWidget


    def getAngleWidget(self):
        return self.__AngleWidget


    def setViewer(self, value):
        self.__Viewer = value


    def setInitialWindow(self, value):
        self.__InitialWindow = value


    def setInitialLevel(self, value):
        self.__InitialLevel = value


    def setInitialSlice(self, value):
        self.__InitialSlice = value


    def setDistanceWidget(self, value):
        self.__DistanceWidget = value


    def setAngleWidget(self, value):
        self.__AngleWidget = value

        