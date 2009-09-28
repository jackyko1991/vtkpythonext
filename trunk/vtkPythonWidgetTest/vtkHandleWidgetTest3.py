# This example tests the vtkHandleWidget with a 2D representation
# First include the required header files for the VTK classes we are using.
import sys
from math import *
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# This does the actual work: updates the probe.
# Callback for the interaction
def vtkHandle2CallBack(obj, event):
	pos = [0]*3
	obj.GetRepresentation().GetDisplayPosition(pos)
	print id(vtkHandle2CallBack.Actor)
	vtkHandle2CallBack.Actor.SetPosition(pos[0], pos[1])

def vtkHandle2CallBack2(obj, event):
	pos = [0]*3
	obj.GetRepresentation().GetDisplayPosition(pos)
	print id(vtkHandle2CallBack2.Actor)
	vtkHandle2CallBack2.Actor.SetPosition(pos[0], pos[1])

eventLog = "# StreamVersion 1" \
"MouseMoveEvent 245 235 0 0 0 0 i" \
"MouseMoveEvent 244 234 0 0 0 0 i" \
"MouseMoveEvent 244 234 0 0 0 0 i" \
"KeyReleaseEvent 244 234 0 0 105 1 i" \
"MouseMoveEvent 243 233 0 0 0 0 i" \
"MouseMoveEvent 242 232 0 0 0 0 i" \
"MouseMoveEvent 241 231 0 0 0 0 i" \
"MouseMoveEvent 240 231 0 0 0 0 i" \
"MouseMoveEvent 240 230 0 0 0 0 i" \
"MouseMoveEvent 239 229 0 0 0 0 i" \
"MouseMoveEvent 238 228 0 0 0 0 i" \
"MouseMoveEvent 237 227 0 0 0 0 i" \
"MouseMoveEvent 236 227 0 0 0 0 i" \
"MouseMoveEvent 235 226 0 0 0 0 i" \
"MouseMoveEvent 235 226 0 0 0 0 i" \
"MouseMoveEvent 234 225 0 0 0 0 i" \
"MouseMoveEvent 233 224 0 0 0 0 i" \
"MouseMoveEvent 232 223 0 0 0 0 i" \
"MouseMoveEvent 231 222 0 0 0 0 i" \
"MouseMoveEvent 230 221 0 0 0 0 i" \
"MouseMoveEvent 229 220 0 0 0 0 i" \
"MouseMoveEvent 228 220 0 0 0 0 i" \
"MouseMoveEvent 228 220 0 0 0 0 i" \
"LeftButtonPressEvent 228 220 0 0 0 0 i" \
"StartInteractionEvent 228 220 0 0 0 0 i" \
"TimerEvent 228 220 0 0 0 0 i" \
"RenderEvent 228 220 0 0 0 0 i" \
"MouseMoveEvent 228 220 0 0 0 0 i" \
"TimerEvent 228 220 0 0 0 0 i" \
"RenderEvent 228 220 0 0 0 0 i" \
"TimerEvent 228 220 0 0 0 0 i" \
"RenderEvent 228 220 0 0 0 0 i" \
"MouseMoveEvent 228 219 0 0 0 0 i" \
"TimerEvent 228 219 0 0 0 0 i" \
"RenderEvent 228 219 0 0 0 0 i" \
"MouseMoveEvent 228 217 0 0 0 0 i" \
"TimerEvent 228 217 0 0 0 0 i" \
"RenderEvent 228 217 0 0 0 0 i" \
"MouseMoveEvent 226 215 0 0 0 0 i" \
"TimerEvent 226 215 0 0 0 0 i" \
"RenderEvent 226 215 0 0 0 0 i" \
"MouseMoveEvent 224 209 0 0 0 0 i" \
"MouseMoveEvent 222 204 0 0 0 0 i" \
"MouseMoveEvent 215 201 0 0 0 0 i" \
"LeftButtonReleaseEvent 215 201 0 0 0 0 i" \
"EndInteractionEvent 215 201 0 0 0 0 i" \
"RenderEvent 215 201 0 0 0 0 i" \
"MouseMoveEvent 215 201 0 0 0 0 i" \
"MouseMoveEvent 215 201 0 0 0 0 i" \
"MouseMoveEvent 210 190 0 0 0 0 i" \
"MouseMoveEvent 204 187 0 0 0 0 i" \
"MouseMoveEvent 193 184 0 0 0 0 i" \
"MouseMoveEvent 184 180 0 0 0 0 i" \
"MouseMoveEvent 175 174 0 0 0 0 i" \
"MouseMoveEvent 168 173 0 0 0 0 i" \
"MouseMoveEvent 165 173 0 0 0 0 i" \
"MouseMoveEvent 163 173 0 0 0 0 i" \
"MouseMoveEvent 160 173 0 0 0 0 i" \
"MouseMoveEvent 159 173 0 0 0 0 i" \
"MouseMoveEvent 158 173 0 0 0 0 i" \
"MouseMoveEvent 158 174 0 0 0 0 i" \
"MouseMoveEvent 157 174 0 0 0 0 i" \
"MouseMoveEvent 157 174 0 0 0 0 i" \
"MouseMoveEvent 157 175 0 0 0 0 i" \
"MouseMoveEvent 158 176 0 0 0 0 i" \
"MouseMoveEvent 158 176 0 0 0 0 i" \
"MouseMoveEvent 160 178 0 0 0 0 i" \
"MouseMoveEvent 163 181 0 0 0 0 i" \
"MouseMoveEvent 168 188 0 0 0 0 i" \
"MouseMoveEvent 178 197 0 0 0 0 i" \
"MouseMoveEvent 195 209 0 0 0 0 i" \
"MouseMoveEvent 207 228 0 0 0 0 i" \
"MouseMoveEvent 220 247 0 0 0 0 i" \
"MouseMoveEvent 235 264 0 0 0 0 i" \
"MouseMoveEvent 246 283 0 0 0 0 i" \
"MouseMoveEvent 256 292 0 0 0 0 i" \
"LeaveEvent 256 292 0 0 0 0 i" \
"ExitEvent 256 292 0 0 0 0 i" 

# Create two widgets
diskSource = vtk.vtkDiskSource()
diskSource.SetInnerRadius(0.0)
diskSource.SetOuterRadius(2)

diskMapper = vtk.vtkPolyDataMapper2D()
diskMapper.SetInput(diskSource.GetOutput())

diskActor = vtk.vtkActor2D()
diskActor.SetMapper(diskMapper)
diskActor.SetPosition(165, 180)

diskSource2 = vtk.vtkDiskSource()
diskSource2.SetInnerRadius(0.0)
diskSource2.SetOuterRadius(2)

diskMapper2 = vtk.vtkPolyDataMapper2D()
diskMapper2.SetInput(diskSource.GetOutput())

diskActor2 = vtk.vtkActor2D()
diskActor2.SetMapper(diskMapper2)
diskActor2.SetPosition(50, 50)

# Create the RenderWindow, Renderer and both Actors
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# The cursor shape can be defined externally. Here we use a default
cursor2D = vtk.vtkCursor2D()
cursor2D.AllOff()
cursor2D.AxesOn()
cursor2D.OutlineOn()
cursor2D.SetRadius(4)

handleRep = vtk.vtkPointHandleRepresentation2D()
handleRep.SetDisplayPosition(diskActor.GetPosition()+(0,))
handleRep.ActiveRepresentationOn()
handleRep.SetCursorShape(cursor2D.GetOutput())

handleWidget = vtk.vtkHandleWidget()
handleWidget.SetInteractor(iren)
handleWidget.SetRepresentation(handleRep)
callback = vtkHandle2CallBack
callback.Actor = diskActor
handleWidget.AddObserver("InteractionEvent", callback)

handleRep2 = vtk.vtkPointHandleRepresentation2D()
handleRep2.SetDisplayPosition(diskActor2.GetPosition()+(0,))
#handleRep2.ActiveRepresentationOn()
handleRep2.SetCursorShape(cursor2D.GetOutput())

handleWidget2 = vtk.vtkHandleWidget()
handleWidget2.SetInteractor(iren)
handleWidget2.SetRepresentation(handleRep2)
callback2 = vtkHandle2CallBack2
callback2.Actor = diskActor2
handleWidget2.AddObserver("InteractionEvent", callback2)

ren1.AddActor(diskActor)
ren1.AddActor(diskActor2)

# Add the actors to the renderer, set the background and size
ren1.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(300, 300)

# record events
recorder = vtk.vtkInteractorEventRecorder()
recorder.SetInteractor(iren)
#recorder.SetFileName("C:/record.log")
#recorder.Record()
recorder.ReadFromInputStringOn()
recorder.SetInputString(eventLog)

# render the image
iren.Initialize()
renWin.Render()
# recorder.Play()
handleWidget.On()
handleWidget2.On()

# Remove the observers so we can go interactive. Without this the "-I"
# testing option fails.
#recorder.Off()
recorder.Play()
iren.Start()
