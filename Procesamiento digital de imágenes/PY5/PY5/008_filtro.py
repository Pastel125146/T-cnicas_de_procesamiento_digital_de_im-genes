import py5  # Importa la biblioteca py5 para gráficos.

img = None  # Inicializa una variable global 'img' a None. Almacenará el objeto de la imagen creada.


def setup():
    """Función que se ejecuta una vez al inicio del programa."""
    global img  # Declara que estamos usando la variable global 'img'.
    py5.size(600, 200)  # Establece el tamaño de la ventana a 600x200 píxeles.
    img = py5.create_image(200, 200, py5.RGB)  # Crea un objeto imagen con formato RGB.

    # Crear imagen de prueba
    img.load_pixels()  # Carga los píxeles de la imagen para poder modificarlos.
    for i in range(len(img.pixels)):  # Itera sobre cada píxel de la imagen.
        img.pixels[i] = py5.color(py5.random(255), py5.random(255), py5.random(255))  # Asigna un color aleatorio (R, G, B) a cada píxel.
    img.update_pixels()  # Actualiza la imagen con los nuevos colores de los píxeles.


def draw():
    """Función que se ejecuta continuamente en cada frame."""
    # Imagen original
    py5.image(img, 0, 0)  # Dibuja la imagen original en la posición (0, 0).

    # Solo canal rojo
    py5.tint(255, 0, 0)  # Aplica un tinte que solo permite pasar el canal rojo (R=255, G=0, B=0).
    py5.image(img, 200, 0)  # Dibuja la imagen con el tinte aplicado en la posición (200, 0).

    # Solo canal verde
    py5.tint(0, 255, 0)  # Aplica un tinte que solo permite pasar el canal verde (R=0, G=255, B=0).
    py5.image(img, 400, 0)  # Dibuja la imagen con el tinte aplicado en la posición (400, 0).

    py5.no_tint()  # Desactiva el tinte para que las siguientes imágenes se dibujen sin ningún efecto de color.


py5.run_sketch()  # Inicia el programa py5.

# El código crea una imagen con colores aleatorios
#  luego dibuja esa imagen tres veces: una vez sin ningún efecto de color
#  una vez con un tinte que solo permite ver el canal rojo
#  y otra vez con un tinte que solo permite ver el canal verde. 
# Esto demuestra cómo los diferentes componentes de color contribuyen a la apariencia general de una imagen.