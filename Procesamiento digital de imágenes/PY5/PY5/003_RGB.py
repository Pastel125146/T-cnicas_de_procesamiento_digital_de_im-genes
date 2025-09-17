import py5  # Importa la librería py5 para crear gráficos

def setup():
    """
    Función que se ejecuta una sola vez al inicio del programa.
    Se encarga de inicializar el entorno gráfico y establecer propiedades básicas,
    como el tamaño de la ventana, el modo de color y la ausencia de contorno en las figuras.
    """
    py5.size(600, 200)  # Define el tamaño de la ventana gráfica a 600x200 píxeles.
    py5.color_mode(py5.RGB, 255) # Establece el modo de color en RGB con valores entre 0 y 255 para cada canal (rojo, verde, azul).
    py5.no_stroke()  # Desactiva el borde/contorno de las figuras.


def draw():
    """
    Función que se ejecuta continuamente en cada frame (cuadro) del programa.
    Se encarga de dibujar los elementos gráficos en la ventana,
    mostrando rectángulos con diferentes colores representando los canales rojo, verde y azul.
    """
    # Canal Rojo
    py5.fill(255, 0, 0)  # Establece el color de relleno a rojo (RGB: 255, 0, 0).
    py5.rect(0, 0, 200, 200) # Dibuja un rectángulo con la esquina superior izquierda en (0, 0), ancho de 200 píxeles y alto de 200 píxeles.

    # Canal Verde
    py5.fill(0, 255, 0)  # Establece el color de relleno a verde (RGB: 0, 255, 0).
    py5.rect(200, 0, 200, 200) # Dibuja un rectángulo con la esquina superior izquierda en (200, 0), ancho de 200 píxeles y alto de 200 píxeles.

    # Canal Azul
    py5.fill(0, 0, 255)  # Establece el color de relleno a azul (RGB: 0, 0, 255).
    py5.rect(400, 0, 200, 200) # Dibuja un rectángulo con la esquina superior izquierda en (400, 0), ancho de 200 píxeles y alto de 200 píxeles.


py5.run_sketch() # Ejecuta el programa py5, iniciando la ventana gráfica y comenzando el bucle principal de renderizado.