import sys
from math import *
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Load some data.
v16 = vtk.vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix("%s/Data/headsq/quarter" % (VTK_DATA_ROOT,))
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.ReleaseDataFlagOn()
v16.SetDataMask(0x7fff)
v16.Update()

range = v16.GetOutput().GetScalarRange()

shifter = vtk.vtkImageShiftScale()
shifter.SetShift(-1.0*range[0])
shifter.SetScale(255.0/(range[1]-range[0]))
shifter.SetOutputScalarTypeToUnsignedChar()
shifter.SetInputConnection(v16.GetOutputPort())
shifter.ReleaseDataFlagOff()
shifter.Update()

imageActor = vtk.vtkImageActor()
imageActor.SetInput(shifter.GetOutput())
imageActor.VisibilityOn()
# imageActor.SetDisplayExtent(0, 63, 0, 63, 46, 46)
imageActor.SetDisplayExtent(0, 63, 0, 63, 46, 46)
imageActor.InterpolateOn()

# Create the RenderWindow, Renderer and both Actors
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

handleRep = vtk.vtkConstrainedPointHandleRepresentation()
handleRep.ActiveRepresentationOn()

handleWidget = vtk.vtkHandleWidget()
handleWidget.SetInteractor(iren)
handleWidget.SetRepresentation(handleRep)

ren1.AddActor(imageActor)

# Add the actors to the renderer, set the background and size
ren1.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(300, 300)

handleRep.SetPosition(imageActor.GetCenter())
handleRep.SetProjectionNormalToYAxis()
handleRep.SetProjectionPosition(imageActor.GetCenter()[1])

bounds = imageActor.GetBounds()

p1 = vtk.vtkPlane()
p1.SetOrigin( bounds[0], bounds[2], bounds[4] )
p1.SetNormal( 1.0, 0.0, 0.0 )

p2 = vtk.vtkPlane()
p2.SetOrigin( bounds[0], bounds[2], bounds[4] )
p2.SetNormal( 0.0, 0.0, 1.0)

p3 = vtk.vtkPlane()
p3.SetOrigin( bounds[1], bounds[3], bounds[5] )
p3.SetNormal( -1.0, 0.0, 0.0 )

p4 = vtk.vtkPlane()
p4.SetOrigin( bounds[1], bounds[3], bounds[5] )
p4.SetNormal( 0.0, 0.0, -1.0 )

handleRep.AddBoundingPlane(p1)
handleRep.AddBoundingPlane(p2)
handleRep.AddBoundingPlane(p3)
handleRep.AddBoundingPlane(p4)

# render the image
ren1.GetActiveCamera().SetPosition(0, 0, 0)
ren1.GetActiveCamera().SetFocalPoint(0, 1, 0)
ren1.GetActiveCamera().SetViewUp(0, 0, 1)
ren1.ResetCamera()
iren.Initialize()

renWin.Render()

iren.Start()