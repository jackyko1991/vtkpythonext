#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light.

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

def callback(obj, event):
	global glyph
	widgetValue = obj.GetDistance()
	glyph.SetScaleFactor( glyph.GetScaleFactor()*widgetValue)


sphereSource = vtk.vtkConeSource()
cone = vtk.vtkConeSource()
glyph = vtk.vtkGlyph3D()
glyph.SetInput(sphereSource.GetOutput())
glyph.SetSource(cone.GetOutput())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)
# The sphere and spikes are appended into a single polydata.
# This just makes things simpler to manage.
apd = vtk.vtkAppendPolyData()
apd.AddInput(glyph.GetOutput())
apd.AddInput(sphereSource.GetOutput())

maceMapper = vtk.vtkPolyDataMapper()
maceMapper.SetInput(apd.GetOutput())

maceActor = vtk.vtkLODActor()
maceActor.SetMapper(maceMapper)
maceActor.VisibilityOn()
maceActor.SetPosition(1, 1, 1)

ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# VTK widgets consist of two parts: the widget part that handles event
# processing; and the widget representation that defines how the widget
# appears in the scene (i.e., matters pertaining to geometry).
sliderRep  = vtk.vtkCompassRepresentation()
sliderRep.SetHeading(0.7)
sliderRep.SetDistance(1.3)
sliderRep.SetValue(1.0)
sliderRep.SetTilt(1.5)
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(0.2, 0.1)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(0.8, 0.1)


sliderWidget = vtk.vtkCompassWidget()
sliderWidget.SetInteractor(iren)
sliderWidget.SetRepresentation(sliderRep)

sliderWidget.AddObserver("InteractionEvent", callback)

ren1.AddActor(maceActor)
ren1.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(300, 300)

recorder = vtk.vtkInteractorEventRecorder()
recorder.SetInteractor(iren)
recorder.SetFileName("C:/record.log")

iren.Initialize()
renWin.Render()
iren.Start()

