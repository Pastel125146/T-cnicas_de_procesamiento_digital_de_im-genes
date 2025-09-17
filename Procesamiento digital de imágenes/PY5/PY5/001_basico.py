import py5  # Importa la librería py5 para crear gráficos

def setup():
    """
    Función que se ejecuta una sola vez al inicio del programa.
    Se encarga de inicializar el entorno gráfico y establecer propiedades básicas.
    """
    py5.size(400, 400)  # Define el tamaño de la ventana gráfica a 400x400 píxeles.
    py5.background(200) # Establece el color de fondo de la ventana a un gris medio (RGB: 200, 200, 200).
    print("py5 funcionando correctamente")  # Imprime un mensaje en la consola para confirmar que py5 se ha inicializado correctamente.


def draw():
    """
    Función que se ejecuta continuamente en cada frame (cuadro) del programa.
    Se encarga de dibujar los elementos gráficos en la ventana.
    """
    py5.fill(255, 0, 0)  # Establece el color de relleno a rojo (RGB: 255, 0, 0).
    py5.no_stroke() # Desactiva el borde/contorno de las figuras.
    py5.ellipse(200, 200, 100, 100)  # Dibuja una elipse centrada en (200, 200) con un ancho y alto de 100 píxeles.


py5.run_sketch() # Ejecuta el programa py5, iniciando la ventana gráfica y comenzando el bucle principal de renderizado.
