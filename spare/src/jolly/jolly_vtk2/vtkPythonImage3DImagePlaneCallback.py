'''
Created on 2009-10-15

@author: summit
'''
import vtk
import math
class vtkPythonImage3DImagePlaneCallback(vtk.vtkObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__Reslice = vtk.vtkImageReslice()
        self.__ResliceAxes = vtk.vtkMatrix4x4()
        
    def Execute(self, caller, event, callData):
        '''
        @param caller: vtkObject
        @param event: str
        @callData: void* 
        '''
#        get the Plane widget
        widget = vtk.vtkPlaneWidget.SafeDownCast(caller)
        if not widget:
            return
        
        imageData = vtk.vtkImageData.SafeDownCast(widget.GetInput())
        if not imageData:
            self.__Reslice.SetInput(None)
            return
        
        self.__Reslice.SetInput(imageData)
        
        # Calculate appropriate pixel spacing for the reslicing
        imageData.UpdateInformation()
        spacing = imageData.GetSpacing()
        
        imOrigin = imageData.GetOrigin()
        
        extent = imageData.GetWholeExtent()
        bounds = [imOrigin[0] + spacing[0]*extent[0], # xmin
                  imOrigin[0] + spacing[0]*extent[1], # xmax
                  imOrigin[1] + spacing[1]*extent[2], # ymin
                  imOrigin[1] + spacing[1]*extent[3], # ymax
                  imOrigin[2] + spacing[2]*extent[4], # zmin
                  imOrigin[2] + spacing[2]*extent[5]  # zmax
                  ]
        
        for i in range(0, 5, 2): # reverse bounds if necessary
            if bounds[i] > bounds[i+1]:
                t = bounds[i+1]
                bounds[i+1] = bounds[i]
                bounds[i] = t
        
        abs_normal=[0.0]*3
        widget.GetNormal(abs_normal)
        planeCenter=[0.0]*3
        widget.GetCenter(planeCenter)
        nmax=0.0
        k=0
        for i in range(3):
            abs_normal[i] = math.fabs(abs_normal[i])
            if abs_normal[i]>nmax:
                nmax = abs_normal[i]
                k=i
        
#         Force the plane to lie within the true image bounds along its normal
        if planeCenter[k] > bounds[2*k+1]:
            planeCenter[k] = bounds[2*k+1]
        elif planeCenter[k] < bounds[2*k]:
            planeCenter[k] = bounds[2*k]
        
        widget.SetCenter(planeCenter)
        
#        get the plane
        point1 = widget.GetPoint1()
        point2 = widget.GetPoint2()
        origin = widget.GetOrign()
        normal = widget.GetNormal()
        
        axis1 = [0.0]*3
        axis2 = [0.0]*3
        for i in range(3):
            axis1[i] = point1[i]-origin[i]
            axis2[i] = point2[i]-origin[i]
        
        planeSizeX = vtk.vtkMath.Normalize(axis1)
        planeSizeY = vtk.vtkMath.Normalize(axis2)
        
        self.__ResliceAxes.Identity()
        for i in range(3):
            self.__ResliceAxes.SetElement(0, i, axis1[i])
            self.__ResliceAxes.SetElement(1, i, axis2[i])
            self.__ResliceAxes.SetElement(2, i, normal[i])
            
        origin[3] = 1.0
        originXYZW = [0.0]*4
        self.__ResliceAxes.MultiplyPoint(origin, originXYZW)
        
        self.__ResliceAxes.Transpose()
        neworiginXYZW = [0.0]*4
        point = originXYZW
        self.__ResliceAxes.MultiplyPoint(point, neworiginXYZW)
        
        self.__ResliceAxes.SetElement(0, 3, neworiginXYZW[0])
        self.__ResliceAxes.SetElement(1, 3, neworiginXYZW[1])
        self.__ResliceAxes.SetElement(2, 3, neworiginXYZW[2])
        
        self.__Reslice.SetResliceAxes(self.__ResliceAxes)
        self.__Reslice.SetInterpolationModeToLinear()
        self.__Reslice.SetOutputSpacing(1.0, 1.0, 1.0)
        self.__Reslice.SetOutputOrigin(0.0, 0.0, 0.0)
        self.__Reslice.SetOutputExtent(0, int(planeSizeX-1), 0,
                                       int(planeSizeY-1),0, 0)
        self.__Reslice.Update()

    def GetOutput(self):
        '''
        @return: vtkImageData
        '''
        return self.__Reslice.GetOutput()
    
    def Reset(self):
        '''
        @return: None
        '''
        self.__Reslice.SetInput(None)
    
    def getMatrix(self):
        return self.__ResliceAxes
   
    def getReslice(self):
        return self.__Reslice


    def getResliceAxes(self):
        return self.__ResliceAxes


    def setReslice(self, value):
        self.__Reslice = value


    def setResliceAxes(self, value):
        self.__ResliceAxes = value

if __name__=="__main__":
    pass

