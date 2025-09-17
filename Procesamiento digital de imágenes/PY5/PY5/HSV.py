import py5  # Importa la biblioteca py5 para crear gráficos interactivos con Python y Java.

def setup():
    """
    La función 'setup' se ejecuta una sola vez al inicio del programa.
    Se utiliza para inicializar el entorno de dibujo, como establecer el tamaño de la ventana y el modo de color.
    """
    py5.size(400, 400)  # Establece el tamaño de la ventana a 400 píxeles de ancho y 400 píxeles de alto.
    py5.color_mode(py5.HSB, 360, 100, 100)  # Define el modo de color en HSB (Hue, Saturation, Brightness). Los valores máximos para cada componente son 360 (Hue), 100 (Saturation) y 100 (Brightness).
    py5.background(200)  # Establece el color de fondo a un tono de gris usando HSB. El valor 200 representa el brillo en este caso, ya que los otros componentes no se especifican.
    print("py5 funcionando correctamente")  # Imprime un mensaje en la consola para confirmar que py5 se ha inicializado correctamente.


def draw():
    """
    La función 'draw' se ejecuta continuamente en un bucle, actualizando los gráficos cada frame.
    Se utiliza para dibujar elementos en la pantalla, como formas y líneas.
    """
    py5.fill(200, 80, 80)  # Establece el color de relleno a HSB 
    # (Hue: 200, Saturation: 80, Brightness: 80).
    #  Esto creará un color con una tonalidad específica y niveles de saturación y brillo definidos.

py5.run_sketch()  # Inicia el programa py5, ejecutando las funciones 'setup' y 'draw'.
