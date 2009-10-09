# -*- coding:utf-8 -*-
"""
Created on 2009-9-16

@author: summit
"""
import sys
from jolly.ImageSeriesReader import *
from jolly.jolly_vtk.vtkViewImage2D import *

if __name__ == "__main__":
    sys.argv.append("../data/head")
    
    if len(sys.argv)<2:
        sys.exit("Usage:\n\t%s <image file>\nExample: \n\t%s [vtkINRIA3D_DATA_DIR]/MRI.vtk\n" 
                 % (sys.argv[0], sys.argv[0]))
    
    #===========================================================================
    # Create 3 views, each of them will have a different orientation, .i.e.
    # axial, sagittal and coronal.
    #===========================================================================
    view1 = vtkViewImage2D()
    view2 = vtkViewImage2D()
    view3 = vtkViewImage2D()
    
    iren1 = vtk.vtkRenderWindowInteractor()
    iren2 = vtk.vtkRenderWindowInteractor()
    iren3 = vtk.vtkRenderWindowInteractor()
    
    rwin1 = vtk.vtkRenderWindow()
    rwin2 = vtk.vtkRenderWindow()
    rwin3 = vtk.vtkRenderWindow()
    
    renderer1 = vtk.vtkRender()
    renderer2 = vtk.vtkRender()
    renderer3 = vtk.vtkRender()
    
    iren1.SetRenderWindow(rwin1)
    iren2.SetRenderWindow(rwin2)
    iren3.SetRenderWindow(rwin3)
    
    rwin1.AddRenderer(renderer1)
    rwin2.AddRenderer(renderer2)
    rwin3.AddRenderer(renderer3)
    
    view1.SetRenderWindow(rwin1)
    view2.SetRenderWindow(rwin2)
    view3.SetRenderWindow(rwin3)
    
    view1.SetRenderer(renderer1)
    view2.SetRenderer(renderer2)
    view3.SetRenderer(renderer3)
    
    # One can also associate to each button (left, middle, right and even wheel)
    # a specific interaction like this:
    
    view1.SetLeftButtonInteractionStyle(vtkViewImage2D.ZOOM_INTERACTION)
    view1.SetMiddleButtonInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view1.SetWheelInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view1.SetRightButtonInteractionStyle(vtkViewImage2D.WINDOW_LEVEL_INTERACTION)
    
    view2.SetLeftButtonInteractionStyle(vtkViewImage2D.ZOOM_INTERACTION)
    view2.SetMiddleButtonInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view2.SetWheelInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view2.SetRightButtonInteractionStyle(vtkViewImage2D.WINDOW_LEVEL_INTERACTION)
    
    view3.SetLeftButtonInteractionStyle(vtkViewImage2D.ZOOM_INTERACTION)
    view3.SetMiddleButtonInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view3.SetWheelInteractionStyle(vtkViewImage2D.SELECT_INTERACTION)
    view3.SetRightButtonInteractionStyle(vtkViewImage2D.WINDOW_LEVEL_INTERACTION)
    
    view1.SetLinkZoom(True)  
    view2.SetLinkZoom(True)
    view3.SetLinkZoom(True)
    
    view1.SetOrientation(vtkViewImage2D.AXIAL_ID)
    view2.SetOrientation(vtkViewImage2D.CORONAL_ID)
    view3.SetOrientation(vtkViewImage2D.SAGITTAL_ID)
    
    view1.SetBackgroundColor(0.0, 0.0, 0.0)
    view2.SetBackgroundColor(0.0, 0.0, 0.0)
    view3.SetBackgroundColor(0.0, 0.0, 0.0)
    
    view1.SetAboutData("Powered by summit & jolly")
    view2.SetAboutData("Powered by summit & jolly")
    view3.SetAboutData("Powered by summit & jolly")
    
    # Link the views together for synchronization.
    view1.AddChild(view2)
    view2.AddChild(view3)
    view3.AddChild(view1)
    
    reader = ImageReader(sys.argv[1])
    image = reader.ReadToVTK()
    print image
    view1.SetImage(image)
    view2.SetImage(image)
    view3.SetImage(image)
    
    #  Reset the window/level and the current position.
    view1.SyncResetCurrentPoint()
    view1.SyncResetWindowLevel()
    
    rwin1.Render()
    rwin2.Render()
    rwin3.Render()
    
    iren1.Start()
    
    view1.Detach()
    view2.Detach()
    view3.Detach()