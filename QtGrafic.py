from ctypes import alignment
import sys
from time import sleep
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from GraficPlanet import GraficPlanet
from Planets import RandomSolar, CountForces, CountNewPosition, SolarSystemLook

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # layouts and graphics
        self.showFullScreen()
        self.HBox = QtWidgets.QHBoxLayout()
        self.setLayout(self.HBox)
        self.setStyleSheet("background-color: black;")

        self.scene = QtWidgets.QGraphicsScene(self)
        screen_resolution = app.desktop().screenGeometry()
        self.width, self.height = screen_resolution.width(), screen_resolution.height()
        self.scene.setSceneRect(0, 0, int(4 * self.width / 5), self.height)

        self.graphicview = QtWidgets.QGraphicsView(self.scene, self)
        self.graphicview.showFullScreen()
        self.graphicview.setGeometry(0, 0, int(4 * self.width / 5), self.height)
        self.graphicview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.HBox.addWidget(self.graphicview)
        self.VBox = QtWidgets.QVBoxLayout() 
        self.VBox.setAlignment(Qt.AlignTop)
        self.HBox.addLayout(self.VBox)

        self.timer = self.startTimer(20)

        self.start = QtWidgets.QPushButton(self)
        self.start.setText("Start")
        self.start.show()
        self.VBox.addWidget(self.start)
        self.start.setStyleSheet("background-color: white;")
        self.start.clicked.connect(self.simulationStart)

        self.reset = QtWidgets.QPushButton(self)
        self.reset.setText("Reset")
        self.reset.show()
        self.reset.setStyleSheet("background-color: white;")
        self.VBox.addWidget(self.reset)
        self.reset.clicked.connect(self.resetRun)

        self.mainControlBox = QtWidgets.QVBoxLayout(self)
        self.VBox.addLayout(self.mainControlBox)
        self.mainControlBox.setSpacing(20)
 
        self.WeightBox1 = QtWidgets.QVBoxLayout(self)
        self.mainControlBox.addLayout(self.WeightBox1)
        self.WeightBox1.setSpacing(5)

        self.label0 = QtWidgets.QLabel(self)
        self.label0.setText("TimeFrames")
        self.label0.setAlignment(QtCore.Qt.AlignCenter)
        self.label0.setFixedWidth(100)
        self.label0.setFixedHeight(20)
        self.label0.show()
        self.WeightBox1.addWidget(self.label0)
        self.label0.setStyleSheet("background-color: white; border: 2px solid gray; border-radius: 5px; }")

        self.slider0 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider0.setFixedWidth(100)
        self.slider0.show()
        self.slider0.setValue(3600)
        self.slider0.setMinimum(60)
        self.slider0.setMaximum(86400)
        self.slider0.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
        self.WeightBox1.addWidget(self.slider0)
        self.slider0.valueChanged.connect(self.timeFrameChance)
        self.timeFrame = self.slider0.value()

        self.WeightBox2 = QtWidgets.QVBoxLayout(self)
        self.mainControlBox.addLayout(self.WeightBox2)
        self.WeightBox2.setSpacing(5)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Zoom")
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setFixedWidth(100)
        self.label1.setFixedHeight(20)
        self.label1.show()
        self.WeightBox2.addWidget(self.label1)
        self.label1.setStyleSheet("background-color: white; border: 2px solid gray; border-radius: 5px; }")

        self.slider1 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider1.setFixedWidth(100)
        self.slider1.show()
        self.slider1.setValue(1000)
        self.slider1.setMinimum(250)
        self.slider1.setMaximum(5000)
        self.slider1.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
        self.WeightBox2.addWidget(self.slider1)
        self.slider1.valueChanged.connect(self.zoomChange)
        self.zoom = self.slider1.value()

        self.simulation_init_()
        self.simulation_paint_()

        self.pause = False
    
    def zoomChange(self):
        self.zoom = self.slider1.value()
        self.scene.clear()
        self.simulation_update_()
        self.simulation_paint_()

    def timeFrameChance(self):
        self.timeFrame = self.slider0.value()

    def resetRun(self):
        self.pause = False
        self.scene.clear()
        self.simulation_init_()
        self.simulation_paint_()
        self.start.setText("Start")
        self.slider0.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
        self.slider1.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")

    def simulationStart(self):
        if not self.pause:
            self.start.setText("Pause")
            self.pause = True
        else:
            self.start.setText("Unpause")
            self.pause = False

    def timerEvent(self, event: QtCore.QTimerEvent):
        if self.pause:
            self.slider0.setStyleSheet(
                "QSlider::handle:horizontal {background-color: gray; border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
            self.slider1.setStyleSheet(
                "QSlider::handle:horizontal {background-color: gray; border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
            CountForces(self.solar)
            CountNewPosition(self.solar, self.timeFrame, self.zoom)
            for i in range(len(self.System)):
                newPos = KartezSystem(self.Scene, self.solar[i].position_Graph[0], self.solar[i].position_Graph[1])
                oldPos = KartezSystem(self.Scene, self.solar[i].previosPosition[0], self.solar[i].previosPosition[1])
                #self.System[i].setPos(newPos[0] - oldPos[0],newPos[1] - oldPos[1])
                self.scene.addLine(newPos[0], newPos[1], oldPos[0], oldPos[1], QtGui.QPen(self.solar[i].color, 1))

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            if event.key() == QtCore.Qt.Key_Escape:
                sys.exit(0)

    def simulation_init_(self):
        self.solar = RandomSolar(self.zoom)
    
    def simulation_update_(self):
        SolarSystemLook(self.solar, self.zoom)
    
    def simulation_paint_(self):
        self.Scene = self.scene.sceneRect()
        self.System = []
        for i in self.solar:
            self.System.append(GraficPlanet(KartezSystem(self.Scene, i.position_Graph[0], i.position_Graph[1]), 10, color=i.color))

        for planet in self.System:
            self.scene.addItem(planet)
        #self.grDot0.setPos(self.start_dot0[0], self.start_dot0[1])
    
def KartezSystem(scene, x = 0, y = 0):
    centerx = scene.right()/2 + x
    centery  = scene.bottom()/2 -y
    return [centerx, centery]

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
