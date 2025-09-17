import py5  # Importa la librería py5 para gráficos.

def setup():
    """
    Función de configuración que se ejecuta una vez al inicio del programa.
    Define el tamaño de la ventana y prepara los píxeles para manipulación.
    """
    py5.size(400, 400)  # Define el tamaño de la ventana a 400x400 píxeles.

    py5.load_pixels()  # Carga el array de píxeles de la imagen para poder acceder y modificar cada píxel individualmente.
                       # Esto es necesario porque py5 no permite acceso directo a los píxeles sin esta llamada.

    # Crear un patrón de píxeles
    for x in range(py5.width):  # Itera sobre cada columna (eje x) de la imagen.
        for y in range(py5.height): # Itera sobre cada fila (eje y) de la imagen, dentro de cada columna.
            # Calcular índice en el array de píxeles
            index = x + y * py5.width  # Calcula el índice del píxel actual en el array lineal de píxeles.
                                        # Cada fila se concatena para formar un array unidimensional.

            # Crear patrón de colores
            r = (x * 255) // py5.width # Calcula el valor rojo (R) basado en la posición x.  Cuanto mayor es x, más rojo será el color.
                                        # Se multiplica por 255 para obtener un rango completo y se divide por el ancho de la imagen para normalizarlo.

            g = (y * 255) // py5.height # Calcula el valor verde (G) basado en la posición y. Cuanto mayor es y, más verde será el color.
                                        # Se multiplica por 255 para obtener un rango completo y se divide por la altura de la imagen para normalizarlo.

            b = 128  # Define el valor azul (B) como 128, que es un valor medio. Esto asegura que todos los píxeles tengan una cantidad constante de azul.

            py5.pixels[index] = py5.color(r, g, b) # Asigna el color calculado al píxel en la posición 'index' del array de píxeles.
                                                    # py5.color(r, g, b) crea un objeto color con los valores rojo, verde y azul especificados.

    py5.update_pixels()  # Actualiza la imagen con los cambios realizados en el array de píxeles. Esto es necesario para que los cambios sean visibles.


py5.run_sketch() # Ejecuta el programa py5, iniciando la ventana gráfica y comenzando el bucle principal de renderizado.
