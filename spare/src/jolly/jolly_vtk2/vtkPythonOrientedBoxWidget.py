'''
Created on 2009-10-15

@author: summit
'''
import vtk
class vtkPythonOrientedBoxWidget(vtk.vtkBoxWidget):
    '''
    vtkOrientedBoxWidget
    orthogonal hexahedron 3D widget with pre-defined orientation
    Description

       This 3D widget defines a region of interest. By default it behaves exactly as the
       vtkBoxWidget class does. But if the user set the Orientation matrix with
       SetOrientationMatrix() then all the actors of the widgets (handles, hexahedron, etc)
       will be oriented according to the argument.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__OrientationMatrix = vtk.vtkMatrix4x4()
        self.__OrientationMatrix.Identity()
        self.__InvertedOrientationMatrix = vtk.vtkMatrix4x4()
        self.__InvertedOrientationMatrix.Identity()
    
    def OnMouseMove(self):
        '''
        '''
        
    def getOrientationMatrix(self):
        return self.__OrientationMatrix


    def getInvertedOrientationMatrix(self):
        return self.__InvertedOrientationMatrix


    def setOrientationMatrix(self, matrix):
        if matrix == self.__OrientationMatrix:
            return
        if self.__OrientationMatrix:
            self.__OrientationMatrix.UnRegister(self)
            self.__OrientationMatrix=None
    
        self.__OrientationMatrix=matrix
        if self.__OrientationMatrix:
            self.__OrientationMatrix.Register(self)
#        move all the actors according to the user-matrix
#        to be continue

    def setInvertedOrientationMatrix(self, value):
        self.__InvertedOrientationMatrix = value

