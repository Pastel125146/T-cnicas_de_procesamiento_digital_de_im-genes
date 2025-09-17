import py5  # Importa la librería py5 para crear gráficos

def setup():
    """
    Función que se ejecuta una sola vez al inicio del programa.
    Se encarga de inicializar el entorno gráfico y establecer propiedades básicas,
    como el tamaño de la ventana, el modo de color en HSB (Hue, Saturation, Brightness)
    y la ausencia de contorno en las figuras.
    """
    py5.size(400, 400)  # Define el tamaño de la ventana gráfica a 400x400 píxeles.
    py5.color_mode(py5.HSB, 360, 100, 100) # Establece el modo de color en HSB (Hue, Saturation, Brightness).
                                            # Los valores están entre 0-360 para Hue, 0-100 para Saturation y 0-100 para Brightness.
    py5.no_stroke()  # Desactiva el borde/contorno de las figuras.


def draw():
    """
    Función que se ejecuta continuamente en cada frame (cuadro) del programa.
    Se encarga de dibujar una serie de rectángulos, cada uno con un color diferente basado en el ángulo Hue,
    creando un degradado de colores a lo largo de la parte superior de la ventana.
    """
    for i in range(360):  # Itera sobre los 360 grados del círculo de color (Hue).
        py5.fill(i, 100, 100) # Establece el color de relleno usando el valor actual de 'i' como Hue, con Saturation y Brightness fijados en 100.
        py5.rect(i, 0, 1, py5.height)  # Dibuja un rectángulo con la esquina superior izquierda en (i, 0), ancho de 1 píxel y alto igual a la altura de la ventana.


py5.run_sketch() # Ejecuta el programa py5, iniciando la ventana gráfica y comenzando el bucle principal de renderizado.
