import sys
from math import *
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

if len(sys.argv)<2:
	msg = "Demonstrates interaction of a handle, represented be a user \n" \
		"specified polygonal shape, so that it is constrained \n" \
		"to lie on a polygonal surface.\n\n" \
		"Usage args: [-DistanceOffset height_offset]."
	sys.exit(msg)



# Read height field
demReader = vtk.vtkDEMReader()
demReader.SetFileName("%s/Data/SainteHelens.dem" % (VTK_DATA_ROOT,))

resample = vtk.vtkImageResample()
resample.SetInput(demReader.GetOutput())
resample.SetDimensionality(2)
resample.SetAxisMagnificationFactor(0, 1.0)
resample.SetAxisMagnificationFactor(1, 1.0)

# Extract geometry
surface = vtk.vtkImageDataGeometryFilter()
surface.SetInput(resample.GetOutput())

# The Dijkistra interpolator will not accept cells that aren't triangles
triangleFilter = vtk.vtkTriangleFilter()
triangleFilter.SetInput( surface.GetOutput() )
triangleFilter.Update()

warp = vtk.vtkWarpScalar()
warp.SetInput(triangleFilter.GetOutput())
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
distanceOffsetSpecified = False
distanceOffset = None
for i in xrange(len(sys.argv)-1):
	if sys.argv[i] == "-DistanceOffset":
		distanceOffset = float(sys.argv[i+1])
		distanceOffsetSpecified = True

if distanceOffsetSpecified:
	normals.SetInput(warp.GetPolyDataOutput())
	normals.SetFeatureAngle(60)
	normals.SplittingOff()

	# vtkvtkPolygonalSurfacePointPlacer needs cell normals
	normals.ComputeCellNormalsOn()
	normals.Update()

pd = (distanceOffsetSpecified and normals.GetOutput()) or warp.GetPolyDataOutput()

demMapper = vtk.vtkPolyDataMapper()
demMapper.SetInput(pd)
demMapper.SetScalarRange(lo, hi)
demMapper.SetLookupTable(lut)


demActor = vtk.vtkActor()
demActor.SetMapper(demMapper)

# Create the RenderWindow, Renderer and the DEM + path actors
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


# Add the actors to the renderer, set the backgournd and size
ren1.AddActor(demActor)

ren1.GetActiveCamera().SetViewUp(0, 0, 1)
ren1.GetActiveCamera().SetPosition(-99900, -21354, 131801)
ren1.GetActiveCamera().SetFocalPoint(41461, 41461, 2815)
ren1.ResetCamera()
ren1.ResetCameraClippingRange()

# Here comes the surface constrained handle widget stuff....

widget = vtk.vtkHandleWidget()
widget.SetInteractor(iren)
rep = vtk.vtkPointHandleRepresentation3D()
widget.SetRepresentation(rep)
pointPlacer = vtk.vtkPolygonalSurfacePointPlacer()
pointPlacer.AddProp(demActor)
pointPlacer.GetPolys().AddItem(pd)
rep.SetPointPlacer(pointPlacer)




# Let the surface constrained point-placer be the sole constraint dictating 
# the placement of handles. Lets not over-constrain it allowing axis
# constrained interactions.
widget.EnableAxisConstraintOff()

# Set some defaults on the handle widget
d = [562532, 5.11396e+06, 2618.62]
rep.SetWorldPosition(d)
rep.GetProperty().SetColor(1.0, 0.0, 0.0)
rep.GetProperty().SetLineWidth(1.0)
rep.GetSelectedProperty().SetColor(0.2, 0.0, 1.0)



if distanceOffsetSpecified:
	pointPlacer.SetDistanceOffset( distanceOffset )

renWin.Render()
iren.Initialize()
widget.EnabledOn()

iren.Start()


iren.Start()

	