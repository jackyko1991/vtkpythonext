#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light. when you put you mouse ,you will see the tips

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

def vtkBiDimensionalCallback(obj, event):
	print "End interaction event"

v16 = vtk.vtkVolume16Reader()
v16.SetDataDimensions(64,64)
v16.SetDataByteOrderToLittleEndian()
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.SetFilePrefix("%s/Data/headsq/quarter" % (VTK_DATA_ROOT,))
v16.ReleaseDataFlagOn()
v16.SetDataMask(0x7fff)
v16.Update()

range = v16.GetOutput().GetScalarRange()

shifter = vtk.vtkImageShiftScale()
shifter = vtk.vtkImageShiftScale()
shifter.SetShift(-1.0*range[0])
shifter.SetScale(255.0/(range[1]-range[0]))
shifter.SetOutputScalarTypeToUnsignedChar()
shifter.SetInputConnection(v16.GetOutputPort())
shifter.ReleaseDataFlagOff()
shifter.Update()

imageActor = vtk.vtkImageActor()
imageActor.SetInput(shifter.GetOutput())
imageActor.VisibilityOn()
imageActor.SetDisplayExtent(0, 63, 0, 63, 46, 46)
imageActor.InterpolateOn()

bounds = imageActor.GetBounds()

# Create the RenderWindow, Renderer and both Actors
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleImage()
iren.SetInteractorStyle(style)

# VTK widgets consist of two parts: the widget part that handles event processing;
# and the widget representation that defines how the widget appears in the scene
# (i.e., matters pertaining to geometry).
rep = vtk.vtkBiDimensionalRepresentation2D()
widget = vtk.vtkBiDimensionalWidget()

widget.SetInteractor(iren)
widget.SetRepresentation(rep)

widget.AddObserver("EndInteractionEvent", vtkBiDimensionalCallback)

# Add the actors to the renderer, set the background and size
ren1.AddActor(imageActor)
ren1.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(300, 300)

# record events
recorder = vtk.vtkInteractorEventRecorder()
recorder.SetInteractor(iren)
recorder.SetFileName("C:/record.log")

# render the image

iren.Initialize()
renWin.Render()
iren.Start()

