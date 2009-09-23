#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light.

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

def vtkAngleCallback(obj, event):
	global rep
	if event == "PlacePointEvent":
		print "point placed"
	elif event == "InteractionEvent":
		point1 = [1, 2, 3]
		center = [1, 2, 3]
		point2 = [1, 2, 3]
		rep.GetPoint1WorldPosition(point1)
		rep.GetCenterWorldPosition(center)
		rep.GetPoint2WorldPosition(point2)
		print "Angle betwwen ", point1, " ", center, " and ", point2, rep.GetAngle()


# Create the RenderWindow, Renderer and both Actors
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
handle = vtk.vtkPointHandleRepresentation2D()
handle.GetProperty().SetColor(1, 0, 0)
rep = vtk.vtkAngleRepresentation2D()
rep.SetHandleRepresentation(handle)

widget = vtk.vtkAngleWidget()
widget.SetInteractor(iren)
widget.CreateDefaultRepresentation()
widget.SetRepresentation(rep)

widget.AddObserver("PlacePointEvent", vtkAngleCallback)
widget.AddObserver("InteractionEvent", vtkAngleCallback)

# Add the actor to the renderer, set the background and size
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