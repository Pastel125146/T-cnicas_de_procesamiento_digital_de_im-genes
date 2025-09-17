import py5  # Importa la biblioteca py5 para gráficos.

img = None  # Variable global que almacenará la imagen cargada.

def setup():
    """Función que se ejecuta una vez al inicio del programa."""
    global img
    py5.size(400, 400)  # Tamaño de la ventana
    py5.background(255)  #  (255 es el valor RGB para blanco).

    try:
        # Intentamos cargar la imagen desde la carpeta
        img = py5.load_image("img/Pastel.jpg")
    except Exception as e:
        print(f"⚠️ Error: coloca una imagen en 'img/Pastel.jpg'. Detalles: {e}")
        return  # Si no hay imagen, salimos de setup

    if img is not None:
        procesar_imagen()  # Procesar la imagen apenas se carga

def procesar_imagen():
    """Procesa la imagen invirtiendo colores."""
    global img
    img.load_pixels()  # Accedemos a los píxeles de la imagen
    for i in range(len(img.pixels)):
        c = img.pixels[i] #Obtiene el color del píxel actual 
        # -- Invertimos cada canal de color (R, G, B)--
        # Tomamos el valor actual de Rojo, Verde y  Azul
        # Restamos 255 a cada uno. Esto es como si restáramos la máxima cantidad posible de cada ingrediente.
        # El resultado es el nuevo color invertido.
        r = 255 - py5.red(c) # Calcula el nuevo valor para el canal rojo (r) invirtiendo su valor original. Si el valor original de rojo era 100, el nuevo valor será 255 - 100 = 155.
        g = 255 - py5.green(c)
        b = 255 - py5.blue(c)
        img.pixels[i] = py5.color(r, g, b)
    img.update_pixels()  # Actualizamos los píxeles modificados

def draw():
    """Función que se ejecuta en bucle para dibujar en la ventana."""
    if img:
        py5.image(img, 0, 0, 400, 400)  # Dibujamos la imagen procesada

# Arrancamos el sketch
py5.run_sketch()
