from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GraficPlanet(QGraphicsItem):
    def __init__(self,pos=[0,0], size=30, color=Qt.green,):
        super().__init__()
        self.size = size

        self.color = color

        self.top_x = pos[0] - self.size/2
        self.top_y = pos[1] - self.size/2

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return QRectF(
            self.top_x,
            self.top_y,
            self.size,
            self.size
        ).normalized()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)

        path_content.addEllipse(self.top_x, self.top_y, self.size,self.size)

        if self.isSelected():
            painter.setPen(Qt.yellow)

        else:
            painter.setPen(Qt.NoPen)

        painter.setBrush(self.color)

        painter.drawPath(path_content.simplified())