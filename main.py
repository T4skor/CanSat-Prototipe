import sys
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QIcon

class MapaVentana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulación CanSat")
        self.setGeometry(100, 100, 1000, 600)

        # Establecer el ícono de la ventana
        self.setWindowIcon(QIcon("C:/Users/fanta/Desktop/Programas/CanSat/LOGO.ico"))

        # Establecer pantalla completa
        self.showFullScreen()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Crear el QWebEngineView para mostrar el mapa
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        # Variables para almacenar datos
        self.altitud = []
        self.temperatura = []
        self.tiempo = []

        # Crear figura y ejes usando matplotlib
        self.fig, self.axs = plt.subplots(1, 2, figsize=(10, 5))
        self.fig.patch.set_facecolor('#2C2F33')

        # Añadir gráficos a la interfaz
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Configurar gráficos
        self.configurar_graficos()

        # Crear el temporizador para actualizar cada 5 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.recargar_mapa)
        self.timer.start(5000)  # 5000 milisegundos = 5 segundos

        # Generar coordenadas iniciales para el mapa
        self.latitud, self.longitud = self.generar_coordenadas()
        self.mapa_url = f"https://www.google.com/maps/place/{self.latitud},{self.longitud}/@{self.latitud},{self.longitud},15z"
        self.web_view.setUrl(QUrl(self.mapa_url))  # Mostrar el mapa inicial

        # Crear la animación
        self.anim = animation.FuncAnimation(self.fig, self.actualizar_graficos, interval=1000, cache_frame_data=False)

        # Altitud inicial y temperatura a la que empieza el lanzamiento
        self.altitud_inicial = 653
        self.temperatura_inicial = 22

    def generar_datos(self):
        if len(self.tiempo) == 0:
            nuevo_tiempo = 0
        else:
            nuevo_tiempo = self.tiempo[-1] + 1
        
        # Lógica de altitud y temperatura
        if nuevo_tiempo <= 40:  # Ascenso durante los primeros 40 segundos
            nueva_altitud = self.altitud_inicial + (nuevo_tiempo / 40) * (1653 - self.altitud_inicial)  # Ascenso hasta 1653 m
        else:
            tiempo_descenso = nuevo_tiempo - 40
            nueva_altitud = 1653 - (1000 / (60 - 40)) * tiempo_descenso  # Descenso hasta 653 m
            if nueva_altitud < self.altitud_inicial:
                nueva_altitud = self.altitud_inicial  # Limitar la altitud a 653 m

        # Temperatura inversamente relacionada con la altitud, ajustada a 22 °C en 653 m
        nueva_temperatura = self.temperatura_inicial - ((nueva_altitud - self.altitud_inicial) / 100) * 5  # Ejemplo de relación

        # Agregar datos a las listas
        self.tiempo.append(nuevo_tiempo)
        self.altitud.append(nueva_altitud)
        self.temperatura.append(nueva_temperatura)
        
        # Limitar la cantidad de datos en pantalla
        if len(self.tiempo) > 100:
            self.tiempo.pop(0)
            self.altitud.pop(0)
            self.temperatura.pop(0)

    def configurar_graficos(self):
        self.axs[0].set_title("Altura (m)", color='white')
        self.axs[0].set_xlabel("Tiempo (s)", color='white')
        self.axs[0].set_ylabel("Altura", color='white')
        self.axs[0].tick_params(colors='white')
        self.axs[0].set_facecolor('#23272A')
        self.axs[0].grid(True, color='#4E5D6C', linestyle='--', linewidth=0.5)

        self.axs[1].set_title("Temperatura (°C)", color='white')
        self.axs[1].set_xlabel("Tiempo (s)", color='white')
        self.axs[1].set_ylabel("Temperatura", color='white')
        self.axs[1].tick_params(colors='white')
        self.axs[1].set_facecolor('#23272A')
        self.axs[1].grid(True, color='#4E5D6C', linestyle='--', linewidth=0.5)

    def actualizar_graficos(self, i):
        self.generar_datos()

        # Gráfico de Altitud
        self.axs[0].clear()
        self.axs[0].plot(self.tiempo, self.altitud, color='#39FF14')
        self.configurar_graficos()

        # Añadir flecha en el gráfico de Altitud
        if len(self.altitud) > 1:
            self.axs[0].annotate('', xy=(self.tiempo[-1], self.altitud[-1]), xytext=(self.tiempo[-2], self.altitud[-2]),
                                 arrowprops=dict(arrowstyle='->', color='white', lw=1.5))

        # Gráfico de Temperatura
        self.axs[1].clear()
        self.axs[1].plot(self.tiempo, self.temperatura, color='#FFD700')
        self.configurar_graficos()

        # Añadir flecha en el gráfico de Temperatura
        if len(self.temperatura) > 1:
            self.axs[1].annotate('', xy=(self.tiempo[-1], self.temperatura[-1]), xytext=(self.tiempo[-2], self.temperatura[-2]),
                                 arrowprops=dict(arrowstyle='->', color='white', lw=1.5))

    def recargar_mapa(self):
        # Actualizar el mapa con nuevas coordenadas
        self.latitud, self.longitud = self.generar_coordenadas()
        # URL de Google Maps con marcador en la posición exacta
        self.mapa_url = f"https://www.google.com/maps/place/{self.latitud},{self.longitud}/@{self.latitud},{self.longitud},15z"
        self.web_view.setUrl(QUrl(self.mapa_url))  # Actualizar el mapa

    def generar_coordenadas(self):
        latitud = random.uniform(36.0, 43.8)  # Rango de latitudes en España
        longitud = random.uniform(-9.5, 3.0)  # Rango de longitudes en España
        return latitud, longitud

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MapaVentana()
    ventana.show()
    sys.exit(app.exec_())