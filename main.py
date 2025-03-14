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

descripcion = {
    "clear sky": "Despejado",
    "few clouds": "Algunas nubes",
    "scattered clouds": "Nubes dispersas",
    "broken clouds": "Nublado",
    "shower rain": "Lluvia ligera",
    "rain": "Lluvia",
    "thunderstorm": "Tormenta",
    "snow": "Nieve",
    "mist": "Neblina"
}

figura_clima = {
    "01": {
        "figura": "circulo",
        "x": 75,
        "y": 50,
        "medida": 40,
        "color": "amarillo oscuro"
        },
    "02": {
        "figura": "triangulo",
        "x": 40,
        "y": 85,
        "medida": 80,
        "color": "verde oscuro"
    },
    "03": {
        "figura": "cuadrado",
        "x": 40,
        "y": 10,
        "medida": 80,
        "color": "cian"
    },
    "04": {
        "figura": "pentagono",
        "x": 70,
        "y": 55,
        "medida": 40,
        "color": "rojo oscuro"
    },
    "09": {
        "figura": "triangulo",
        "x": 40,
        "y": 85,
        "medida": 80,
        "color": "azul oscuro"
    },
    "10": {
        "figura": "cuadrado",
        "x": 40,
        "y": 10,
        "medida": 80,
        "color": "verde"
    },
    "11": {
        "figura": "pentagono",
        "x": 70,
        "y": 55,
        "medida": 40,
        "color": "magenta"
    },
    "13": {
        "figura": "circulo",
        "x": 75,
        "y": 50,
        "medida": 40,
        "color": "verde oscuro"
    },
    "50": {
        "figura": "rectangulo",
        "x": 20,
        "y": 20,
        "medida": 60,
        "color": "gris"
        },
}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App de Clima")

        # Variable para numero de ciudad
        self.clima = 0
        
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
            if(data['ciudad'] == False): 
                print("Ciudad no encontrada")
                canvas = self.label.pixmap()
                painter = QtGui.QPainter(canvas)
                desplazamiento = 100 * self.clima
                # Ilumina el fondo
                figura=library.Rectangulo(painter,0,0 + desplazamiento,599,100)
                figura.dibujar(Qt.GlobalColor.white)
                # Dibuja el texto
                painter.setPen(Qt.GlobalColor.black)
                painter.setFont(QtGui.QFont('Arial', 16))
                painter.drawText(100, 60 + desplazamiento, f"Ciudad no encontrada")
                painter.end()      
                self.label.setPixmap(canvas)
            else:   
                print(data)
                print(data['icono'][:2])
                fig = figura_clima[data['icono'][:2]]
                print(fig["figura"])
                if data["icono"][-1] == 'n':
                    fondo = True
                else:
                    fondo = False
                datos = {
                    "ciudad": data['ciudad'],
                    "temperatura": data['temperatura'],
                    "descripcion": data['description'],
                    "posicion": self.clima,
                    "noche": fondo,
                    "figura": fig["figura"],
                    "x": fig["x"],
                    "y": fig["y"],
                    "medida": fig["medida"],
                    "color": fig["color"]
                }
                self.dibuja_figura(datos)
                if self.clima == 5:
                    self.clima = 0
                else:
                    self.clima += 1
        else:
            print("Por favor, ingrese el nombre de una ciudad.")
            canvas = self.label.pixmap()
            painter = QtGui.QPainter(canvas)
            desplazamiento = 100 * self.clima
            # Ilumina el fondo
            figura=library.Rectangulo(painter,0,0 + desplazamiento,599,100)
            figura.dibujar(Qt.GlobalColor.white)
            # Dibuja el texto
            painter.setPen(Qt.GlobalColor.black)
            painter.setFont(QtGui.QFont('Arial', 16))
            painter.drawText(100, 60 + desplazamiento, f"Por favor, ingrese el nombre de una ciudad.")
            painter.end()      
            self.label.setPixmap(canvas)

    def dibuja_figura(self, datos):
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        desplazamiento = 100 * datos["posicion"]
        # Ilumina el fondo
        if datos["noche"]:
            figura=library.Rectangulo(painter,0,0 + desplazamiento,599,100)
            figura.dibujar(Qt.GlobalColor.black)
            painter.setPen(Qt.GlobalColor.white)
        else:
            figura=library.Rectangulo(painter,0,0 + desplazamiento,599,100)
            figura.dibujar(Qt.GlobalColor.yellow)
            painter.setPen(Qt.GlobalColor.black)
        # Dibuja el texto
        painter.setFont(QtGui.QFont('Arial', 42))
        painter.drawText(160, 70 + desplazamiento, f"{int(round(datos["temperatura"]))} °C")
        painter.setFont(QtGui.QFont('Arial', 16))
        painter.drawText(330, 40 + desplazamiento, f"Ciudad: {datos["ciudad"]}")
        painter.drawText(330, 70 + desplazamiento, f"{descripcion.get(datos['descripcion'], 'Descripción no disponible')}")
        
        if datos["figura"] == "circulo":
            figura=library.Circulo(painter, datos["x"], datos["y"] + desplazamiento, datos["medida"])
            if(datos["color"]):
                color = color_translation[datos["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        elif datos["figura"] == 'cuadrado':
            figura=library.Cuadrado(painter, datos["x"], datos["y"] + desplazamiento, datos["medida"])
            if(datos["color"]):
                color = color_translation[datos["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        elif datos["figura"] == 'rectangulo':
            figura=library.Rectangulo(painter, datos["x"], datos["y"] + desplazamiento, datos["medida"] * 2, datos["medida"])
            if(datos["color"]):
                color = color_translation[datos["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        elif datos["figura"] == 'triangulo':
            figura=library.Triangulo(painter, datos["x"], datos["y"] + desplazamiento, datos["medida"])
            if(datos["color"]):
                color = color_translation[datos["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        elif datos["figura"] == 'pentagono':
            figura=library.Pentagono(painter, datos["x"], datos["y"] + desplazamiento, datos["medida"])
            if(datos["color"]):
                color = color_translation[datos["color"]]
                figura.dibujar(Qt.GlobalColor[color])
            else:
                figura.dibujar()
        else:
            print("No se reconoce la figura {}".format(datos["figura"]))
        painter.end()      
        self.label.setPixmap(canvas)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()