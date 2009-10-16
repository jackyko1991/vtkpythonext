'''
Created on 2009-10-14

@author: summit
'''
import vtk
class vtkPythonImage3DCroppingBoxCallback(vtk.vtkObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__VolumeMapper = None
    
    def SetVolumeMapper(self, mapper):
        self.__VolumeMapper = mapper
    
    def GetVolumeMapper(self):
        return self.__VolumeMapper
    
    def Execute(self, caller, event, callData):
        if not self.__VolumeMapper:
            return
        
        # get the box widget
        widget = caller
        
        if not widget:
            return
        
        # Get the poly data defined by the vtkBowWidget
        myBox = vtk.vtkPolyData()
        widget.GetPolyData(myBox)
        
        bounds = self.__VolumeMapper.GetBounds()
        
        # myBox contains 15 points and points 8 to 13
        # define the bounding box
        pt = myBox.GetPoint(8)
        xmin = pt[0]
        pt = myBox.GetPoint(9)
        xmax = pt[0]
        pt = myBox.GetPoint(10)
        ymin = pt[1]
        pt = myBox.GetPoint(11)
        ymax = pt[1]
        pt = myBox.GetPoint(12)
        zmin = pt[2]
        pt = myBox.GetPoint(13)
        zmax = pt[2]
        
        if xmin<bounds[0]: xmin=bounds[0]
        if ymin<bounds[2]: ymin=bounds[2]
        if zmin<bounds[4]: zmin=bounds[4]
        if xmax<bounds[1]: xmax=bounds[1]
        if ymax<bounds[3]: ymax=bounds[3]
        if zmax<bounds[5]: zmax=bounds[5]
        
        self.__VolumeMapper.SetCroppingRegionPlanes(xmin, xmax, ymin, ymax, zmin, zmax)
#        del myBox
        
        