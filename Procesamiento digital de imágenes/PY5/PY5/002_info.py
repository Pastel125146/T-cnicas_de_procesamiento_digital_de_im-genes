import py5  # Importa la librería py5 para crear gráficos

def setup():
    """
    Función que se ejecuta una sola vez al inicio del programa.
    Se encarga de inicializar el entorno gráfico y establecer propiedades básicas,
    como el tamaño de la ventana y el color de fondo.
    """
    py5.size(800, 600)  # Define el tamaño de la ventana gráfica a 800x600 píxeles (resolución HD 4:3).
    py5.background(220) # Establece el color de fondo de la ventana a un gris claro (RGB: 220, 220, 220).

    # Mostrar información de la ventana en la consola
    print(f"Ancho: {py5.width} píxeles")  # Imprime el ancho de la ventana en píxeles.
    print(f"Alto: {py5.height} píxeles") # Imprime el alto de la ventana en píxeles.
    print(f"Total píxeles: {py5.width * py5.height}")  # Calcula e imprime el número total de píxeles en la ventana.


py5.run_sketch() # Ejecuta el programa py5, iniciando la ventana gráfica y comenzando el bucle principal de renderizado.
