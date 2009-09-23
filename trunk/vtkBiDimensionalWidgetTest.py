#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light. when you put you mouse ,you will see the tips

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

def vtkBiDimensionalCallback(obj, event):
	print "End interaction event

v16 = vtk.vtkVolume16Reader()
v16.SetDataDimensions(64,64)
v16.SetDataByteOrderToLittleEndian()
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.SetFilePrefix("%s/Data/headsq/quarter" % (VTK_DATA_ROOT,))
v16.ReleaseDataFlagOn()
v16.SetDataMask(0x7fff)
v16.Update()
