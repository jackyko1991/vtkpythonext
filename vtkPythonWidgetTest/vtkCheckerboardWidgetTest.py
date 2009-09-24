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
 
# Create a checkerboard pipeline
image1 = vtk.vtkImageCanvasSource2D()
image1.SetNumberOfScalarComponents(3)
image1.SetScalarTypeToUnsignedChar()
image1.SetExtent(0,511,0,511,0,0)
image1.SetDrawColor(255,255,0)
image1.FillBox(0,511,0,511)

pad1 = vtk.vtkImageWrapPad()
pad1.SetInput(image1.GetOutput())
pad1.SetOutputWholeExtent(0,511,0,511,0,0)

image2 = vtk.vtkImageCanvasSource2D()
image2.SetNumberOfScalarComponents(3)
image2.SetScalarTypeToUnsignedChar()
image2.SetExtent(0,511,0,511,0,0)
image2.SetDrawColor(0,255,255)
image2.FillBox(0,511,0,511)

pad2 = vtk.vtkImageWrapPad()
pad2.SetInput(image1.GetOutput())
pad2.SetOutputWholeExtent(0,511,0,511,0,0)

checkers = vtk.vtkImageCheckerboard()
checkers.SetInput(0, pad1.GetOutput())
checkers.SetInput(1, pad2.GetOutput())
checkers.SetNumberOfDivisions(10, 6, 1)

checkerboardActor = vtk.vtkImageActor()
checkerboardActor.SetInput(checkers.GetOutput())

# VTK widgets consist of two parts: the widget part that handles event processing;
# and the widget representation that defines how the widget appears in the scene
# (i.e., matters pertaining to geometry).
rep = vtk.vtkCheckerboardRepresentation()
rep.SetImageActor(checkerboardActor)
rep.SetCheckerboard(checkers)

checkerboardWidget = vtk.vtkCheckerboardWidget()
checkerboardWidget.SetInteractor(iren)
checkerboardWidget.SetRepresentation(rep)

# Add the actors to the renderer, set the background and size
ren1.AddActor(checkerboardActor)
ren1.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(300, 300)

# record events
recorder = vtk.vtkInteractorEventRecorder()
recorder.SetInteractor(iren)
recorder.SetFileName("C:/record.log")

# render the image

iren.Initialize()
renWin.Render()
checkerboardWidget.On()
iren.Start()