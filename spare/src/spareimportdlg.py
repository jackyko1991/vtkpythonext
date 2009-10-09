# -*- coding:utf-8 -*-
"""
Created on 2009-10-3

@author: summit
"""
import os.path as osp
import vtk
from QVTKRenderWindowInteractor import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType

FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
                                  'spareimportdlg.ui'))

class SpareImportDialog(BaseClass, FormClass):
    """
        QT should add this to ui
        <customwidgets>
          <customwidget>
           <class>QVTKRenderWindowInteractor</class>
           <extends>QWidget</extends>
           <header>QVTKRenderWindowInteractor</header>
          </customwidget>
         </customwidgets>
    """
    def __init__(self, parent=None):
        BaseClass.__init__(self, parent)
        
        self.setupUi(self)
        self.previewWidget.Initialize()
        self.previewWidget.Start()
        self.ren = vtk.vtkRenderer()
        self.previewWidget.GetRenderWindow().AddRenderer(self.ren)

        self.actor = vtk.vtkActor()
        self.ren.AddActor(self.actor)
        
        self.dirname = QDir.currentPath()
        
        self.setWidgets()
        self.bind()
        
        
    def setWidgets(self):
        self.frame.hide()
        self.adjustSize()
    
    def enableWidgets(self):
        self.tabButton.setEnabled(True)
        self.fileformatcomboBox.setEnabled(True)
        self.importButton.setEnabled(True)
        self.sortButton.setEnabled(True)
        self.upButton.setEnabled(True)
        self.downButton.setEnabled(True)
        self.deleteButton.setEnabled(True)
        self.renameButton.setEnabled(True)
        self.backButton.setEnabled(True)
        self.tabWidget.setEnabled(True)
        
    def bind(self):
        self.connect(self.openButton, SIGNAL("clicked()"), self.onSelectDirectory) 
        self.connect(self.tabButton, SIGNAL("clicked()"), self.onToggleTabWidget)
        self.connect(self.sortButton, SIGNAL("clicked()"), self.onSortFileItem)
        self.connect(self.upButton, SIGNAL("clicked()"), self.onUpFileItem)
        self.connect(self.downButton, SIGNAL("clicked()"), self.onDownFileItem)
        self.connect(self.deleteButton, SIGNAL("clicked()"), self.onDeleteFileItem)
        self.connect(self.backButton, SIGNAL("clicked()"), self.resetFileListWidget)
        
    def onSelectDirectory(self):
        self.dirname = QFileDialog.getExistingDirectory(self, "Select a Directory", 
                                                   self.dirname )
        if self.dirname:
            self.enableWidgets()
            self.resetFileListWidget()
            
    def onToggleTabWidget(self):   
        if  self.frame.isHidden():
            self.frame.show()
            self.adjustSize()
        else:
            self.frame.hide()
            self.adjustSize()
    
    def updateFileListWidget(self):
        self.filelistWidget.clear()
        self.filelistWidget.addItems(self.files)
        self.filelistWidget.setCurrentRow(0)
        self.filelistWidget.update()
    
    def resetFileListWidget(self):
        dir = QDir(self.dirname)
        filters = QStringList()
        if self.fileformatcomboBox.currentText() == "BMP":
            filters << "*.bmp"
        elif self.fileformatcomboBox.currentText() == "JPG":
            filters << "*.JPG" << "*.JPEG" << "*.JPE" << "*.JFIF"
        elif self.fileformatcomboBox.currentText() == "TIFF":
            filters << "*.TIF" << "*.TIFF"
        else:
            filters << "*"
            
        self.files = dir.entryList(filters, QDir.Files)
        
        self.updateFileListWidget()
        
    def onUpFileItem(self):
        index = self.filelistWidget.currentRow()
        if index > 0:
            self.files.move(index, index-1)
            self.updateFileListWidget()
            self.filelistWidget.setCurrentRow(index-1)
    
    def onDownFileItem(self):
        index = self.filelistWidget.currentRow()
        if index+1 < self.files.count():
            self.files.move(index, index+1)
            self.updateFileListWidget()
            self.filelistWidget.setCurrentRow(index+1)
    
    def onSortFileItem(self):
        self.files.sort()
        self.updateFileListWidget()
    
    def onDeleteFileItem(self):
        index = self.filelistWidget.currentRow()
        if index >= 0 and index < self.files.count():
            self.files.removeAt(index)
            self.updateFileListWidget()
            self.filelistWidget.setCurrentRow(index-1)
    
if __name__ == "__main__":
   
    app = QApplication([])
    form = SpareImportDialog()
    form.show()
    app.exec_()