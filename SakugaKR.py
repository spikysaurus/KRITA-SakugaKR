import krita
from PyQt5.QtGui import QImage
from pathlib import Path
import os
try:
    if int(krita.qVersion().split('.')[0]) == 5:
        raise
    from PyQt6.QtWidgets import *
except:
    from PyQt5.QtWidgets import *
from krita import *

class SakugaKR(DockWidget):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 100))    
        self.setWindowTitle("SakugaKR") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)
        self.line.setText("Path to parent folder with layer folder names inside it")

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        pybutton = QPushButton('Import', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,32)
        pybutton.move(80, 60)        

    def clickMethod(self):
        target_directory = self.line.text()
        app = Krita.instance()
        document = app.activeDocument() 

        if not os.path.isdir(target_directory):
            print(f"Directory not found at {target_directory}")
        else:
            for item in os.listdir(target_directory):
                arr = []
                arr.append(item)
                if document:
                    if document.nodeByName(item) == None:
                        newLayer = document.createNode(str(item), "paintLayer")
                        document.rootNode().addChildNode(newLayer, None)
                        newLayer.enableAnimation()
                    else: 
                        currentLayer = document.activeNode()
                        for folderLayer in arr:
                            if currentLayer == document.nodeByName(folderLayer):
                                item_path = os.path.join(target_directory, folderLayer)
                        
                                imageSequence = []
                                image_sequence_path = item_path
                                files = os.listdir(image_sequence_path)
                                for filename in files:
                                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                                        imageSequence.append(
                                            ( int(Path(filename).stem) ,os.path.join(image_sequence_path, filename)    ))
                                    imageSequence.sort()

                                    for i in imageSequence:
                                        document.setCurrentTime(int(Path(filename).stem))

                                        add_blank_frame_action = Krita.instance().action("add_blank_frame")
                                        add_blank_frame_action.trigger()

                                        image = QImage(str(os.path.join(image_sequence_path, filename)))
                                        pixelData = bytes(image.constBits().asarray(image.byteCount()))
                                        currentLayer.setPixelData(pixelData, 0, 0, image.width(), image.height())
                            else : pass
                else : pass

    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("SakugaKR", DockWidgetFactoryBase.DockPosition.DockRight, SakugaKR)) 
