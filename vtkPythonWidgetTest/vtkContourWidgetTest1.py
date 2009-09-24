#!/usr/bin/env python

# This example demonstrates how to use the vtkSphereWidget to control
# the position of a light.
import sys
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

if len(sys.argv) < 2:
	print "Demonstrates editing capabilities of a contour widget on terrain \n" \
		"data. Additional arguments : \n" \
		"\tThe projection mode may optionally be specified. [0-Simple,1-NonOccluded\n" \
		",2-Hug]. (defaults to Hug)\n" \
		"\tA height offset may be specified. Defaults to 0.0\n" \
		"\tIf a polydata is specified, an initial contour is constucted from\n" \
		"the points in the polydata. The polydata is expected to be a polyline\n" \
		"(one cell and two or more points on that cell)."
	print "\n\nUsage: " << argv[0] << "\n" \
		"  [-ProjectionMode (0,1 or 2)]\n" \
		"  [-HeightOffset heightOffset]\n" \
		"  [-InitialPath SomeVTKXmlfileContainingPath.vtk]" 

demReader = vtk.vtkDEMReader()
demReader.SetFileName("%s/Data/SainteHelens.dem" % (VTK_DATA_ROOT,))

# Extract geometry
surface = vtk.vtkImageDataGeometryFilter()
surface.SetInput(demReader.GetOutput())

warp = vtk.vtkWarpScalar()
warp.SetInput(surface.GetOutput())
warp.SetScaleFactor(1)
warp.UseNormalOn()
warp.SetNormal(0, 0, 1)
warp.Update()

# Define a LUT mapping for the height field 
lo, hi = demReader.GetOutput().GetScalarRange()

lut = vtk.vtkLookupTable()
lut.SetHueRange(0.6, 0)
lut.SetSaturationRange(1.0, 0)
lut.SetValueRange(0.5, 1.0)

normals = vtk.vtkPolyDataNormals()
normals.SetInput(warp.GetPolyDataOutput())
normals.SetFeatureAngle(60)
normals.SplittingOff()

demMapper = vtk.vtkPolyDataMapper()
demMapper.SetInput(normals.GetOutput())
normals.Update()
demMapper.SetScalarRange(lo, hi)
demMapper.SetLookupTable(lut)

demActor = vtk.vtkActor()
demActor.SetMapper(demMapper)

# Create the RenderWindow, Renderer and the DEM + path actors.
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
renWin.SetSize(600, 600)
ren1.AddActor(demActor)
ren1.GetActiveCamera().SetViewUp(0, 0, 1)
ren1.GetActiveCamera().SetPosition(-99900, -21354, 131801)
ren1.GetActiveCamera().SetFocalPoint(41461, 41461, 2815)
ren1.ResetCamera()
ren1.GetActiveCamera().Dolly(1.2)
ren1.ResetCameraClippingRange()

# Here comes the contour widget stuff.....
contourWidget = vtk.vtkContourWidget()
rep = contourWidget.GetRepresentation()
rep.GetLinesProperty().SetColor(1.0, 0.0, 0.0)
contourWidget.SetInteractor(iren)

# Set the point placer to the one used for terrains...
pointPlacer = vtk.vtkTerrainDataPointPlacer()
pointPlacer.AddProp(demActor)	# the actor(s) containing the terrain.
rep.SetPointPlacer(pointPlacer)

# Set a terrain interpolator. Interpolates points as they are placed,
# so that they lie on the terrain.
interpolator = vtk.vtkTerrainContourLineInterpolator()
rep.SetLineInterpolator(interpolator)
interpolator.SetImageData(demReader.GetOutput())

# Set the default projection mode to hug the terrain, unless user 
# overrides it.
interpolator.GetProjector().SetProjectionModeToHug()
for i in range(0, len(sys.argv)):
	if sys.argv[i] == "-ProjectionMode":
		interpolator.GetProjector().SetProjectionMode(int(sys.argv[i+1]))
	if sys.argv[i] == "HeightOffset":
		interpolator.GetProjector().SetHeightOffset(int(sys.argv[i+1]))
	if sys.argv[i] == "InitialPath":
		# If we had an input poly as an initial path, build a contour widget from
		# that path.
		terrainPathReader  = vtk.vtkPolyDataReader()
		terrainPathReader.SetFileName(sys.argv[i+1])
		terrainPathReader.Update();
		contourWidget.Initialize( terrainPathReader.GetOutput(), 0 );
		
contourWidget.EnabledOn()

# record events
recorder = vtk.vtkInteractorEventRecorder()
recorder.SetInteractor(iren)
recorder.SetFileName("C:/record.log")

# render the image

iren.Initialize()
renWin.Render()
iren.Start()
