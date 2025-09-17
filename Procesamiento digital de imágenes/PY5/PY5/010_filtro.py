import py5  # Importa la biblioteca py5 para crear gráficos interactivos con Python y Java.

def setup():
    """
    La función 'setup' se ejecuta una sola vez al inicio del programa.
    Se utiliza para inicializar el entorno de dibujo, como establecer el tamaño de la ventana.
    """
    py5.size(400, 400)  # Establece el tamaño de la ventana a 400 píxeles de ancho y 400 píxeles de alto.

def draw():
    """
    La función 'draw' se ejecuta continuamente en un bucle, actualizando los gráficos cada frame.
    Se utiliza para dibujar elementos en la pantalla, como imágenes y formas.
    """
    img = py5.load_image("img/Pastel.jpg")  # Intenta cargar una imagen desde el archivo "img/Pastel.jpg".
    py5.image(img, 0, 0, 400, 400)  # Dibuja la imagen cargada en la ventana, comenzando en las coordenadas (0, 0) y con un tamaño de 400x400 píxeles.
    py5.apply_filter(py5.THRESHOLD, 0.8)  # Aplica un filtro de umbral a la imagen actual. 
    # El valor 0.8 define el nivel de umbral; los píxeles por debajo de este valor se convierten en negro y los que están por encima en blanco.

py5.run_sketch()  # Inicia el programa py5, ejecutando las funciones 'setup' y 'draw'.
