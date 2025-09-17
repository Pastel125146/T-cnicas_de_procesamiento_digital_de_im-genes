import py5

# Función que se ejecuta una sola vez al inicio del sketch
def setup():
    global img  # Declaramos img como variable global para usarla en draw()
    py5.size(800, 450)  # Definimos el tamaño de la ventana del sketch

    try:
        # Intentamos cargar la imagen desde la carpeta especificada
        img = py5.load_image("img/Pastel.jpg")  # Cambiar por ruta válida si es necesario
    except Exception as e:
        # Si hay un error (ej: archivo no encontrado), lo mostramos en consola
        print(f"Error loading image: {e}")
        img = None  # Evitamos que img quede indefinida

# Función que se ejecuta en bucle mientras el sketch está corriendo
def draw():
    if img:  # Verificamos que la imagen se haya cargado correctamente
        # Mostrar la imagen original (escalada a 400x400 en la esquina superior izquierda)
        py5.image(img, 0, 0, 400, 400)

        # Mostrar la misma imagen redimensionada (200x200) en la parte derecha
        py5.image(img, 400, 0, 200, 200)

        # Mostrar texto con información de la imagen
        py5.fill(0)  # Color negro para el texto
        py5.text(f"Original: {img.width} x {img.height}", 10, 20)

#  Esto arranca el sketch
py5.run_sketch()



