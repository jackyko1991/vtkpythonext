# -*- coding:utf-8 -*-
"""
Created on 2009-10-5

@author: summit
"""
import vtk
import math
from QVTKRenderWindowInteractor import *

class vtkSynchronizedView(vtk.vtkObject):
    def __init__(self):
        self.IsProcessed = False
        self.InteractionOn = True
        self.ShowAnnotations = True
        
        self.Renderer = None
        self.RenderWindow = None
        self.RenderWindowInteractor = None
        self.Children = []
        
        # Initilize Annotations
        self.CornerAnnotation = vtk.vtkCornerAnnotation()
        self.CornerAnnotation.SetNonlinearFontScaleFactor(0.3)
        
        self.TextProperty = vtk.vtkTextProperty()
        self.CornerAnnotation.SetTextProperty(self.TextProperty)
        
        #self.OrientationAnnotation = vtkOrientationAnnotation()
        #self.OrientationAnnotation.SetNonlinearFontScaleFactor(0.25)
        
        self.InteractorStyle = vtk.vtkInteractorStyleSwitch()
        
        self.Parent = None
        self.LinkRender = True
        
        self.downRightAnnotation = ""
        self.upLeftAnnotation = ""
        self.upRightAnnotation = ""
        self.downLeftAnnotation = ""
        self.AboutData = ""
        
    
    def SetRenderWindow(self, arg):
        if arg==None:
            self.Uninitialize()
            if self.RenderWindow:
                self.RenderWindow.UnRegister(self)
            self.RenderWindow = None
            return
        if self.RenderWindow == arg:
            return
        self.Uninitialize()
        if self.RenderWindow:
            self.RenderWindow.UnRegister(self)
        self.RenderWindow = arg
        
        if self.RenderWindow:
            self.RenderWindow.Register(self)
        
        if self.RenderWindow.GetInteractor():
            self.SetInteractor(self.RenderWindow.GetInteractor())
        
        self.Initialize()       

    def SetRenderer(self, arg):
        if arg == None:
            self.Uninitialize()
            if self.Renderer:
                self.Renderer.UnRegister(self)
            self.Renderer = None
            return
        if self.Renderer == arg:
            return
        self.Uninitialize()
        if self.Renderer:
            self.Renderer.UnRegister(self)
        self.Renderer = arg
        if self.Renderer:
            self.Renderer.Register(self)
        self.Initialize()
    
    def SetInteractor(self, arg):
        if self.RenderWindowInteractor == arg:
            return
        self.Uninitialize()
        if self.RenderWindowInteractor:
            self.RenderWindowInteractor.UnRegister(self)
        self.RenderWindowInteractor = arg
        if self.RenderWindowInteractor:
            self.RenderWindowInteractor.Register(self)
        self.Initialize()

    def SetInteractorStyle(self, style):
        if self.InteractorStyle == style:
            return
        if self.InteractorStyle:
            self.InteractorStyle.UnRegister(self)
        self.InteractorStyle = style
        if self.InteractorStyle:
            self.InteractorStyle.Register(self)
        self.Modified()
        self.SetInteraction()
    
    def Initialize(self):
        if self.Renderer:
            self.Renderer.SetBackground(0.9, 0.9, 0.9)
        if self.RenderWindow and self.Renderer:
            self.RenderWindow.AddRenderer(self.Renderer)
        self.AddActor(self.CornerAnnotation)
        #self.AddActor(self.OrientationAnnotation)
        
        if self.RenderWindowInteractor and self.InteractorStyle:
            self.RenderWindowInteractor.SetInteractorStyle(self.InteractorStyle)
            self.RenderWindowInteractor.SetRenderWindow(self.RenderWindow)
        self.SetInteraction()
    
    def Uninitialize(self):
        if self.Renderer:
            self.Renderer.RemoveAllViewProps()
        if self.RenderWindow and self.Renderer:
            self.RenderWindow.RemoveRenderer(self.Renderer)
        if self.RenderWindowInteractor:
            self.RenderWindowInteractor.SetInteractorStyle(None)
            self.RenderWindowInteractor.SetRenderWindow(None)
    
    def GetViewToObserve(self):
        return self.GetChildren()
    
    def AddActor(self, actor):
        if self.Renderer:
            self.Renderer.AddActor(actor)
    
    def RemoveActor(self, actor):
        if self.Renderer:
            self.Renderer.RemoveActor(actor)
            
    def SetInteractionOff(self):
        self.InteractionOn = False
        self.SetInteraction()
    
    def SetInteractionOn(self):
        self.InteractionOn = True
        self.SetInteraction()
    
    def SetInteraction(self):
        if self.RenderWindowInteractor:
            if not self.InteractionOn:
                self.RenderWindowInteractor.SetInteractorStyle(None)
            else:
                if self.InteractorStyle:
                    self.RenderWindowInteractor.SetInteractorStyle(self.InteractorStyle)
    
    def SetUpLeftAnnotation(self, annotation):
        self.upLeftAnnotation = annotation
        self.UpdateAnnotations()
    
    def SetUpRightAnnotation(self, annotation):
        self.upRightAnnotation = annotation
        self.UpdateAnnotations()
    
    def SetDownLeftAnnotation(self, annotation):
        self.downLeftAnnotation = annotation
        self.UpdateAnnotations()
    
    def SetDownRightAnnotation(self, annotation):
        self.downRightAnnotation = annotation
        self.UpdateAnnotations()
    
    def UpdateAnnotations(self):
        if self.ShowAnnotations:
            self.CornerAnnotation.SetText(1, self.downRightAnnotation)
            self.CornerAnnotation.SetText(2, self.upLeftAnnotation)
            self.CornerAnnotation.SetText(3, self.upRightAnnotation)
        else:
            self.CornerAnnotation.SetText(1, "")
            self.CornerAnnotation.SetText(2, "")
            self.CornerAnnotation.SetText(3, "")
        # always show about data...
        self.CornerAnnotation.SetText(0, self.downLeftAnnotation)
        
    def SetBackgroundColor(self, r, g, b):
        if self.Renderer:
            self.Renderer.SetBackground(r,g,b)
    
    def HasChild(self, view):
        if not view:
            return False
        if view in self.Children:
            return True
        return False
    
    def ResetCamera(self):
        if self.Renderer:
            self.Renderer.ResetCamera()
    
    def Render(self):
        
        if self.RenderWindow and (not self.RenderWindow.GetNeverRendered()):
            self.RenderWindow.Render()
            
    def IsLocked(self):
        return self.IsProcessed
    
    def SyncRender(self):
        if self.IsLocked():
            return
        self.Render()
        # this boolean is used so that the other observe won't call
        # Render() again and again and again...
        self.Lock()
        for view in self.Children:
            if (view and view.GetLinkRender()):
                view.SyncRender()
        self.UnLock()
    
    def __str__(self):
        return "%s:\n\tInteraction-State = %s\n\tRender Window = %s\n" %( self.__class__, self.InteractionOn,
                                                                   self.RenderWindow)
    
    def SetParent(self, parent):
        self.Parent = parent
    
    def AddChild(self, child): 
        if self.HasChild(child) or child == self:
            return
        if child:
            parent = child.Parent
            child.Register(self)
            child.SetParent(self)
            self.Children.append(child)
            
            # Now that the child has changed its parent, we remove
            # the child from its previous parent's children list.
            # If we have done that earlier, this could result in
            # a call to Delete(), since the RemoveChild function
            # unregsiter the object.
        
        if parent:
            parent.RemoveChild(child)
    
    def AddChildren(self, children):
        for child in children:
            self.AddChild(child)
    
    def RemoveChild(self, view):
        self.Children.remove(view)
        # view.UnRegister(self)
        
    def RemoveAllChildren(self):
        self.Children = []
    
    def Detach(self):
        if self.Parent:
            self.Parent.AddChildren(self.Children)
            self.Parent.RemoveChild(self)
            self.Parent = None
        self.RemoveAllChildren()
    
    def Lock(self):  
        self.IsProcessed = True
    
    def UnLock(self):
        self.IsProcessed = False
        
    def SetTextColor(self, color):
        self.TextProperty.SetColor(color[0], color[1], color[2])
        self.CornerAnnotation.Modified()
    
    # Get/Set lower left annotation
    def SetAboutData(self, about):
        self.AboutData = about
        self.SetDownLeftAnnotation(self.AboutData)

def vtkrint(a):
    test = math.fabs(a-float(int(a)))
    res = 0
    if (a>0):
        if test>0.5:
            res = a+1
        else:
            res = a
    else:
        if test>0.5:
            res = a-1
        else:
            res = a
    return res
        
if __name__ == "__main__":
    # 
    # Next we create an instance of vtkConeSource and set some of its
    # properties. The instance of vtkConeSource "cone" is part of a visualization
    # pipeline (it is a source process object); it produces data (output type is
    # vtkPolyData) which other filters may process.
    #
    cone = vtk.vtkConeSource()
    cone.SetHeight( 3.0 )
    cone.SetRadius( 1.0 )
    cone.SetResolution( 10 )
    
    # 
    # In this example we terminate the pipeline with a mapper process object.
    # (Intermediate filters such as vtkShrinkPolyData could be inserted in
    # between the source and the mapper.)  We create an instance of
    # vtkPolyDataMapper to map the polygonal data into graphics primitives. We
    # connect the output of the cone souece to the input of this mapper.
    #
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection( cone.GetOutputPort() )
    
    # 
    # Create an actor to represent the cone. The actor orchestrates rendering of
    # the mapper's graphics primitives. An actor also refers to properties via a
    # vtkProperty instance, and includes an internal transformation matrix. We
    # set this actor's mapper to be coneMapper which we created above.
    #
    coneActor = vtk.vtkActor()
    coneActor.SetMapper( coneMapper )

    #
    # Create the Renderer and assign actors to it. A renderer is like a
    # viewport. It is part or all of a window on the screen and it is
    # responsible for drawing the actors it has.  We also set the background
    # color here
    #
    ren1= vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    iren = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleTrackballCamera()
    view =  vtkSynchronizedView()
  
    view.SetRenderer(ren1)
    view.SetRenderWindow(renWin)
    view.SetInteractor(iren)
    view.AddActor(coneActor)
    #view.SetInteractorStyle(style)
    #sview.Initialize()
    view.SetUpLeftAnnotation("hello")
    view.SetDownLeftAnnotation("jolly")
    view.Render()
    iren.Initialize()
    iren.Start()
    print view