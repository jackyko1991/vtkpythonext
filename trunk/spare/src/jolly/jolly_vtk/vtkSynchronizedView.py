# -*- coding:utf-8 -*-
"""
Created on 2009-10-5

@author: summit
"""
import vtk
import math
from vtk.qt4.QVTKRenderWindowInteractor import *

class vtkSynchronizedView(vtk.vtkObject):
    def __init__(self):
        self.IsProcessed = False
        self.Interaction = True
        self.ShowAnnotations = True
        self.ShowDirections = True
        self.AboutDataVisibility = True
        self.LinkRender = True
        self.LinkCameraFocalAndPosition = False
        
        
        self.Renderer = None
        self.RenderWindow = None
        self.RenderWindowInteractor = None
        self.Children = []
        self.InteractorStyle = None
        # Initilize Annotations
        self.CornerAnnotation = vtk.vtkCornerAnnotation()
        self.CornerAnnotation.SetNonlinearFontScaleFactor(0.3)
        
        self.TextProperty = vtk.vtkTextProperty()
        self.CornerAnnotation.SetTextProperty(self.TextProperty)
        
        #self.OrientationAnnotation = vtkOrientationAnnotation()
        #self.OrientationAnnotation.SetNonlinearFontScaleFactor(0.25)
        
        #self.InteractorStyle = vtk.vtkInteractorStyleSwitch()
        
        self.Parent = None
        
        self.downRightAnnotation = ""
        self.upLeftAnnotation = ""
        self.upRightAnnotation = ""
        self.downLeftAnnotation = ""
        self.AboutData = ""
        self.InternalMTime = 0
        
    #===========================================================================
    # Set/Get the RenderWindow.
    #===========================================================================
    def SetRenderWindow(self, arg):
        
        if self.RenderWindow == arg:
            return
        self.Uninitialize()
        if self.RenderWindow:
            self.RenderWindow.UnRegister(self)
        self.RenderWindow = arg
        
        if self.RenderWindow:
            self.RenderWindow.Register(self)
        
        if self.RenderWindow and self.RenderWindow.GetInteractor():
            self.SetInteractor(self.RenderWindow.GetInteractor())
        
        self.Initialize()
        self.Modified()
    
    def GetRenderWindow(self):     
        return self.RenderWindow
    
    #===========================================================================
    # Set/Get the Renderer.
    #===========================================================================
    def SetRenderer(self, arg):
#        if arg == None:
#            self.Uninitialize()
#            if self.Renderer:
#                self.Renderer.UnRegister(self)
#            self.Renderer = None
#            return
        if self.Renderer == arg:
            return
        self.Uninitialize()
        if self.Renderer:
            self.Renderer.UnRegister(self)
        self.Renderer = arg
        if self.Renderer:
            self.Renderer.Register(self)
        self.Initialize()
        self.Modified()
    
    def GetRenderer(self):
        return self.Renderer
    
    def SetInteractor(self, arg):
        print "VTK_LEGACY_REPLACED:SetInteractor"
        self.SetRenderWindowInteractor(arg)
        
    #===========================================================================
    # Attach an interactor to the internal RenderWindow.
    #===========================================================================
    def SetRenderWindowInteractor(self, arg):
        if self.RenderWindowInteractor == arg:
            return
        self.Uninitialize()
        if self.RenderWindowInteractor:
            self.RenderWindowInteractor.UnRegister(self)
        self.RenderWindowInteractor = arg
        if self.RenderWindowInteractor:
            self.RenderWindowInteractor.Register(self)
        self.Initialize()
        self.Modified()
    
    def GetRenderWindowInteractor(self):
        return self.RenderWindowInteractor
    
    #===========================================================================
    # Add the actor to the first renderer of the render window if exist. 
    #  Do nothing otherwise.
    #===========================================================================
    def AddActor(self, actor):
        if self.Renderer:
            self.Renderer.AddActor(actor)
    
    #===========================================================================
    # Remove the actor from the first renderer of the render window if exist. 
    # Do nothing otherwise.
    #===========================================================================
    def RemoveActor(self, actor):
        if self.Renderer:
            self.Renderer.RemoveActor(actor)
    
    #===========================================================================
    # Enable or Disable interaction on the view. The Interaction mode is store
    # internaly and set at each time the widget is showed. The interaction
    # mode cannot be set before the vtkRenderWindowInteractor is initialized.
    #===========================================================================
    def SetInteraction(self):
        if self.RenderWindowInteractor:
            if self.Interaction and self.InteractorStyle:
                self.InteractorStyle.SetInteractor(self.RenderWindowInteractor)
                self.RenderWindowInteractor.SetInteractorStyle(None)
        self.Modified()       
    
    def InteractionOn(self):
        pass
    
    def InteractionOff(self):
        pass
    
    def GetInteraction(self):
        return self.Interaction
    
    #===========================================================================
    # Set the background color. Format is RGB, 0 <= R,G,B <=1
    # Example: SetBackgroundColor(0.9,0.9,0.9) for grey-white.
    #===========================================================================
    def SetBackgroundColor(self, r, g, b):
        if self.Renderer:
            self.Renderer.SetBackground(r,g,b)
        self.Modified()
    
    #===========================================================================
    # Set/Get annotations methods.
    #===========================================================================
    def SetNorthAnnotation(self, p_annotation):
        self.northAnnotation = p_annotation
        self.UpdateAnnotations()
        
    def GetNorthAnnotation(self):
        return self.northAnnotation 
    
    def SetSouthAnnotation(self, p_annotation):
        self.southAnnotation = p_annotation
        self.UpdateAnnotations()
        
    def GetSouthAnnotation(self):
        return self.southAnnotation 
    def SetEastAnnotation(self, p_annotation):
        self.eastAnnotation = p_annotation
        self.UpdateAnnotations()
        
    def GetEastAnnotation(self):
        return self.eastAnnotation
    
    def SetWestAnnotation(self, p_annotation):
        self.ouestAnnotation = p_annotation
        self.UpdateAnnotations()
        
    def GetWestAnnotation(self):
        return self.ouestAnnotation
    
    def SetUpLeftAnnotation(self, annotation):
        self.upLeftAnnotation = annotation
        self.CornerAnnotation.SetText(2, self.upLeftAnnotation)
        self.Modified()
    
    def SetUpRightAnnotation(self, annotation):
        self.upRightAnnotation = annotation
        self.CornerAnnotation.SetText(3, self.upRightAnnotation)
        self.Modified()
    
    def SetDownLeftAnnotation(self, annotation):
        self.downLeftAnnotation = annotation
        self.CornerAnnotation.SetText(0, self.downLeftAnnotation)
        self.Modified()
    
    def SetDownRightAnnotation(self, annotation):
        self.downRightAnnotation = annotation
        self.CornerAnnotation.SetText(1, self.downRightAnnotation)
        self.Modified()
    
    def GetUpLeftAnnotation(self):
        return self.upLeftAnnotation
    
    def GetUpRightAnnotation(self):
        return self.upRightAnnotation
    
    def GetDownRightAnnotation(self):
        return self.downRightAnnotation
    
    def GetDownLeftAnnotation(self):
        return self.downLeftAnnotation
    
    #===========================================================================
    # Set/Get about data string. Data string is automatically set in the
    # down-left text area. Overload this method to change the default behaviour.
    #===========================================================================
    def SetAboutData(self, AboutData):
        self.AboutData = AboutData
        if self.AboutDataVisibility:
            self.SetDownLeftAnnotation(self.AboutData)
        self.Modified()
    
    def GetAboutData(self):
        return self.AboutData
    
    #===========================================================================
    # Set/Get the about data text visibility. If you default the about data text in a
    # place different than the down-left text area, you must overload SetAboutDataVisibility
    # and place the text in the correct spot.
    #===========================================================================
    def SetAboutDataVisibility(self, AboutDataVisibility):
        self.AboutDataVisibility = AboutDataVisibility
        if AboutDataVisibility:
            self.SetDownLeftAnnotation(self.GetAboutData())
        else:
            self.SetDownRightAnnotation("")
    
    def AboutDataVisibilityOn(self):
        self.SetAboutDataVisibility(True)
    
    def AboutDataVisibilityOff(self):
        self.SetAboutDataVisibility(False)
    
    def GetAboutDataVisibility(self):
        return self.AboutDataVisibility
    
    #==========================================================================
    # Show/Hide the annotations, i.e., the up-left, up-right, down-left and 
    # down-right text areas.
    #==========================================================================
    def SetShowAnnotations(self,ShowAnnotations):
        self.ShowAnnotations = ShowAnnotations
        if ShowAnnotations:
            self.CornerAnnotation.SetVisibility(True)
        else:
            self.CornerAnnotation.SetVisibility(False)
        self.Modified()
    
    def ShowAnnotationsOn(self):
        self.SetShowAnnotations(True)
    
    def ShowAnnotationsOff(self):
        self.SetShowAnnotations(False)
    
    def GetShowAnnotations(self):
        return self.ShowAnnotations
    
    #===========================================================================
    # Show/Hide the directions, i.e., the up, down, left and right text areas
    #===========================================================================
    def SetShowDirections(self, ShowDirections):
        pass
    
    def ShowDirectionsOn(self):
        self.SetShowDirections(True)
    
    def ShowDirectionsOff(self):
        self.SetShowDirections(False)
    
    def GetShowDirections(self):
        return self.ShowDirections
    
    #===========================================================================
    # Get the corner annotation object.
    #===========================================================================
    def GetCornerAnnotation(self):
        return self.CornerAnnotation
    
    #===========================================================================
    # Get the orientation annotation object.
    #===========================================================================
#    def GetOrientationAnnotation(self):
#        return self.OrientationAnnotation

    
    #===========================================================================
    # Call the RenderWindow's Render() method.
    #===========================================================================
    def Render(self):
        
        if self.RenderWindow and (not self.RenderWindow.GetNeverRendered()):
            self.RenderWindow.Render()
            self.InternalMTime = self.GetMTime()
            
    
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
    
    #==========================================================================
    # Synonym of Render(), except that the rendering is acutally made
    # only if needed, i.e., if view is not up to date.
    #==========================================================================
    def Update(self):
        if self.GetMTime() > self.InternalMTime:
            self.Render()
    
    def SyncUpdate(self):
        if self.IsLocked():
            return
        self.Update()
        # this boolean is used so that the other observe won't call
        # Render() again and again and again...
        self.Lock()
        for view in self.Children:
            if (view and view.GetLinkRender()):
                view.SyncUpdate()
        self.UnLock()
    
    #===========================================================================
    # Set the camera position, focal and view up.
    #===========================================================================
    def SetCameraPosition(self, position):
        if not self.GetRenderWindow().GetNeverRender():
            self.GetRenderer().GetActiveCamera().SetPosition(position)
        self.Modified()
    
    def SetCameraFocalPoint(self, position):
        if not self.GetRenderWindow().GetNeverRender():
            self.GetRenderer().GetActiveCamera().SetFocalPoint(position)
        self.Modified()
    
    def SetCameraViewUp(self, position):
        if not self.GetRenderWindow().GetNeverRender():
            self.GetRenderer().GetActiveCamera().SetViewUp(position)
        self.Modified()
    
    #===========================================================================
    # Manually set/get the camera focal and position. Used to set the translation.
    #===========================================================================
    def SetCameraFocalAndPosition(self, focal, pos):
        if not self.GetRenderer():
            return
        camera = self.GetRenderer().GetActiveCamera()
        c_position = camera.GetPosition()
        c_focal = camera.GetFocalPoint()
        
        camera.SetFocalPoint(focal[0], focal[1], focal[2])
        camera.SetPosition   (pos[0], pos[1], pos[2])
        self.Modified()
    
    
    def GetCameraFocalAndPosition(self, focal, pos):
        if not self.GetRenderer():
            return
        
        camera = self.GetRenderer().GetActiveCamera()
        camera.GetPosition(pos)
        camera.GetFocalPoint(focal)
    

    #===========================================================================
    # Synchronized version of SetCameraFocalAndPosition.
    #===========================================================================
    def SyncSetCameraFocalAndPosition(self, focal, pos):
        if self.IsLocked():
            return
        
        if self.GetLinkCameraFocalAndPosition():
            self.SetCameraFocalAndPosition(focal, pos)
        self.Lock()    
        for view in self.Children:
            if view <> None:
                view.SyncSetCameraFocalAndPosition(focal, pos)
                view.Update()
        self.UnLock()    
                
    
    #===========================================================================
    # Reset the camera focal and position.
    #===========================================================================
    def ResetCamera(self):
        if self.Renderer:
            self.Renderer.ResetCameraClippingRange()
            self.Renderer.ResetCamera()
    
    
    #===========================================================================
    # In the tree-structure of the view, returns the View's parent.
    #===========================================================================
    def GetParent(self):
        return self.Parent
    
    #===========================================================================
    # Add a child to the list of children. Check if the child is already
    # in the list firt.
    #===========================================================================
    def AddChild(self, child): 
        if self.HasChild(child): # nothing to do
            return
        if child == self: # someone wants to add itself as a child to itself
            # remove the child from its parent as apparently it doesn't want it anymore
            parent = child.GetParent()
            if parent:
                parent.RemoveChild(child)
            #  but do nothing more
            return
        if child:
            # We temporary store the child's parent
            parent = child.Parent
            child.Register(self)
            
#           Now that the child has changed its parent, we remove
#           the child from its previous parent's children list.
#           If we have done that earlier, this could result in
#           a call to Delete(), since the RemoveChild function
#           unregsiter the object.
            if parent:
                parent.RemoveChild(child)
            
            child.SetParent(self)
            self.Children.append(child)
        
        
    
    def AddChildren(self, children):
        for child in children:
            self.AddChild(child)
    
    #==========================================================================
    # Returns true if the view has this child in its list.
    #==========================================================================
    def HasChild(self, view):
        if not view:
            return False
        if view in self.Children:
            return True
        return False
    
    #===========================================================================
    # Remove a child form the list of children.
    #===========================================================================
    def RemoveChild(self, view):
        if not view or len(self.Children):
            return
        
        try:
            ind = self.Children.index(view)
            self.Children[ind].SetParent(None)
            self.Children[ind].UnRegister(self)
            self.Children[ind].remove(view)
        except IndexError:
            print "RemoveChild: view not in the list"
            pass
        # view.UnRegister(self)
    
    #===========================================================================
    # Remove all children of the view.
    #===========================================================================
    def RemoveAllChildren(self):
        for view in self.Children:
            view.SetParent(None)
            view.UnRegister(self)
        self.Children = []
    
    #===========================================================================
    # Detach the view, i.e. add its own children (if any) to its parent's children (if any).
    #===========================================================================
    def Detach(self):
        parent = self.GetParent()
        if parent:
            parent.AddChildren(self.Children)
            parent.RemoveChild(self)
            
#           Handle the case where the parent's parent of the view is the view itself.
#           Tell the it that it no longer has a parent, life is sad...
            if parent.GetParent()==self:
                parent.SetParent(None)
                parent.UnRegister(self)
        else:
            self.RemoveAllChildren()
    
    def GetChildren(self):
        return self.Children
    
    #===========================================================================
    # Set the color of the annotations.
    #===========================================================================
    def SetTextColor(self, color):
        self.TextProperty.SetColor(color[0], color[1], color[2])
        self.CornerAnnotation.Modified()
        self.Modified()
    
    #===========================================================================
    # Part of the function propagation mechanism, when the function Lock() is
    # called, the view does not transmit the function to its children (and does
    # not do anything in fact).
    #===========================================================================
    def Lock(self):  
        self.IsProcessed = True
    
    
    
    #===========================================================================
    # Returns whether the view is Locked or not.
    #===========================================================================
    def IsLocked(self):
        return self.GetIsProcessed()
    
    #==========================================================================
    # A call to UnLock() permits to transmit function calls to the view's children.
    #==========================================================================
    def UnLock(self):
        self.IsProcessed = False
    
    #===========================================================================
    # Set/Get the camera focal and position link ON or OFF.
    #===========================================================================
    def SetLinkCameraFocalAndPosition(self):
        pass
    
    def GetLinkCameraFocalAndPosition(self):
        self.LinkCameraFocalAndPosition
        
    
    #===========================================================================
    # Set the render link ON or OFF.
    #===========================================================================
    def SetLinkRender(self, LinkRender):
        self.LinkRender = LinkRender
    
    def GetLinkRender(self):
        return self.LinkRender
    
    #===========================================================================
    # This function is called right after setting both Renderer and RenderWindow.
    # It allows a class to add actors for instance without knowing when the Renderer
    # and RenderWindow are set. For example, vtkSynchronizedView will add the 
    # corner annotations
    # during the call to the Initialize function.
    #===========================================================================
    def Initialize(self):
        if self.Renderer:
            self.Renderer.SetBackground(0.9, 0.9, 0.9)
            self.Renderer.AddViewProp(self.CornerAnnotation)
            #self.Renderer.AddViewProp(self.OrientationAnnotation)
        if self.RenderWindow and self.Renderer:
            self.RenderWindow.AddRenderer(self.Renderer)
        #self.AddActor(self.CornerAnnotation)
        #self.AddActor(self.OrientationAnnotation)
        
#        if self.RenderWindowInteractor and self.InteractorStyle:
#            self.RenderWindowInteractor.SetInteractorStyle(None)
#            #self.InteractorStyle.SetInteractor(self.RenderWindowInteractor)
#            #self.RenderWindowInteractor.SetInteractorStyle(self.InteractorStyle)
#            self.RenderWindowInteractor.SetRenderWindow(self.RenderWindow)
#        self.SetInteraction()
        if self.RenderWindowInteractor:
            self.RenderWindowInteractor.SetRenderWindow(self.RenderWindow)
        
    
    def Uninitialize(self):
        if self.Renderer:
            #self.Renderer.RemoveAllViewProps()
            self.Renderer.RemoveViewProp(self.CornerAnnotation)
            #self.Renderer.RemoveViewProp(self.OrientationAnnotation)
        if self.RenderWindow and self.Renderer:
            self.RenderWindow.RemoveRenderer(self.Renderer)
#        if self.RenderWindowInteractor:
#            self.RenderWindowInteractor.SetInteractorStyle(None)
#            self.RenderWindowInteractor.SetRenderWindow(None)
    
    def GetViewToObserve(self):
        return self.GetChildren()
    
    def GetIsProcessed(self):
        return self.IsProcessed
    
    #===========================================================================
    # Set the parent for this view. Internal use only.
    #===========================================================================
    def SetParent(self, parent):
        self.Parent = parent
        self.Modified()
    
    
    

#    def SetInteractorStyle(self, style):
#        if self.InteractorStyle == style:
#            return
#        #if self.InteractorStyle:
#        #    self.InteractorStyle.UnRegister(self)
#        self.InteractorStyle = style
#        if self.InteractorStyle:
#            self.InteractorStyle.Register(self)
#        self.Modified()
#        self.SetInteraction()
              
    def SetInteractionOff(self):
        self.InteractionOn = False
        self.SetInteraction()
    
    def SetInteractionOn(self):
        self.InteractionOn = True
        self.SetInteraction()

    def UpdateAnnotations(self):
#        if self.ShowAnnotations:
#            self.CornerAnnotation.SetText(1, self.downRightAnnotation)
#            self.CornerAnnotation.SetText(2, self.upLeftAnnotation)
#            self.CornerAnnotation.SetText(3, self.upRightAnnotation)
#        else:
#            self.CornerAnnotation.SetText(1, "")
#            self.CornerAnnotation.SetText(2, "")
#            self.CornerAnnotation.SetText(3, "")
#        # always show about data...
#        self.CornerAnnotation.SetText(0, self.downLeftAnnotation)
#        self.Modified()
        print "VTK_LEGACY_BODY:UpdateAnnotations"

    
    
    
    def __str__(self):
        return "%s:\n\tInteraction-State = %s\n\tRender Window = %s\n" %( self.__class__, self.InteractionOn,
                                                                   self.RenderWindow)

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
    vtkSynchronizedView().Modified()
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