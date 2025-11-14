import krita
from PyQt5.QtGui import QImage, QPainter, QColor, QPen, QFont
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

        central = QWidget(self)
        self.setWidget(central)

        self.Vbox_0 = QVBoxLayout(central)

        # Create the tab widget
        self.tabWidget = QTabWidget(central)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)

        # Add tabs
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("DockWidget", "Camera", None)
        )

        self.tab_1 = QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tabWidget.addTab(self.tab_1, "")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_1),
            QCoreApplication.translate("DockWidget", "Import", None)
        )

        self.Vbox_0.addWidget(self.tabWidget)
        self.setLayout(self.Vbox_0)

#        self.setMinimumSize(QSize(258, 100))    
        self.setWindowTitle("SakugaKR") 

        Vbox = QVBoxLayout(self.tab)
        
        Hbox_0 = QHBoxLayout()
        labelLabel = QLabel()
        labelLabel.setText('Label : ')
        self.lineStamp = QLineEdit()
        self.lineStamp.setText("A")
        Hbox_0.addWidget(labelLabel)
        Hbox_0.addWidget(self.lineStamp)
        
        Hbox_1 = QHBoxLayout()
        labelColor = QLabel()
        labelColor.setText('Color : ')
        self.lineColor = QLineEdit()
        self.lineColor.setText("red")
        Hbox_1.addWidget(labelColor)
        Hbox_1.addWidget(self.lineColor)

        Hbox = QHBoxLayout()
        labelSize = QLabel()
        labelSize.setText('Size : ')
        self.lineWidth = QLineEdit()
        self.lineWidth.setText("1496")
        self.lineHeight = QLineEdit()
        self.lineHeight.setText("842")
        Hbox.addWidget(labelSize)
        Hbox.addWidget(self.lineWidth)
        Hbox.addWidget(self.lineHeight)
        
        Hbox_3 = QHBoxLayout()
        labelScale = QLabel()
        labelScale.setText('Scale : ')
        self.lineScale = QLineEdit()
        self.lineScale.setText("100")
        labelOffsetY = QLabel()
        labelOffsetY.setText('Offset Y : ')
        self.lineOffsetY = QLineEdit()
        self.lineOffsetY.setText("0.079")
        Hbox_3.addWidget(labelScale)
        Hbox_3.addWidget(self.lineScale)
        Hbox_3.addWidget(labelOffsetY)
        Hbox_3.addWidget(self.lineOffsetY)
        
        Hbox_4 = QHBoxLayout()
        BtnStamp = QPushButton('Stamp Camera')
        BtnStamp.clicked.connect(self.draw_red_outline_rectangle_with_text)
        BtnReset = QPushButton('Reset')
        BtnReset.clicked.connect(self.reset_camera_stamp_values)
        Hbox_4.addWidget(BtnReset, 1)
        Hbox_4.addWidget(BtnStamp, 2)
        
        Vbox.addLayout(Hbox_0)
        Vbox.addLayout(Hbox_1)
        Vbox.addLayout(Hbox)
        Vbox.addLayout(Hbox_3)
        Vbox.addLayout(Hbox_4)
        
        self.setLayout(Vbox)

        Vbox_1 = QVBoxLayout(self.tab_1)
        Hbox_5 = QHBoxLayout()
        nameLabel = QLabel(self.tab_1)
        nameLabel.setText('Path : ')
        self.line = QLineEdit(self.tab_1)
        self.line.setText("")
        Hbox_5.addWidget(nameLabel)
        Hbox_5.addWidget(self.line)
        
        Hbox_6 = QHBoxLayout()
        pybutton = QPushButton('Create Layers', self.tab_1)
        pybutton.clicked.connect(self.clickMethod)  
        pybutton2 = QPushButton('Import Images', self.tab_1)
        pybutton2.clicked.connect(self.clickMethod2)
        Hbox_6.addWidget(pybutton)
        Hbox_6.addWidget(pybutton2)
        
        Vbox_1.addLayout(Hbox_5)
        Vbox_1.addLayout(Hbox_6)

        self.setLayout(Vbox_1)

    def reset_camera_stamp_values(self):
        self.lineWidth.setText("1496")
        self.lineHeight.setText("842")
        self.lineScale.setText("100")
        self.lineOffsetY.setText("0.079")

    def draw_red_outline_rectangle_with_text(self):
        app = Krita.instance()
        doc = app.activeDocument()
        if not doc:
            doc = app.createDocument(1920, 1080, "RedOutlineTextDoc", "RGBA", "U8", "", 120.0)
            app.activeWindow().addView(doc)

        # Create a new paint layer
        new_layer = doc.createNode("Camera " + self.lineStamp.text(), "paintlayer")
        active_node = doc.activeNode()
        parent_node = active_node.parentNode()
        parent_node.addChildNode(new_layer, None)

        # --- Scale factor (percentage) ---
        # Example: user enters "120" for 120% scaling
        scale_percent = float(self.lineScale.text()) if hasattr(self, "lineScale") else 100.0
        scale_factor = scale_percent / 100.0

        # Base rectangle size
        base_width = int(self.lineWidth.text())
        base_height = int(self.lineHeight.text())

        # Apply scaling
        width = int(base_width * scale_factor)
        height = int(base_height * scale_factor)

        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(QColor(0, 0, 0, 0))

        painter = QPainter(image)
        warna = self.lineColor.text()
        pen = QPen(QColor(warna))
        pen.setWidth(int(7 * scale_factor))  # scale outline thickness too
        painter.setPen(pen)
        painter.setBrush(QColor(0, 0, 0, 0))

        painter.drawRect(0, 0, width, height)

        # Scale font size
        base_font_size = 48
        font = QFont("Arial", int(base_font_size * scale_factor))
        painter.setFont(font)
        painter.setPen(QColor(warna))

        # Scale text position
        text_x = int(10 * scale_factor)
        text_y = int(60 * scale_factor)
        painter.drawText(text_x, text_y, self.lineStamp.text())

        painter.end()

        new_layer.setPixelData(image.bits().asstring(image.byteCount()), 0, 0, width, height)

        # Center + offset logic unchanged
        canvas_width = doc.width()
        canvas_height = doc.height()

        bounds = new_layer.bounds()
        layer_width = bounds.width()
        layer_height = bounds.height()

        target_x = (canvas_width - layer_width) / 2.0
        target_y = (canvas_height - layer_height) / 2.0

        offset_y = canvas_height * float(self.lineOffsetY.text())
        target_y += offset_y

        delta_x = target_x - bounds.x()
        delta_y = target_y - bounds.y()
        new_layer.move(int(delta_x), int(delta_y))

        doc.refreshProjection()

        
        


    def clickMethod2(self):
        target_directory = self.line.text()
        app = Krita.instance()
        document = app.activeDocument() 
        currentLayer = document.activeNode()

        if not os.path.isdir(target_directory):
            print(f"Directory not found at {target_directory}")
        else:
            for item in os.listdir(target_directory):
                arr = []
                arr.append(item)

                if currentLayer.name() in arr: 
                    item_path = os.path.join(target_directory, currentLayer.name())
                    imageSequence = []
                    image_sequence_path = item_path
                    files = os.listdir(image_sequence_path)
                    for filename in files:
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                            imageSequence.append(( int(Path(filename).stem) ,os.path.join(image_sequence_path, filename)  ))
                        imageSequence.sort()

                        for i in imageSequence:
                            document.setCurrentTime(int(Path(filename).stem))

                            add_blank_frame_action = Krita.instance().action("add_blank_frame")
                            add_blank_frame_action.trigger()

                            image = QImage(str(os.path.join(image_sequence_path, filename)))
                            pixelData = bytes(image.constBits().asarray(image.byteCount()))
                            currentLayer.setPixelData(pixelData, 0, 0, image.width(), image.height())
 
    def clickMethod(self):
        target_directory = self.line.text()
        app = Krita.instance()
        document = app.activeDocument() 
        currentLayer = document.activeNode()

        if not os.path.isdir(target_directory):
            print(f"Directory not found at {target_directory}")
        else:
            for item in os.listdir(target_directory):
                arr = []
                arr.append(item)
                
                if currentLayer.name() not in arr:
                    newLayer = document.createNode(str(item), "paintLayer")
                    document.rootNode().addChildNode(newLayer, None)
                    newLayer.enableAnimation()
                    


    def canvasChanged(self, canvas):
        pass

Krita.instance().addDockWidgetFactory(DockWidgetFactory("SakugaKR", DockWidgetFactoryBase.DockPosition.DockRight, SakugaKR)) 
