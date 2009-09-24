#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light.
import sys
from math import *
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Create the RenderWindow, Renderer and both Actors
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren1.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(600, 600)

contourRep = vtk.vtkOrientedGlyphContourRepresentation()
contourWidget = vtk.vtkContourWidget()
contourWidget.SetInteractor(iren)
contourWidget.SetRepresentation(contourRep)
contourWidget.On()

for i in range(0, len(sys.argv)):
	if sys.argv[i] == "-Shift":
		contourWidget.GetEventTranslator().RemoveTranslation( "LeftButtonPressEvent" );
	elif sys.argv[i] == "-Scale":
		contourWidget.GetEventTranslator().RemoveTranslation( "LeftButtonPressEvent" );
		contourWidget.GetEventTranslator().RemoveTranslation( "LeftButtonPressEvent", vtk.vtkWidgetEvent.Scale );

pd = vtk.vtkPolyData()
points = vtk.vtkPoints()
#lines = vtk.vtkCellArray()
lineIndices = vtk.vtkIdList()
for i in range(0, 20):
	angle = 2.0 * vtk.vtkMath.Pi()*i/20.0
	points.InsertPoint(i, 0.1*cos(angle), 0.1*sin(angle), 0.0)
	#lineIndices.InsertNextId(i)
#lineIndices.InsertNextId(0)
#lines.InsertNextCell(lineIndices)
pd.SetLines(vtk.vtkCellArray())
pd.SetPoints(points)
#pd.SetLines(lines)



contourWidget.Initialize(pd, 1)
contourWidget.Render()
ren1.ResetCamera()
renWin.Render()

iren.Initialize()
iren.Start()