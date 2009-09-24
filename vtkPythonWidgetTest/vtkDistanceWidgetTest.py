#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light.

import vtk
from math import *
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()


# This callback is responsible for adjusting the point position.
# It looks in the region around the point and finds the maximum or
# minimum value.

def vtkDistanceCallback(obj, event, pid):
	global ren1, renWin, rep
	
	if event == "InteractionEvent" or event == "EndInteractionEvent":
		pos1 = [0]*3
		pos2 = [0]*3
		# Modify the measure axis
		rep.GetPoint1WorldPosition(pos1)
		rep.GetPoint2WorldPosition(pos2)
		dist = sqrt(vtk.vtkMath.Distance2BetweenPoints(pos1, pos2))

		rep.GetAxis().SetRange(0.0, dist)
		rep.GetAxis().SetTitle("%-#6.3g" % dist)
	else:
		# From the point id, get the display coordinates
		pos1 = [0]*3
		pos2 = [0]*3
		pos  = None
		rep.GetPoint1WorldPosition(pos1)
		rep.GetPoint2WorldPosition(pos2)
		if pid == 0:
			pos = pos1
		else:
			pos = pos2
		# Okay, render without the widget, and get the color buffer
		enabled = obj.GetEnabled()
		if enabled:
			obj.SetEnabled(0)	# does a Render() as a side effect
		# Pretend we are doing something serious....just randomly bump the
		# location of the point.
		p = [0]*3
		p[0] = pos[0] + int(vtk.vtkMath.Random(-5.5, 5.5))
		p[1] = pos[1] + int(vtk.vtkMath.Random(-5.5, 5.5))
		p[2] = 0.0

		# Set the new position
		if pid == 0:
			rep.SetPoint1DisplayPosition(p)
		else:
			rep.SetPoint2DisplayPosition(p)
		
		# Side effect of a render here
		if enabled:
			obj.SetEnabled(1)

vtkDistanceCallback.CallDataType = 'string0'

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
handle.GetProperty().SetColor(1,0,0)
rep = vtk.vtkDistanceRepresentation2D()
rep.SetHandleRepresentation(handle)

rep.GetAxis().SetNumberOfMinorTicks(4)
rep.GetAxis().SetTickLength(9)
rep.GetAxis().SetTitlePosition(0.2)

widget = vtk.vtkDistanceWidget()
widget.SetInteractor(iren)
widget.CreateDefaultRepresentation()
widget.SetRepresentation(rep)

widget.AddObserver("InteractionEvent", vtkDistanceCallback)
widget.AddObserver("EndInteractionEvent", vtkDistanceCallback)
widget.AddObserver("PlacePointEvent", vtkDistanceCallback)
widget.AddObserver("StartInteractionEvent", vtkDistanceCallback)

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
