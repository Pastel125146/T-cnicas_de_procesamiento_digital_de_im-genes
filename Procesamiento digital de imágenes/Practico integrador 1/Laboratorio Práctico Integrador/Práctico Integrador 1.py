# --------------- Generación de Imágenes con py ---------------

# Ejercicio 1: Figura en Espacio de Color RGB

import py5

# def setup():
    # Lienzo 400x400
#    py5.size(400, 400)

    # Modo de color en RGB
#    py5.color_mode(py5.RGB)

    # Fondo blanco
#    py5.background(255)

    # Cuadrado rojo sin borde
#    py5.no_stroke()
#    py5.fill(255, 0, 0)  # Rojo puro

    # Coordenadas del cuadrado
#    py5.rect(100, 100, 200, 200)

    # Guardar como JPEG
#    py5.save_frame('figura_rgb.jpg')

#    py5.no_loop()

#py5.run_sketch()

# -----------------------------------------------------------------------

# Ejercicio 2: Figura en Espacio de Color HSV

#def setup():
#    py5.size(400, 400)  # Lienzo 400x400
#    py5.color_mode(py5.HSB, 360, 100, 100)  # Modo de color HSV
#    py5.background(0, 0, 100)  # Saturación=0, Brillo=100 → fondo blanco
#    py5.no_stroke()      # Sin borde

    # círculo con Hue=200 (azulado), Saturación=80, Brillo=100
#    py5.fill(200, 80, 100)
#    py5.ellipse(200, 200, 200, 200)  # Círculo centrado

    # Guardar imagen
#    py5.save_frame('figura_hsv.jpg')

#    py5.no_loop()

#py5.run_sketch()

# -----------------------------------------------------------------------

# Ejercicio 3: Cámara Oscura 

def setup():
    global img1, img2  # Declaramos variables globales
    py5.size(800, 450)

    try:
        # Cargar las dos imágenes desde la carpeta "img"
        img1 = py5.load_image("img/pastel1.jpg")
        img2 = py5.load_image("img/pastel2.jpg")
    except Exception as e:
        print(f"Error loading image: {e}")
        img1, img2 = None, None

def draw():
    py5.background(255)  # Fondo blanco

    if img1:
        # Mostrar imagen 1 en la izquierda
        py5.image(img1, 0, 0, 400, 400)
        py5.fill(0)
        py5.text(f"Imagen 1: {img1.width}x{img1.height}", 10, 20)

    if img2:
        # Mostrar imagen 2 en la derecha
        py5.image(img2, 400, 0, 400, 400)
        py5.fill(0)
        py5.text(f"Imagen 2: {img2.width}x{img2.height}", 410, 20)

py5.run_sketch()
