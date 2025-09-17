import py5  # Importa la biblioteca py5 para gráficos.

def setup():
    """Función que se ejecuta una vez al inicio del programa."""
    py5.size(400, 400)  # Establece el tamaño de la ventana a 400x400 píxeles.
    py5.rect_mode(py5.CENTER)  # Define que las coordenadas de los rectángulos se refieran al centro del rectángulo.


def draw():
    """Función que se ejecuta continuamente en cada frame."""
    py5.square(py5.mouse_x, py5.mouse_y, 10)  # Dibuja un cuadrado centrado en la posición actual del mouse con una longitud de lado de 10 píxeles.


def mouse_pressed():
    """Función que se ejecuta cuando se presiona el botón del mouse."""
    py5.fill(py5.random_int(255), py5.random_int(255), py5.random_int(255))  # Establece el color de relleno a un color aleatorio generado usando py5.random_int(255) para cada componente RGB (rojo, verde y azul).


py5.run_sketch()  # Inicia el programa py5.
