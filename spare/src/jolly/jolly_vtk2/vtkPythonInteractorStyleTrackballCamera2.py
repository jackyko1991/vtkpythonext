'''
Created on 2009-10-15

@author: summit
'''
import vtk
from jolly.jolly_vtk2.vtkPythonInteractorStyleTrackballCamera import *

class vtkPythonInteractorStyleTrackballCamera2(vtkPythonInteractorStyleTrackballCamera):
    '''
    vtkInteractorStyleTrackballCamera2 - interactive manipulation of the camera
    vtkInteractorStyleTrackballCamera2 allows the user to interactively
     manipulate (rotate, pan, etc.) the camera, the viewpoint of the scene.  In
     trackball interaction, the magnitude of the mouse motion is proportional
     to the camera motion associated with a particular mouse binding. For
     example, small left-button motions cause small changes in the rotation of
     the camera around its focal point. For a 3-button mouse, the left button
     is for rotation, the right button for zooming, the middle button for
     panning, and ctrl + left button for spinning.  (With fewer mouse buttons,
     ctrl + shift + left button is for zooming, and shift + left button is for
     panning.)
    '''
    
#    StyleIds
    TrackStyleCamera = 0
    TrackStyleActor = 1
    
    def __init__(self):
        '''
        Constructor
        '''
        vtkPythonInteractorStyleTrackballCamera.__init__(self)
        
        self.__TrackStyle = self.TrackStyleCamera
        self.__InteractionPicker = vtk.vtkPropPicker()
        self.__InteractionProp = None
    
    #===========================================================================
    # Description:
    #    Event bindings controlling the effects of pressing mouse buttons
    #    or moving the mouse.
    #===========================================================================
    def OnLeftButtonDown(self):
        '''
        @return: None
        '''
        x, y = self.GetInteractor().GetEventPosition()
        print x, y
        self.FindPokedRenderer(x, y)
        self.FindPickedActor(x, y)
        
        vtkPythonInteractorStyleTrackballCamera.OnLeftButtonDown(self)
    
    def OnMiddleButtonDown(self):
        '''
        @return: None
        '''
        x, y = self.GetInteractor().GetEventPosition()
        
        self.FindPokedRenderer(x, y)
        self.FindPickedActor(x, y)
        
        vtkPythonInteractorStyleTrackballCamera.OnMiddleButtonDown(self)
    
    def OnRightButtonDown(self):
        '''
        @return: None
        '''
        x, y = self.GetInteractor().GetEventPosition()
        
        self.FindPokedRenderer(x, y)
        self.FindPickedActor(x, y)
        
        vtkPythonInteractorStyleTrackballCamera.OnRightButtonDown(self)
    
    def OnChar(self):
        '''
        @return: None
        '''
        keyCode = self.GetInteractor().GetKeyCode()
        if keyCode in ['c', 'C']:
            self.SetTrackStyleToCamera()
#            self.EventCallbackCommand.SetAbortFlag(1)
        elif keyCode in ['a', 'A']:
            self.SetTrackStyleToActor()
#            self.EventCallbackCommand.SetAbortFlag(1)
        else:
            vtkPythonInteractorStyleTrackballCamera.OnChar(self)
    #===========================================================================
    # These methods for the different interactions in different modes
    # are overridden in subclasses to perform the correct motion. Since
    # they are called by OnTimer, they do not have mouse coord parameters
    # (use interactor's GetEventPosition and GetLastEventPosition)    
    #===========================================================================
    def Rotate(self):
        '''
        '''
        if self.CurrentRenderer == None:
            return
        
        if ( (self.getTrackStyle()==self.TrackStyleActor) and self.__InteractionProp):
            if self.CurrentRenderer == None or self. __InteractionProp == None:
                return
        
            rwi = self.GetInteractor()
            cam = self.CurrentRenderer.GetActiveCamera()
            
    #        First get the origin of the assembly
            obj_center = self.__InteractionProp.GetCenetr()
            
    #        GetLength gets the length of the diagonal of the bounding box
            boundRadius = self.__InteractionProp.GetLength()*0.5
            
    #        Get the view up and view right vectors
            view_up = [0.0]*3
            view_look = [0.0]*3
            view_right = [0.0]*3
            
            cam.OrthogonalizeViewUp()
            cam.ComputeViewPlaneNormal()
            cam.GetVewUp(view_up)
            vtk.vtkMath.Normalize(view_up)
            cam.GetViewPlaneNormal(view_look)
            vtk.vtkMath.Cross(viewup, view_look, viewright)
            vtk.vtkMath.Normalize(view_right)
            
    #        Get the furtherest point from object position+origin
            outsidept = [0.0]*3
            
            outsidept[0] = obj_center[0]+view_right[0]*boundRadius
            outsidept[1] = obj_center[1]+view_right[1]*boundRadius
            outsidept[2] = obj_center[2]+view_right[2]*boundRadius
            
    #        Convert them to display coord
            disp_obj_center = [0.0]*3
            disp_obj_center = self.ComputeWorldToDisplay(obj_center[0], 
                                                         obj_center[1], 
                                                         obj_center[2], 
                                                         disp_obj_center)
            outsidept = self.ComputeWorldToDisplay1( outsidept[0], 
                                                     outsidept[1], 
                                                     outsidept[2], 
                                                     outsidept)
            radius = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(disp_obj_center, outsidept))
            
            nxf = (rwi.GetEventPosition()[0]-disp_obj_center[0])/radius
            
            nyf = (rwi.GetEventPosition()[1]-disp_obj_center[1])/radius
            
            oxf = (rwi.GetLastEventPosition()[0]-disp_obj_center[0])/radius
            
            oyf = (rwi.GetLastEventPosition()[1]-disp_obj_center[1])/radius
            
            if ( (nxf*nxf+nyf*nyf)<=1.0) and ((oxf*oxf+oyf*oyf)<=1.0):
                newXAngle = vtk.vtkMath.DegreesFromRadians(math.asin(nxf))
                newYAngle = vtk.vtkMath.DegreesFromRadians(math.asin(nyf))
                oldXAngle = vtk.vtkMath.DegreesFromRadians(math.asin(oxf))
                oldYAngle = vtk.vtkMath.DegreesFromRadians(math.asin(oyf))
                
                scale = [0.0]*3
                scale[0] = scale[1] = scale[2] = 1.0
                
                rotate = [[newXAngle-oldXAngle, view_up[0], view_up[1], view_up[2]],
                          [oldYAngle-newYAngle, view_right[0], view_right[1], view_right[2]]]
                
                self.Prop3DTransform(self.__InteractionProp, obj_center, 2, rotate, scale)
                
                if self.AutoAdjustCameraClippingRange:
                    self.CurrentRenderer.ResetCameraClippingRange()
                
                rwi.Render()
        else:
            vtkPythonInteractorStyleTrackballCamera.Rotate(self)
            
    def Spin(self):
        '''
        '''
        if self.CurrentRenderer == None:
            return
        
        if ( (self.getTrackStyle()==self.TrackStyleActor) and self.__InteractionProp):
            if self.CurrentRenderer == None or self. __InteractionProp == None:
                return
        
            rwi = self.GetInteractor()
            cam = self.CurrentRenderer.GetActiveCamera()
            # Get the axis to rotate around = vector from eye to origin
            obj_center = self.__InteractionProp.GetCenter()
            
            motion_vector = [0.0]*3
            view_point = [0.0]*3
            
            if cam.GetParallelProjection():
                # If parallel projection, want to get the view plane normal...
                cam.ComputeViewPlaneNormal()
                cam.GetViewPlaneNormal(motion_vector)
            else:
                # Perspective projection, get vector from eye to center of actor
                cam.GetPosition(view_point)
                motion_vector[0] = view_point[0] - obj_center[0]
                motion_vector[1] = view_point[1] - obj_center[1]
                motion_vector[2] = view_point[2] - obj_center[2]
                vtk.vtkMath.Normalize(motion_vector)
            
            disp_obj_center = [0.0]*3
            
            disp_obj_center = self.ComputeWorldToDisplay(obj_center[0], obj_center[1],
                                                          obj_center[1],disp_obj_center)
            
            newAngle = math.atan2(rwi.GetEventPosition()[1]-disp_obj_center[1], 
                             rwi.GetEventPosition()[0]-disp_obj_center[0])
            oldAngle = math.atan2(rwi.GetLastEventPosition()[1]-disp_obj_center[1], 
                             rwi.GetLastEventPosition()[0]-disp_obj_center[0])
            
            newAngle = vtk.vtkMath.DegreesFromRadians(newAngle)
            oldAngle = vtk.vtkMath.DegreesFromRadians(oldAngle)
            
            scale = [1.0]*3
            
            rotate = [[newAngle-oldAngle, motion_vector[0], motion_vector[1], motion_vector[2]]]
            
            self.Prop3DTransform(self.__InteractionProp, obj_center, 1, rotate, scale)
            if self.AutoAdjustCameraClippingRange:
                self.CurrentRenderer.ResetCameraClippingRange()
                
            rwi.Render()
        else:
            vtkPythonInteractorStyleTrackballCamera.Spin(self)
                
            
       
       
    def Pan(self):
        '''
        '''
        if self.CurrentRenderer == None:
            return
        
        if ( (self.getTrackStyle()==self.TrackStyleActor) and self.__InteractionProp):
            if self.CurrentRenderer == None or self. __InteractionProp == None:
                return
            rwi = self.GetInteractor()
            
#            Use initial center as the origin from which to pan
            obj_center = self.__InteractionProp.GetCenter()
            disp_obj_center = [0.0]*3
            new_pick_point = [0.0]*3
            old_pick_point = [0.0]*4
            motion_vector = [0.0]*3
            
            self.ComputeWorldToDisplay(obj_center[0], obj_center[1], obj_center[2],
                                       disp_obj_center)
            self.ComputeDisplayToWorld(rwi.GetEventPosition()[0],
                                       rwi.GetEventPosition()[1],
                                       disp_obj_center[2],
                                       new_pick_point)
            self.ComputeDisplayToWorld(rwi.GetLastEventPosition()[0],
                                       rwi.GetLastEventPosition()[1],
                                       disp_obj_center[2],
                                       old_pick_point)
            
            motion_vector[0] = new_pick_point[0] - old_pick_point[0]
            motion_vector[1] = new_pick_point[1] - old_pick_point[1]
            motion_vector[2] = new_pick_point[2] - old_pick_point[2]
            
            if self.__InteractionProp.GetUserMatrix() <> None:
                t = vtk.vtkTransform()
                t.PostMultiply()
                t.SetMatrix(self.__InteractionProp.GetUserMatrix())
                t.Translate(motion_vector[0], motion_vector[1], motion_vector[2])
                self.__InteractionProp.GetUserMatrix().DeepCopy(t.GetMatrix())
#                del t
            else:
                self.__InteractionProp.AddPosition(motion_vector[0],
                                                   motion_vector[1],
                                                   motion_vector[2])
            if self.AutoAdjustCameraClippingRange:
                self.CurrentRenderer.ResetCameraClippingRange()
                
            rwi.Render()
        else:
            vtkPythonInteractorStyleTrackballCamera.Pan(self)
    
    def SetTrackStyleToCamera(self):
        self.setTrackStyle(self.TrackStyleCamera)
    
    def SetTrackStyleToActor(self):
        self.setTrackStyle(self.TrackStyleActor)
    
    def FindPickedActor(self, x, y):
        '''
        @param x: int
        @param y: int
        @return: None
        '''
        self.__InteractionPicker.Pick(x, y, 0.0, self.CurrentRenderer)
        prop = self.__InteractionPicker.GetViewProp()
        
        if prop<>None:
            self.__InteractionProp = vtk.vtkProp3D.SafeDownCast(prop)
        else:
            self.__InteractionProp = None
    
    def Prop3DTransform(self, prop3D, boxCenter, numRotation, rotate, scale):
        '''
        @param prop3D: vtkProp3D 
        @param boxCenter: double[]
        @param numRotation: int
        @param rotate: double[][]
        @param scale: double    
        '''
        oldMatrix = vtk.vtkMatrix4x4()
        prop3D.GetMatrix(oldMatrix)
        
        orig = [0.0]*3
        prop3D.GetOrigin(orig)
        newTransform = vtk.vtkTransform()
        newTransform.PostMultiply()
        if prop3D.GetUserMatrix()<>None:
            newTransform.SetMatrix(prop3D.GetUserMatrix())
        else:
            newTransform.SetMatrix(oldMatrix)
        
        newTransform.Translate(-(boxCenter[0]), -(boxCenter[1]), -(boxCenter[2]))
        
        for i in range(numRotation):
            newTransform.RotateWXYZ(rotate[i][0], rotate[i][1], rotate[i][2], rotate[i][3])
        
        if ((scale[0]*scale[1]*scale[2])<>0.0):
            newTransform.Scale(scale[0], scale[1], scale[2])
        
        newTransform.Translate(boxCenter[0], boxCenter[1], boxCenter[2])
        
        # now try to get the composit of translate, rotate, and scale
        newTransform.Translate(-(orig[0]), -(orig[1]), -(orig[2]))
        newTransform.PreMultiply()
        newTransform.Translate(orig[0], orig[1], orig[2])
        
        if prop3D.GetUserMatrix()<>None:
            newTransform.SetMatrix(prop3D.GetUserMatrix())
#            newTransform.GetMatrix(prop3D.GetUserMatrix()) # ?????
        else:
            prop3D.SetPosition(newTransform.GetPosition())
            prop3D.SetScale(newTransform.GetScale())
            prop3D.SetOrientation(newTransform.GetOrientation())
        
    def getTrackStyle(self):
        return self.__TrackStyle


    def getInteractionPicker(self):
        return self.__InteractionPicker


    def getInteractionProp(self):
        return self.__InteractionProp


    def setTrackStyle(self, value):
        if value<self.TrackStyleCamera or value>self.TrackStyleCamera:
            return
        self.__TrackStyle = value


    def setInteractionPicker(self, value):
        self.__InteractionPicker = value


    def setInteractionProp(self, value):
        self.__InteractionProp = value

if __name__=="__main__":
   
    print "fuck"
    
        