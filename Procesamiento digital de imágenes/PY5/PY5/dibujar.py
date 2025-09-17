import py5  # Importa la biblioteca py5 para gráficos

# Lista de colores disponibles + el negro como borrador (comentado con su nombre)
colores = [
    (255, 0, 0),    # Rojo
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarillo
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Naranja
    (255, 192, 203),# Rosa
    (0, 0, 0)       # Borrador (negro)
]

color_actual = colores[0]  # Color seleccionado inicialmente
barra_altura = 40          # Altura de la barra de colores
radio = 20                 # Radio de los círculos (tamaño del pincel)

def setup():
    py5.size(400, 400)     # Tamaño de la ventana
    py5.background(0)      # Fondo negro
    py5.no_stroke()        # Sin borde en los círculos

def draw():
    # Dibuja círculos si el mouse está presionado y fuera de la barra de colores
    if py5.is_mouse_pressed and py5.mouse_y < py5.height - barra_altura:
        py5.fill(*color_actual)                # Aplica el color seleccionado
        py5.circle(py5.mouse_x, py5.mouse_y, radio)  # Dibuja círculo en la posición del mouse
    
    # Dibuja la barra de colores en la parte inferior
    ancho_celda = py5.width / len(colores)      # Ancho de cada celda de color
    for i, c in enumerate(colores):             # Itera sobre cada color
        py5.fill(*c)                            # Aplica el color de la celda
        py5.rect(i * ancho_celda, py5.height - barra_altura, ancho_celda, barra_altura)  # Dibuja la celda

def mouse_pressed():
    global color_actual
    # Cambia el color actual si clickeamos dentro de la barra de colores
    if py5.mouse_y > py5.height - barra_altura:
        ancho_celda = py5.width / len(colores)       # Calcula ancho de cada celda
        indice = int(py5.mouse_x // ancho_celda)    # Determina el índice del color clickeado
        color_actual = colores[indice]              # Actualiza el color seleccionado

def key_pressed():
    # Limpia la pantalla con la tecla C
    if py5.key == 'c' or py5.key == 'C':
        py5.background(0)  # Restablece el fondo negro

py5.run_sketch()  # Inicia el sketch de py5


