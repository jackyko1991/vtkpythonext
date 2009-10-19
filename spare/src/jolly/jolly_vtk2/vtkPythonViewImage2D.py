'''
Created on 2009-10-13

@author: summit
'''
from jolly.jolly_vtk2.vtkPythonViewImage import *
from jolly.jolly_vtk2.vtkPythonInteractorStyleImage2D import *
from jolly.jolly_vtk2.vtkPythonViewImage2DCommand import *

class vtkPythonViewImage2D(vtkPythonViewImage):
    '''
     Description:
     The orientation of the view is a abstract representation of the object
     we are looking at. It results from the acquisition plane. Setting the View
     Orientation by calling SetViewOrientation() will imply the view to set its
     inner "slice" orientation. (slice orientation == 2 means plane of acquisition.)

     IMPORTANT NOTE:

     The view orientations defined here are orthogonal to the normal basis
     in the scanner. A very interesting improvement would be to define "oblique"
     view orientations for cardiac imaging, something like:

     VIEW_ORIENTATION_SHORT_AXIS, VIEW_ORIENTATION_LONG_AXIS, and VIEW_ORIENTATION_FOUR_CHAMBER
     could define the different views that are usually used in cardiac imaging.

     From this user-input information, the idea would be to evaluate which slice
     orientation does correspond to the requested view. This can be done by evaluating the
     dot product between the axis of acquisition and a pre-defi
    '''
    
    VIEW_ORIENTATION_SAGITTAL = 0
    VIEW_ORIENTATION_CORONAL = 1
    VIEW_ORIENTATION_AXIAL = 2
    
    VIEW_CONVENTION_RADIOLOGICAL = 0
    VIEW_CONVENTION_NEUROLOGICAL = 1
    
    #===========================================================================
    # These types describe the behaviour
    # of the interactor style.
    #===========================================================================
    INTERACTOR_STYLE_NAVIGATION = 0
    INTERACTOR_STYLE_RUBBER_ZOOM = 1
    
    def __init__(self):
        '''
        Constructor
        '''
        vtkPythonViewImage.__init__(self)
        
        self.__ConventionMatrix = vtk.vtkMatrix4x4()
        self.__SliceImplicitPlane = vtk.vtkPlane()
        self.__AdjustmentTransform = vtk.vtkTransform()
        self.__SlicePlane = vtk.vtkPolyData()
        # self.__OrientationAnnotation = vtkOrientationAnnotation()
        
        self.__InteractorStyleSwitcher = None
        self.__InteractorStyleRubberZoom = None
        
        self.__Command = vtkPythonViewImage2DCommand()
        self.__Command.setViewer(self)
        
        self.__AdjustmentTransform.Identity()
        self.__SliceImplicitPlane.SetOrigin(0,0,0)
        self.__SliceImplicitPlane.SetNormal(1,1,1)
        
        #self.__OrientationAnnotation.SetNonlinearFontScaleFactor(0.25)
        #self.__OrientationAnnotation.SetTextProperty(self.__TextProperty())
        
        self.__ViewOrientation = self.VIEW_ORIENTATION_AXIAL
        self.__ViewConvention = self.VIEW_CONVENTION_RADIOLOGICAL
        self.__InteractorStyleType = self.INTERACTOR_STYLE_NAVIGATION  
        self.__ViewCenter = [0,0,0]
        
        self.__ConventionMatrix.Zero()
        self.__ConventionMatrix.SetElement(2, 0, 1)
        self.__ConventionMatrix.SetElement(2, 1, 1)
        self.__ConventionMatrix.SetElement(1, 2, -1)
        self.__ConventionMatrix.SetElement(0, 3, 1)
        self.__ConventionMatrix.SetElement(1, 3, -1)
        self.__ConventionMatrix.SetElement(2, 3, -1)
        
        #self.__Renderer.AddViewProp(self.__OrientationAnnotation)
        
        self.__CursorGenerator = vtk.vtkCursor2D()
        self.__CursorGenerator.AllOff()
        self.__CursorGenerator.AxesOn()
        self.__CursorGenerator.SetRadius(3)
        self.__CursorGenerator.SetModelBounds(-40, 40, -40, 40, 0, 0)
        
        self.__Cursor = vtk.vtkPointHandleRepresentation2D()
        self.__Cursor.ActiveRepresentationOff()
        self.__Cursor.SetCursorShape(self.__CursorGenerator.GetOutput())
        self.__Cursor.GetProperty().SetColor(0.9, 0.9, 0.1)
        
        self.GetRenderer().AddViewProp(self.__Cursor)
        
        self.ShowAnnotationsOn()
        self.InitializeSlicePlane()
        
        self.__SliceAndWindowInformation = ""
        self.__ImageInformation = ""
        
      

    def SetWorldCoordinates(self, pos):
        '''
         The wolrd is not always what we think it is ...

         Use this method to move the viewer slice such that the position
         (in world coordinates) given by the arguments is contained by
         the slice plane. If the given position is outside the bounds
         of the image, then the slice will be as close as possible.
         @param pos: double[3]
         @return None
        '''
        self.SetSlice(self.GetSliceForWorldCoordinates(pos))
    
    def SetSlice(self, slice):
        '''
        Set/Get the current slice to display (depending on the orientation 
         this can be in X, Y or Z).
    
         This method has been overriden in order to generalize the use of this class
         to 2D AND 3D scene visualization. In the 2D case, it is an important method.
         @param slice: int
         @return: None 
        '''
        cam = None
        if self.GetRenderer() <> None:
            cam = self.GetRenderer().GetActiveCamera()
        if cam == None:
            return 
        range = [0]*2
        self.GetSliceRange(range)
        if range:
            if slice < range[0]:
                slice = range[0]
            elif slice > range[1]:
                slice = range[1]
        if self.GetSlice() == slice:
            return
        vtk.vtkImageViewer2.SetSlice(self, slice)
        self.Modified()
        
        pos = self.GetWorldCoordinatesForSlice(slice)
        self.__SliceImplicitPlane.SetOrigin(pos[0:3])
        
        self.UpdateDisplayExtent()
        self.UpdateCenter()
        self.UpdateSlicePlane()
        
    def SetOrientationMatrix(self, matrix):
        '''
        Instead of setting the slice orientation to an axis (YZ - XZ - XY),
         you can force the view to be axial (foot-head), coronal (front-back),
         or sagittal (left-right). It will just use the OrientationMatrix
         (GetOrientationMatrix()) to check which slice orientation to pick.
         @param matrix: vtkMatrix4x4
         @return: None
        '''
        vtkPythonViewImage.setOrientationMatrix(self, matrix)
        self.UpdateOrientation()
    
    def GetWorldCoordinatesForSlice(self, slice):
        '''
        Convert an indices coordinate point (image coordinates) into a world coordinate point
        @param slice: int
        @return: double[3] 
        '''
        indices = [0]*3
        indices[self.GetSliceOrientation()] = slice
        return self.GetWorldCoordinatesFromImageCoordinates(indices)
    
    def GetSliceForWorldCoordinates(self, pos):
        '''
        Convert a world coordinate point into an image indices coordinate point
        @param pos: double[3]
        @return: int 
        '''
        indices = self.GetImageCoordinatesFromWorldCoordinates(pos)
        return indices[self.GetSliceOrientation()]
        
    def ResetPosition(self):  
        '''
        Reset the 3D position to center
        @return: None
        '''
        
        if not self.GetInput():
            return 
        range = [0]*2
        self.GetSliceRange(range)
        self.SetSlice(vtk.vtkMath.Round(float(range[1]-range[0])/2.0))
        
    def Reset(self):
        '''
         Reset position - zoom - window/level to default
        '''
        vtkPythonViewImage.Reset(self)
        self.ResetPosition()
    
    def GetWorldCoordinatesFromDisplayPositionByArray(self, xy):
        '''
        @param xy: int[2] 
        @return: double[3]
        '''
        if not self.GetInput() or not self.GetRenderer():
            return [0.0,0.0,0.0]
        slicepos = self.GetWorldCoordinatesForSlice(self.GetSlice())
        self.GetRenderer().SetWorldPoint(slicepos)
        self.GetRenderer().WorldToDisplay()
        self.GetRenderer().SetDisplayPoint(xy[0], xy[1], self.GetRenderer().GetDisplayPoint()[2])
        self.GetRenderer().DisplayToWorld()
        return self.GetRenderer().GetWorldPoint()
    
    
    
    def GetWorldCoordinatesFromDisplayPosition(self, x, y):  
        '''
        @param x: int
        @param y: int
        @return: double[3]  
        '''
        self.GetWorldCoordinatesFromDisplayPositionByArray([x,y])
        
    def getSliceImplicitPlane(self):
        '''
        The SliceImplicitPlane instance (GetImplicitSlicePlane()) is the
         implicit function that cuts every dataset that is added with AddDataSet().
         @return: vtkPlane
        '''
        return self.__SliceImplicitPlane
    
    def SetInterpolate(self, val):
        if self.GetImageActor():
            self.GetImageActor().SetInterpolate(val)
    
    def GetInterpolate(self):
        '''
        @return: int
        '''
        if self.GetImageActor():
            return self.GetImageActor().GetInterpolate()
        return 0
    
    def InterpolateOn(self):
        self.SetInterpolate(True)
    
    def InterpolateOff(self):    
        self.SetInterpolate(False)
        
    def AddDataSet(self, dataset, property=None):
        '''
        Add a dataset to the view (has to be subclass of vtkPointSet).
        The dataset will be cut through the implicit slice plane
        (GetImplicitSlicePlane()).
    
        This results in a loss of dimensionality, i.e. tetrahedron will be displayed
        as triangles, triangles as lines, lines as points.
        A vtkProperty of the dataset can be specified.
        @param dataset: vtkDataSet
        @param property: vtkProperty
        @return vtkActor 
        '''
        if not dataset or self.getDataSetCollection().IsItemPresent(dataset):
            return None
        if vtk.vtkImageData.SafeDownCast(dataset):
            self.SetInput(vtk.vtkImageData.SafeDownCast(dataset))
            return None
        
        cam = None
        if self.GetRenderer() <> None:
            cam = self.GetRenderer().GetActiveCamera()
        if cam == None:
            return
        
        cutter = vtk.vtkCutter()
        cutter.SetInputConnection(0, dataset.GetProducerPort())
        cutter.SetCutFunction(self.__SliceImplicitPlane)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(0, cutter.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        if property:
            actor.SetProperty(property)
        
        actor.SetUserTransform(self.__AdjustmentTransform)
        self.GetRenderer().AddViewProp(actor)

        self.getDataSetCollection().AddItem(dataset)
        self.getProp3DCollection().AddItem(actor)
        
#        Returning the actor is a little bit odd.
#       Even if its referencing count has been decreased above,
#       the instance still exist, actor is not NULL.
#       However, this is not the best way to do so.
        return actor
        
        
    def setShowAnnotations(self, value):
        '''
        Show/Hide the annotations.
        '''
        vtkPythonViewImage.setShowAnnotations(self, value)
#        self.__OrientationAnnotation.SetVisibility(value)

    def GetViewCenter(self):
        '''
        @return: double[3]
        '''
        pass
    def Update(self):
        self.UpdateOrientation()
        pass
    
    def PostUpdateOrientation(self):
        '''
        @return: None
        '''
        axis = self.SetCameraFromOrientation()
        self.__ViewOrientation = axis
        
        self.UpdateCenter()
        
        self.SetAnnotationsFromOrientation()
        self.SetImplicitPlaneFromOrientation()
        self.SetSlicePlaneFromOrientation()
    
    def SetLeftButtonInteractionStyle(self, arg):
        '''
        @param arg: int 
        '''
        if self.__InteractorStyle:
            self.__InteractorStyle.SetLeftButtonInteractionStyle(arg)
    
    def SetRightButtonInteractionStyle(self, arg):       
        '''
        @param arg: int 
        '''
        if self.__InteractorStyle:
            self.__InteractorStyle.SetRightButtonInteraction(arg)
    
    def SetMiddleButtonInteractionStyle(self, arg): 
        '''
        @param arg: int
        '''
        if self.__InteractorStyle:
            self.__InteractorStyle.SetMiddleButtonInteraction(arg)
    
    def SetWheelInteractionStyle(self, arg):
        '''
        @param arg: int
        '''
        if self.__InteractorStyle:
            self.__InteractorStyle.SetWheelInteractionStyle(arg)
    
    def SetInteractionStyle(self, arg):
        '''
        @param arg: int
        '''
        self.SetLeftButtonInteractionStyle(arg)
        self.SetRightButtonInteractionStyle(arg)
        self.SetMiddleButtonInteractionStyle(arg)
        self.SetWheelInteractionStyle(arg)
    
    def GetInteractionStyle(self):
        '''
        @return: int
        '''
        if self.__InteractorStyle:
            return self.__InteractorStyle.GetLeftButtonInteraction()
        else:
            return 0
    
    def UpdateCursor(self, XY):
        '''
        @param XY: int[2]
        @return: None
        '''
        xy = [XY[0], XY[1], 0]
        self.getCursor().SetDisplayPosition(xy)
        
        position = self.GetWorldCoordinatesFromDisplayPositionByArray(XY)
        
        os = "%s\nXYZ:  %4.2f, %4.2f, %4.2f mm\nValue: %g" % (self.__ImageInformation,
                                                              position[0], position[1], position[2],
                                                              self.GetValueAtPosition(position))
        self.getCornerAnnotation().SetText(2,os)
        
    def UpdateSlicePlane(self):
        '''
        @return None
        '''
        oldpoints = vtk.vtkPoints()
        points = vtk.vtkPoints()
        x = [0.0]*3
        bounds = [0.0]*6
        self.GetImageActor().GetDisplayBounds(bounds)
        added1 = 0
        added2 = 0
        for i in range(4):
            if not i%2:
                added1 = 1
            else:
                added1 = 0
            if i<2:
                added2 = 1
            else:
                added2 = 0
            x[(self.GetSliceOrientation()+1)%3] = bounds[2*((self.GetSliceOrientation()+1)%3)+added1]
            x[(self.GetSliceOrientation()+2)%3] = bounds[2*((self.GetSliceOrientation()+2)%3)+added2]
            x[self.GetSliceOrientation()] = bounds[2*self.GetSliceOrientation()]
            oldpoints.InsertPoint(i, x)
        self.getOrientationTransform().TransformPoints(oldpoints, points)
       
        self.__SlicePlane.SetPoints(points)
        del oldpoints
        del points
    
    def UpdateCenter(self):
        '''
        @return None
        '''
        if self.GetInput() == None:
            return
        
        cam = None
        if self.GetRenderer() <> None:
            cam = self.GetRenderer().GetActiveCamera()
        if cam == None:
            return 
        
        dimensions = self.GetInput().GetDimensions()
        
        indices = [0]*3
        for i in range(3):
            indices[i] = int(float(dimensions[i])/2.0)
        indices[self.GetSliceOrientation()] = self.GetSlice()
        center = self.GetWorldCoordinatesFromImageCoordinates(indices)
        self.__ViewCenter = center[i]
        
    def UpdateOrientation(self):
        '''
        @return None
        '''
        
        # Python vtk wrap could not invoke the protected member function
        # So we reset the orientation to asked vtkImageView2 for  UpdateOrientation
        self.SetSliceOrientation(self.GetSliceOrientation ())
        # vtkPythonViewImage.UpdateOrientation()
        self.PostUpdateOrientation()
    
    def SetSlicePlaneFromOrientation(self):
        '''
        @return: None
        '''
#         These lines tell the slice plane which color it should be
#         We should allow more colors...
        vals = [0.0]*3
        vals[self.__ViewOrientation] = 255
        array = self.__SlicePlane.GetPointData().GetScalars()
       
        if not array:
            return
        array.InsertComponent(0,0,vals[0])
        array.InsertComponent(0,1,vals[1])
        array.InsertComponent(0,2,vals[2])
        array.InsertComponent(1,0,vals[0])
        array.InsertComponent(1,1,vals[1])
        array.InsertComponent(1,2,vals[2])
        array.InsertComponent(2,0,vals[0])
        array.InsertComponent(2,1,vals[1])
        array.InsertComponent(2,2,vals[2])
        array.InsertComponent(3,0,vals[0])
        array.InsertComponent(3,1,vals[1])
        array.InsertComponent(3,2,vals[2])
       
            
    def SetCameraFromOrientation(self):
        '''
        @return: int
        '''
#        The camera has already been set as if the image has no orientation.
#        So we just have to adjust its position and view up according
#        to the image orientation and conventions.
        cam = None
        if self.GetRenderer() <> None:
            cam = self.GetRenderer().GetActiveCamera()
        if cam == None:
            return -1
        
#        First recover information from the camera.
#        Recover also information from the convention matrix
        position = [0.0]*4
        focalpoint = [0.0]*4
        conventionposition = [0.0]*4
        conventionview = [0.0]*4
        viewup = [0.0]*4
        focaltoposition = [0.0]*3
        first = [0.0]*3
        second = [0.0]*3
        third = [0.0]*3
        fourth = [0.0]*3
        viewupchoices = []
        
        for i in range(3):
            position[i] = cam.GetPosition()[i]
            focalpoint[i] = cam.GetFocalPoint()[i]
            conventionposition[i] = self.__ConventionMatrix.GetElement(i, 3)
            conventionview[i] = self.__ConventionMatrix.GetElement(i, self.GetSliceOrientation())
        
        position[3] = 1
        focalpoint[3] = 1
        conventionview[3] = 0
        viewup[3] = 0
#        Apply the orientation matrix to all this information
        if self.getOrientationMatrix():
            self.getOrientationMatrix().MultiplyPoint(position, position)
            self.getOrientationMatrix().MultiplyPoint(focalpoint, focalpoint)
            self.getOrientationMatrix().MultiplyPoint(conventionview, conventionview)
            self.getOrientationMatrix().MultiplyPoint(conventionposition, conventionposition)
            
            
#        Compute the vector perpendicular to the view
        for i in range(3):
            focaltoposition[i] = position[i] - focalpoint[i]
            
#        Deal with the position :
#        invert it if necessary (symetry among the focal point)
        inverseposition = (vtk.vtkMath.Dot(focaltoposition, conventionposition[0:3])<0)
        if inverseposition:
            for i in range(3):
                position[i] = position[i] - 2*focaltoposition[i]
        
#         Now we now we have 4 choices for the View-Up information
        for i in range(3):
            first[i] = conventionview[i]
            second[i] = -conventionview[i]
        
        vtk.vtkMath.Cross(first, focaltoposition, third)
        vtk.vtkMath.Cross(second, focaltoposition, fourth)
        vtk.vtkMath.Normalize(third)
        vtk.vtkMath.Normalize(fourth)
        
        viewupchoices.append(first)
        viewupchoices.append(second)
        viewupchoices.append(third)
        viewupchoices.append(fourth)
        
#        To choose between these choices, first we find the axis
#        the closest to the focaltoposition vector
        id = 0
        dot = 0
        for i in range(3):
            if dot < abs(focaltoposition[i]):
                dot = abs(focaltoposition[i])
                id = i
        
#        Then we choose the convention matrix vector correspondant to the
#        one we just found
        for i in range(3):
            conventionview[i] = self.__ConventionMatrix.GetElement(i, id)
        
#        Then we pick from the 4 solutions the closest to the
#        vector just found
        id2 = 0
        dot2 = 0
        
        for i in range(len(viewupchoices)):
            if dot2 < vtk.vtkMath.Dot(viewupchoices[i], conventionview[0:3]):
                dot2 = vtk.vtkMath.Dot(viewupchoices[i], conventionview[0:3])
                id2 = i
                
#        We found the solution
        for i in range(3):
            viewup[i] = viewupchoices[id2][i]
        
        cam.SetPosition(position[0], position[1], position[2])
        cam.SetFocalPoint(focalpoint[0], focalpoint[1], focalpoint[2])
        cam.SetViewUp(viewup[0], viewup[1], viewup[2])
        
        return id
        
    def SetAnnotationsFromOrientation(self):
        '''
        @return: None
        '''
#        This method has to be called after the camera
#        has been set according to orientation and convention.
#        We rely on the camera settings to compute the oriention
#        annotations.
        cam = None
        if self.GetRenderer() <> None:
            cam = self.GetRenderer().GetActiveCamera()
        if cam == None:
            return
        matrix = [("R", "L"),("A, P"), ("I", "S")]
        solution = ["","","", ""]
        
#        surely there is a simpler way to do all of that !
        viewup = cam.GetViewUp()
        normal = cam.GetViewPlaneNormal()
        rightvector = [0.0]*3
        vtk.vtkMath.Cross(normal, viewup, rightvector)
        
        id1 = 0
        id2 = 0
        id3 = 0
        dot1 = 0.0
        dot2 = 0.0
        dot3 = 0.0
        for i in range(3):
            if dot1 <= abs(viewup[i]):
                dot1 = abs(viewup[i])
                id1 = i
            if dot2 <= abs(rightvector[i]):
                dot2 = abs(rightvector[i])
                id2 = i
            if dot3 <= abs(normal[i]):
                dot3 = abs(normal[i])
                id3 = i
        if viewup[id1]>0:
            solution[3] = matrix[id1][0]
            solution[1] = matrix[id1][1]
        else:
            solution[3] = matrix[id1][1]
            solution[1] = matrix[id1][0]
        if rightvector[id2]>0:
            solution[0] = matrix[id2][0]
            solution[2] = matrix[id2][1]
        else:
            solution[0] = matrix[id2][1]
            solution[2] = matrix[id2][0]
#        for i in range(4):
#            self.__OrientationAnnotation.SetText(i, solution[i])
        if self.GetInput():
#            naively the X and Y axes of the current view
#            correspond to the rightvector and the viewup respectively.
#            But in fact we have to put those vectors back in the image
#            coordinates and see to which xyz image axis they correspond.
            Xaxis = [0.0, 0.0, 0.0, 0.0]
            Yaxis = [0.0, 0.0, 0.0, 0.0]
            for i in range(3):
                Xaxis[i] = rightvector[i]
                Yaxis[i] = viewup[i]
            
            inverse = vtk.vtkMatrix4x4()
            inverse.Identity()
            if self.getOrientationMatrix():
                vtk.vtkMatrix4x4.Invert(self.getOrientationMatrix(), inverse)
            inverse.MultiplyPoint(Xaxis, Xaxis)
            inverse.MultiplyPoint(Yaxis, Yaxis)
            del inverse
            
            dotX = 0.0
            dotY = 0.0
            idX = 0
            idY = 0
            for i in range(3):
                if dotX <= abs(Xaxis[i]):
                    dotX = abs(Xaxis[i])
                    idX = i
                if dotY <= abs(Yaxis[i]):
                    dotY = abs(Yaxis[i])
                    idY = i
            dimensions = self.GetInput().GetDimensions()
            spacing = self.GetInput().GetSpacing()
            self.__ImageInformation = "Image Size:  %i x %i\nVoxel Size: %g x %g mm" % \
                                        (dimensions[idX], dimensions[idY],
                                         spacing[idX], spacing[idY])
            self.__SliceAndWindowInformation = "<slice_and_max>\n<window>\n<level>"
            
            self.getCornerAnnotation().SetText(2, self.__ImageInformation)
            self.getCornerAnnotation().SetText(3, self.__SliceAndWindowInformation)
            
    
    def SetImplicitPlaneFromOrientation(self):
        '''
        @return: None
        '''
        cam = None
        if self.GetRenderer() <> None:
            cam = self.GetRenderer().GetActiveCamera()
        if cam == None:
            return 
        
        position = cam.GetPosition()
        focalpoint = cam.GetFocalPoint()
        focaltoposition = [0.0]*3
        for i in range(3):
            focaltoposition[i] = position[i] - focalpoint[i]
        
        self.__SliceImplicitPlane.SetNormal(focaltoposition)
        
#        these lines are meant to fix the bug that make the line
#        actor (and other added dataset) appear behind the 2D scene...
        normal = cam.GetViewPlaneNormal()
        translation = [0.0]*3
        for i in range(3):
            translation[i] = 0.01*normal[i]
        self.__AdjustmentTransform.Identity()
        self.__AdjustmentTransform.Translate(translation)
        
    def InitializeSlicePlane(self):
        '''
        @return: None
        '''
        self.__SlicePlane.SetPolys(vtk.vtkCellArray())
        points = vtk.vtkPoints()
        self.__SlicePlane.SetPoints(points)
        points.InsertNextPoint(0, 0, 0)
        points.InsertNextPoint(1, 0, 0)
        points.InsertNextPoint(0, 1, 0)
        points.InsertNextPoint(1, 1, 0)
        
        
        pts = vtk.vtkIdList()
        pts.InsertNextId(0)
        pts.InsertNextId(1)
        pts.InsertNextId(2)
        self.__SlicePlane.InsertNextCell(vtk.VTK_POLYGON,  pts)
        pts.Reset()
        pts.InsertNextId(1)
        pts.InsertNextId(2) #???
        pts.InsertNextId(3)
        self.__SlicePlane.InsertNextCell(vtk.VTK_POLYGON,  pts)
        pts.Reset()
        pts.InsertNextId(0)
        pts.InsertNextId(1) #???
        pts.InsertNextId(3)
        self.__SlicePlane.InsertNextCell(vtk.VTK_POLYGON,  pts)
        pts.Reset()
        pts.InsertNextId(0)
        pts.InsertNextId(2) #???
        pts.InsertNextId(3)
        self.__SlicePlane.InsertNextCell(vtk.VTK_POLYGON,  pts)
        #del points
        
        array = vtk.vtkUnsignedCharArray()
        array.SetName("Colors")
        array.SetNumberOfComponents(3)
        array.InsertComponent(0,0,255)
        array.InsertComponent(0,1,0)
        array.InsertComponent(0,2,0)
        array.InsertComponent(1,0,255)
        array.InsertComponent(1,1,0)
        array.InsertComponent(1,2,0)
        array.InsertComponent(2,0,255)
        array.InsertComponent(2,1,0)
        array.InsertComponent(2,2,0)
        array.InsertComponent(3,0,255)
        array.InsertComponent(3,1,0)
        array.InsertComponent(3,2,0)

        self.__SlicePlane.GetPointData().SetScalars(array)
        
        #del array
        
    def InstallPipeline(self):
        '''
        @return: None
        '''
        if self.GetRenderWindow() and self.GetRenderer():
            self.GetRenderWindow().AddRenderer(self.GetRenderer())
        if self.GetInteractor():
            if self.getInteractorStyleType() == self.INTERACTOR_STYLE_NAVIGATION:
                if (not self.__InteractorStyleSwitcher or 
                    not isinstance(self.__InteractorStyleSwitcher, vtkPythonViewImage2D)):
                    self.__InteractorStyleSwitcher = vtkPythonInteractorStyleImage2D()
                    self.GetInteractor().SetInteractorStyle(None)
                    self.__InteractorStyleSwitcher.SetPriority(1.0)
                    
                    self.__InteractorStyleSwitcher.AddObserver("UserEvent", lambda obj,event:self.__Command.Execute(obj,"UserEvent", self.__InteractorStyleSwitcher))
                    self.__InteractorStyleSwitcher.AddObserver("UserEvent", lambda obj,event:self.__Command.Execute(obj,"UserEvent", self.__InteractorStyleSwitcher))
                    
                    self.__InteractorStyleSwitcher.AddObserver("UserEvent", lambda obj,event:self.__Command.Execute(obj,"UserEvent", self.__InteractorStyleSwitcher))
                    self.__InteractorStyleSwitcher.AddObserver("UserEvent", lambda obj,event:self.__Command.Execute(obj,"UserEvent", self.__InteractorStyleSwitcher))
                    self.__InteractorStyleSwitcher.AddObserver("StartWindowLevelEvent", lambda obj,event:self.__Command.Execute(obj,"StartWindowLevelEvent", self.__InteractorStyleSwitcher))
                    self.__InteractorStyleSwitcher.AddObserver("WindowLevelEvent", lambda obj,event:self.__Command.Execute(obj,"WindowLevelEvent", self.__InteractorStyleSwitcher))
                    self.__InteractorStyleSwitcher.AddObserver("CharEvent", lambda obj,event:self.__Command.Execute(obj,"CharEvent", self.__InteractorStyleSwitcher))
                    self.__InteractorStyleSwitcher.AddObserver("ResetWindowLevelEvent", lambda obj,event:self.__Command.Execute(obj,"ResetWindowLevelEvent", self.__InteractorStyleSwitcher))
                
    #                We don't observe the ResetWindowLevelEvent because it is already
    #                included in the ResetViewerEvent.
                #self.__InteractorStyleSwitcher = self.GetInteractorStyle()
            elif self.getInteractorStyleType() == self.INTERACTOR_STYLE_RUBBER_ZOOM:
                if not self.__InteractorStyleRubberZoom:
                    self.__InteractorStyleRubberZoom = vtk.vtkInteractorStyleRubberBandZoom()
                self.__InteractorStyleSwitcher = self.__InteractorStyleRubberZoom
            else:
                pass
        
#            self.GetInteractor().SetInteractorStyle(self.__InteractorStyleSwitcher)

#        The redefine python commandobj is not vtkInteractorStyle, so we use SetInteractor
#        instead of use SetInteractorStyle
            self.GetInteractor().SetInteractorStyle(None)
            self.__InteractorStyleSwitcher.SetInteractor(self.GetInteractor())
            self.GetInteractor().SetRenderWindow(self.GetRenderWindow())
        if self.GetRenderer() and self.GetImageActor():
            self.GetRenderer().AddViewProp(self.GetImageActor())
        if self.GetImageActor() and self.GetWindowLevel():
            self.GetImageActor().SetInput(self.GetWindowLevel().GetOutput())
            
    def getSlicePlane(self):
        '''
        The SlicePlane instance (GetSlicePlane()) is the polygonal
         square corresponding to the slice plane,
         it is updated each time the slice changes,
         and is color-coded according to conventions
         @return: vtkPolyData
        '''
        return self.__SlicePlane


    def getCommand(self):
        return self.__Command


    def getCursor(self):
        return self.__Cursor


    def getCursorGenerator(self):
        return self.__CursorGenerator


    def getViewOrientation(self):
        '''
        Instead of setting the slice orientation to an axis (YZ - XZ - XY),
         you can force the view to be axial (foot-head), coronal (front-back),
         or sagittal (left-right). It will just use the OrientationMatrix
         (GetOrientationMatrix()) to check which slice orientation to pick.
         @return: int 
        '''
        return self.__ViewOrientation


    def getViewConvention(self):
        '''
         The ViewConvention instance explains where to place the camera around
         the patient. Default behaviour is Radiological convention, meaning
         we respectively look at the patient from his feet, his face and his left ear.
    
         For Neurological convention, we respectively look from the top of his head,
         the the back of his head, and his left ear.
         @return: int 
        '''
        return self.__ViewConvention


    def getInteractorStyleType(self):
        '''
         Get/Set the interactor style behaviour.
         @return: int
        '''
        return self.__InteractorStyleType


    def setSliceImplicitPlane(self, value):
        self.__SliceImplicitPlane = value


    def setSlicePlane(self, value):
        self.__SlicePlane = value


    def setCommand(self, value):
        self.__Command = value


    def setViewOrientation(self, orientation):
        '''
        Instead of setting the slice orientation to an axis (YZ - XZ - XY),
         you can force the view to be axial (foot-head), coronal (front-back),
         or sagittal (left-right). It will just use the OrientationMatrix
         (GetOrientationMatrix()) to check which slice orientation to pick.
         @param value: int
         @return: None 
        '''
        if ((orientation<self.VIEW_ORIENTATION_SAGITTAL) or 
            (orientation == self.__ViewOrientation)):
            return
        
        self.sliceorientation = 0
        dot = 0
        if self.getOrientationMatrix():
            for i in range(3):
                if dot < abs(self.getOrientationMatrix().GetElement(orientation, i)):
                    dot = abs(self.getOrientationMatrix().GetElement(orientation, i))
                    sliceorientation = i
        self.SetSliceOrientation(sliceorientation)
    
    def getInteractorStyleSwitcher(self):
        return self.__InteractorStyleSwitcher

    def setViewConvention(self, convention):
        '''
         The ViewConvention instance explains where to place the camera around
         the patient. Default behaviour is Radiological convention, meaning
         we respectively look at the patient from his feet, his face and his left ear.
    
         For Neurological convention, we respectively look from the top of his head,
         the the back of his head, and his left ear.
         @param convention: int
         @return: None 
        '''
        if ((convention<self.VIEW_CONVENTION_RADIOLOGICAL) or
            (convention==self.__ViewConvention)):
            return
        self.__ViewConvention = convention
        
        self.__ConventionMatrix.SetElement(2,0,1)
        self.__ConventionMatrix.SetElement(2,1,1)
        self.__ConventionMatrix.SetElement(1,2,-1)
        
        x_watcher = 1 
        y_watcher = 1
        z_watcher = 1
        if convention == self.VIEW_CONVENTION_RADIOLOGICAL:
            y_watcher = -1
            z_watcher = -1
#        else covention == self.VIEW_CONVENTION_NEUROLOGICAL:
#            x_watcher = 1 
#            y_watcher = 1
#            z_watcher = 1

        #=======================================================================
        # why not adding cardiologic conventions with oblique points of view ? 
        # actually we can't: oblique point of view implies resampling data: 
        # loss of data... and we don't want that, do we ?
        #=======================================================================
        self.__ConventionMatrix.SetElement(0,3,x_watcher)
        self.__ConventionMatrix.SetElement(1,3,y_watcher)
        self.__ConventionMatrix.SetElement(2,3,z_watcher)
        
        self.UpdateOrientation()
        
        
    def setInteractorStyleType(self, value):
        '''
         Get/Set the interactor style behaviour.
         @param int:
         @return: None 
        '''
        self.__InteractorStyleType = value
        self.InstallPipeline()
    
    def SetInteractorStyleTypeToNavigation(self):
        '''
        Get/Set the interactor style behaviour.
        '''
        self.setInteractorStyleType(self.INTERACTOR_STYLE_NAVIGATION)
    
    def SetInteractorStyleTypeToRubberZoom(self):
        '''
        Get/Set the interactor style behaviour.
        '''
        self.setInteractorStyleType(self.INTERACTOR_STYLE_RUBBER_ZOOM)

if __name__ == "__main__":
    import sys
    from jolly.ImageSeriesReader import *
    from vtk.util.misc import vtkGetDataRoot
    sys.argv.append("C:/head")
    
    if len(sys.argv)<2:
        sys.exit("Usage:\n\t%s <image file>\nExample: \n\t%s [vtkINRIA3D_DATA_DIR]/MRI.vtk\n" 
                 % (sys.argv[0], sys.argv[0]))
    
    #===========================================================================
    # Create 3 views, each of them will have a different orientation, .i.e.
    # axial, sagittal and coronal.
    #===========================================================================
    view1 = vtkPythonViewImage2D()
    iren1 = vtk.vtkRenderWindowInteractor()
    view1.SetupInteractor(iren1)
    view1.SetBackground(0.0, 0.0, 0.0)
    view1.SetSliceOrientationToXY()
    view1.SetInteractorStyleTypeToNavigation()
    
    view2 = vtkPythonViewImage2D()
    iren2 = vtk.vtkRenderWindowInteractor()
    view2.SetupInteractor(iren2)
    view2.SetBackground(0.0, 0.0, 0.0)
    view2.SetSliceOrientationToXZ()
    view2.SetInteractorStyleTypeToNavigation()
    
    view3 = vtkPythonViewImage2D()
    iren3 = vtk.vtkRenderWindowInteractor()
    view3.SetupInteractor(iren3)
    view3.SetBackground(0.0, 0.0, 0.0)
    view3.SetSliceOrientationToYZ()
    view3.SetInteractorStyleTypeToNavigation()
 
    
    reader = ImageSeriesReader(sys.argv[1])
#    v16 = vtk.vtkVolume16Reader()
#    v16.SetDataDimensions(64, 64)
#    v16.SetDataByteOrderToLittleEndian()
#    v16.SetFilePrefix(os.path.join(vtkGetDataRoot(),
#                                   "Data", "headsq", "quarter"))
#    v16.SetImageRange(1, 93)
#    v16.SetDataSpacing(3.2, 3.2, 1.5)
#    v16.Update()
#    
#    image = v16.GetOutput()
    
    image = vtk.vtkImageData()
   
    # must use deepcopy the convert imagedata
    image.DeepCopy(reader.ReadToVTK(".dcm"))    
    
    image.SetOrigin(0,0,0)
    
   
    
    
    view1.SetInput(image)
    view2.SetInput(image)
    view3.SetInput(image)
    
    view1.Update()
    view2.Update()
    view3.Update()
    
    view1.Reset()
    view2.Reset()
    view3.Reset()
    
    view1.Render()
    view2.Render()
    view3.Render()

    iren1.Start()
    
    