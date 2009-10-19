'''
Created on 2009-10-17

@author: summit
'''
import vtk
import math
class vtkPythonRulerWidget(vtk.vtkLineWidget):
    '''
    classdocs
    '''
    Start = 0
    MovingHandle = 1
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__Caption = vtk.vtkCaptionActor2D()
        
        self.SetAlign(False)
        self.GetLineProperty().SetColor(0.85,0.85,1)
        self.GetHandleProperty().SetColor (0.75,0.75,1)
        
        self.KeyPressActivationOff()
        
        self.__Caption.SetAttachmentPoint(0, 0, 0)
        self.__Caption.SetCaption(".")
        self.__Caption.GetCaptionTextProperty().SetColor (0.7, 0.7, 0)
        self.__Caption.GetCaptionTextProperty().ShadowOff()
        self.__Caption.GetCaptionTextProperty().BoldOn()
        self.__Caption.GetCaptionTextProperty().ItalicOn()
        self.__Caption.GetTextActor().SetTextScaleModeToNone()
        self.__Caption.GetCaptionTextProperty().SetFontSize(15)
        self.__Caption.SetLeaderGlyphSize(0.05)
        self.__Caption.BorderOff()
        self.__Caption.SetPadding(5)
        
        self.__State = self.Start
        self.AddObserver("MouseMoveEvent", self.OnMouseMove)
        self.AddObserver("StartInteractionEvent", self.OnStart)
        self.AddObserver("EndInteractionEvent", self.OnEnd)
    
    #===========================================================================
    # Description:
    #    Methods that satisfy the superclass' API.
    #===========================================================================
    def SetEnabled(self, int):
        '''
        @return: None
        '''
        pass
    
    def PlaceWidgetPosition(self, bounds):
        '''
        @param bounds: double[6]
        @return: None 
        '''
    
    def PlaceWidget(self):
        vtk.vtkLineWidget.PlaceWidget(self)
    
    def PlaceWidgetByComponent(self, xmin, xmax, ymin, ymax, zmin, zmax):
        '''
        @param xmin: double 
        @param xmax: double 
        @param ymin: double 
        @param ymax: double 
        @param zmin: double 
        @param zmax: double 
        '''
        
        vtk.vtkLineWidget.PlaceWidget(xmin, xmax, ymin, ymax, zmin, zmax)
    
    def OnMouseMove(self):
        # See whether we're active
        X, Y=self.GetInteractor().GetEventPosition()
#        Okay, make sure that the pick is in the current renderer
#        vtkLineWidget::Outside
        if not self.GetCurrentRenderer() and not self.GetCurrentRenderer().IsInViewport(X,Y):
            return
        
        if self.__State == self.Start:
            return
        
#        Do different things depending on state
#        Calculations everybody does
        camera = self.GetCurrentRenderer().GetActiveCamera()
        if not camera:
            return
        
#         Compute the two points defining the motion vector
        pt1 = self.GetPoint1()
        pt2 = self.GetPoint2()
        pt = [pt1[0]-pt2[0], pt1[1]-pt2[1], pt1[2]-pt2[2]]
        
        distance = math.sqrt(pt[0]*pt[0]+pt[1]*pt[1]+pt[2]*pt[2])
        self.__Caption.SetCaption("distance: %g mm" % distance )
        self.__Caption.SetAttachmentPoint(self.GetPoint2())
        
        self.GetInteractor().Render()
        
    def OnStart(self):
        self.__State = self.MovingHandle
    
    def OnEnd(self):
        self.__State = self.Start
    
    def getCaption(self):
        return self.__Caption


    def setCaption(self, value):
        self.__Caption = value

if __name__ == "__main__":
    vtkPythonRulerWidget().PlaceWidget()

        