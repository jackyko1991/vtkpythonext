#!/usr/bin/env python

# This example tests the vtkSeedWidget

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

def vtkSeedCallback(obj, event):
	global rep

	print "Point placed, total of:%d"%(rep.GetNumberOfSeeds())
	for i in range(rep.GetNumberOfSeeds()):
		pos=[0.0]*3
		rep.GetSeedWorldPosition(i, pos)
		print "Point %d World Position:"%(i), pos
		rep.GetSeedDisplayPosition(i, pos)
		print "Point %d Display Position:"%(i), pos

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
rep = vtk.vtkSeedRepresentation()
rep.SetHandleRepresentation(handle)

widget=vtk.vtkSeedWidget()
widget.SetInteractor(iren)
widget.SetRepresentation(rep)

widget.AddObserver("PlacePointEvent", vtkSeedCallback)

# Add the actors to the renderer, set the background and size

ren1.AddActor(actor)
ren1.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(300, 300)

iren.Initialize()
renWin.Render()
widget.On()

iren.Start()