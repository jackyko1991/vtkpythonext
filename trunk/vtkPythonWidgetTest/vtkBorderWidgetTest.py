#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light.

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()


ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Create a test pipeline
ss = vtk.vtkSphereSource()
mapper = vtk.vtkPolyDataMapper()
mapper.SetInput(ss.GetOutput())
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create the widget and its representation
rep = vtk.vtkBorderRepresentation()
rep.ProportionalResizeOn()
rep.SetShowBorderToOn()
#rep.SetShowBorderToActive()

widget = vtk.vtkBorderWidget()
widget.SetInteractor(iren)
widget.SetRepresentation(rep)
widget.SelectableOff()

# Add the actors to the renderer, set the background and size
ren1.AddActor(actor)
ren1.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(300, 300)

# record events
recorder = vtk.vtkInteractorEventRecorder()
recorder.SetInteractor(iren)
recorder.SetFileName("C:/record.log")

# render the image

iren.Initialize()
renWin.Render()
widget.On()
iren.Start()
