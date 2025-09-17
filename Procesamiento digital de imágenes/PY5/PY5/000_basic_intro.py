# Importa la biblioteca py5 para crear gráficos interactivos con Python y Java.
# py5 es una envoltura de Python alrededor de Processing, un entorno de programación visual.
# Permite combinar la sintaxis sencilla de Python con el rendimiento de Java (a través de la JVM).
import py5

def setup():
    """
    Función que se ejecuta una vez al inicio del programa para configurar el entorno gráfico.
    En Processing/py5, esta función es obligatoria y se llama automáticamente.
    """
    # Define el tamaño de la ventana gráfica a 500 píxeles de ancho por 500 píxeles de alto.
    py5.size(500, 500)

    # Establece el color de relleno para las formas en rojo (#FF0000).
    py5.fill("#FF0000") #FF representa la cantidad de Rojo (Red) - en este caso, el valor máximo (255).
 #00 representa la cantidad de Verde (Green) - en este caso, nada de verde.
 #00 representa la cantidad de Azul (Blue) - en este caso, nada de azul.

    # Dibuja un rectángulo con la esquina superior izquierda en (100, 150),
    # con un ancho de 200 píxeles y una altura de 300 píxeles.
    py5.rect(100, 150, 200, 300)

    # Guarda la imagen actual en un archivo llamado "000_intro_py5.png"
    # en el directorio "/img/testing/".  Asegúrate de que este directorio exista.
    py5.save("/img/testing/000_intro_py5.png")


# Ejecuta el sketch (programa) de py5. Esta línea es esencial para iniciar la aplicación gráfica.
py5.run_sketch()
