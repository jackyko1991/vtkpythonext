#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light. when you put you mouse ,you will see the tips

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

def vtkBalloonCallback(obj, event):
	if obj.GetCurrentProp() == None:
		print "Prop selected"

# Create the RenderWindow, Renderer and both Actors
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

style = vtk.vtkInteractorStyleTrackballCamera()
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
# iren.SetInteractorStyle(style)

# Create an image for the balloon widget
image1 = vtk.vtkTIFFReader()
image1.SetFileName("%s/Data/beach.tif" % (VTK_DATA_ROOT,))
image1.SetOrientationType(4)

# Create a test pipeline
ss = vtk.vtkSphereSource()
mapper = vtk.vtkPolyDataMapper()
mapper.SetInput(ss.GetOutput())
sph = vtk.vtkActor()
sph.SetMapper(mapper)

cs = vtk.vtkCylinderSource()
csMapper = vtk.vtkPolyDataMapper()
csMapper.SetInput(cs.GetOutput())
cy1 = vtk.vtkActor()
cy1.SetMapper(mapper)
cy1.AddPosition(5, 0, 0)

coneSource = vtk.vtkConeSource()
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInput(coneSource.GetOutput())
cone = vtk.vtkActor()
cone.SetMapper(coneMapper)
cone.AddPosition(0, 5, 0)

# Create the widget
rep = vtk.vtkBalloonRepresentation()
rep.SetBalloonLayoutToImageRight()

widget = vtk.vtkBalloonWidget()
widget.SetInteractor(iren)
widget.SetRepresentation(rep)
widget.AddBalloon(sph, "This is a sphere", None)
widget.AddBalloon(cy1, "This is a\ncylinder", image1.GetOutput())
widget.AddBalloon(cone, "This is a \ncone, \na really big cone, \nyou wouldn't believe how big", image1.GetOutput())

widget.AddObserver("WidgetActivateEvent", vtkBalloonCallback)

# Add the actors to the renderer, set the background and size

ren1.AddActor(sph)
ren1.AddActor(cy1)
ren1.AddActor(cone)
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

recorder.Off()

iren.Start()
