from multimethod import multimethod
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
import math

class Geometrica:
    def __init__(self,painter:QtGui.QPainter, x, y):
        self.x = x
        self.y = y
        self.painter = painter
        print(f"Se ha creado una figura geometrica en la posicion ({self.x},{self.y}) ")
        
    def moverse(self):
        self.x += 10
        self.y += 10
        print(f"Se ha movido la figura geometrica a la posicion ({self.x},{self.y}) ")
        
class Circulo(Geometrica):
    def __init__(self,painter:QtGui.QPainter, x, y, radio):
        super().__init__(painter,x,y)    
        self.radio = radio
        
    @multimethod    
    def dibujar(self):
        self.painter.setBrush(Qt.GlobalColor.transparent)
        self.painter.drawEllipse(self.x-self.radio,self.y-self.radio,self.radio*2,self.radio*2)

    @multimethod    
    def dibujar(self, color:Qt.GlobalColor):
        self.painter.setBrush(color)
        self.painter.drawEllipse(self.x-self.radio,self.y-self.radio,self.radio*2,self.radio*2)

class Cuadrado(Geometrica):    
    def __init__(self,painter:QtGui.QPainter, x, y, lado):
        super().__init__(painter,x,y)    
        self.lado = lado
        
    @multimethod    
    def dibujar(self, color:Qt.GlobalColor):
        self.painter.setBrush(color)
        self.painter.drawRect(self.x,self.y,self.lado,self.lado)

    @multimethod    
    def dibujar(self):
        self.painter.setBrush(Qt.GlobalColor.transparent)
        self.painter.drawRect(self.x,self.y,self.lado,self.lado)

class Triangulo(Geometrica):
    def __init__(self, painter:QtGui.QPainter, x, y, lado):
        super().__init__(painter, x, y)
        self.lado = lado

    @multimethod
    def dibujar(self):
        self.painter.setBrush(Qt.GlobalColor.transparent)
        path = QtGui.QPainterPath()
        path.moveTo(self.x, self.y)
        path.lineTo(self.x + self.lado, self.y)
        path.lineTo(self.x + self.lado/2, self.y - self.lado * 0.866)
        path.closeSubpath()
        self.painter.drawPath(path)

    @multimethod
    def dibujar(self, color:Qt.GlobalColor):
        self.painter.setBrush(color)
        path = QtGui.QPainterPath()
        path.moveTo(self.x, self.y)
        path.lineTo(self.x + self.lado, self.y)
        path.lineTo(self.x + self.lado/2, self.y - self.lado * 0.866)
        path.closeSubpath()
        self.painter.drawPath(path)

class Pentagono(Geometrica):
    def __init__(self, painter:QtGui.QPainter, x, y, radio):
        super().__init__(painter, x, y)
        self.radio = radio

    @multimethod
    def dibujar(self):
        self.painter.setBrush(Qt.GlobalColor.transparent)
        path = QtGui.QPainterPath()
        angle = 72
        for i in range(5):
            theta = (angle * i -90) * math.pi / 180
            x = self.x + self.radio * math.cos(theta)
            y = self.y + self.radio * math.sin(theta)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()
        self.painter.drawPath(path)

    @multimethod
    def dibujar(self, color:Qt.GlobalColor):
        self.painter.setBrush(color)
        path = QtGui.QPainterPath()
        angle = 72
        for i in range(5):
            theta = (angle * i -90) * math.pi / 180
            x = self.x + self.radio * math.cos(theta)
            y = self.y + self.radio * math.sin(theta)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()
        self.painter.drawPath(path)