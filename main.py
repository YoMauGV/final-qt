import sys
import json
import library
import urllib.request
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt, QTimer
from weather import Clima

color_translation = {
    "negro": "black",
    "rojo": "red",
    "rojo oscuro": "darkRed",
    "verde": "green",
    "verde oscuro": "darkGreen",
    "azul": "blue",
    "azul oscuro": "darkBlue",
    "cian": "cyan",
    "cian oscuro": "darkCyan",
    "magenta": "magenta",
    "magenta oscuro": "darkMagenta",
    "amarillo": "yellow",
    "amarillo oscuro": "darkYellow",
    "gris": "gray",
    "gris oscuro": "darkGray",
    "gris claro": "lightGray"
}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App de Clima")

        # Variable para numero de ciudad
        ciudad = 1
        
        # Crear un layout vertical
        layout = QtWidgets.QVBoxLayout()
        
        # Crear un cuadro de texto para ingresar la ciudad
        self.ciudad_input = QtWidgets.QLineEdit(self)
        self.ciudad_input.setPlaceholderText("Ingrese el nombre de la ciudad")
        layout.addWidget(self.ciudad_input)
        
        # Crear un botón para obtener los datos del clima
        self.boton = QtWidgets.QPushButton("Obtener Clima", self)
        self.boton.clicked.connect(self.leer_json)
        layout.addWidget(self.boton)
        
        # Crear un QLabel para mostrar el canvas
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(600, 600)
        canvas.fill(Qt.GlobalColor.white)
        self.label.setPixmap(canvas)
        layout.addWidget(self.label)
        
        # Crear un widget central y establecer el layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def leer_json(self):
        ciudad = self.ciudad_input.text()
        if ciudad:
            c = Clima()
            data = c.extrae_relevantes(ciudad)
            print(data)
            figura = {
                "nombre": "circulo",
                "x": 50,
                "y": 50,
                "medida": 0,
                "color": "azul"
            }
            self.dibuja_figura(figura, data['ciudad'], data['temperatura'])
        else:
            print("Por favor, ingrese el nombre de una ciudad.")

    def dibuja_figura(self,json_fig, ciudad, temperatura):
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(QtGui.QFont('Arial', 12))
        painter.drawText(50, 50, f"Ciudad: {ciudad}")
        painter.drawText(50, 70, f"Temperatura: {temperatura}°C")
        
        if json_fig["nombre"] == "circulo":
            figura=library.Circulo(painter,json_fig["x"],json_fig["y"],json_fig["medida"])
            if(json_fig["color"]):
                color = color_translation[json_fig["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        elif json_fig["nombre"] == 'cuadrado':
            figura=library.Cuadrado(painter,json_fig["x"],json_fig["y"],json_fig["medida"])
            if(json_fig["color"]):
                color = color_translation[json_fig["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        elif json_fig["nombre"] == 'rectangulo':
            figura=library.Rectangulo(painter,json_fig["x"],json_fig["y"],json_fig["medida"])
            if(json_fig["color"]):
                color = color_translation[json_fig["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        elif json_fig["nombre"] == 'triangulo':
            figura=library.Triangulo(painter,json_fig["x"],json_fig["y"],json_fig["medida"])
            if(json_fig["color"]):
                color = color_translation[json_fig["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        elif json_fig["nombre"] == 'pentagono':
            figura=library.Pentagono(painter,json_fig["x"],json_fig["y"],json_fig["medida"])
            if(json_fig["color"]):
                color = color_translation[json_fig["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        else:
            print("No se reconoce la figura {}".format(json_fig))
        painter.end()      
        self.label.setPixmap(canvas)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()