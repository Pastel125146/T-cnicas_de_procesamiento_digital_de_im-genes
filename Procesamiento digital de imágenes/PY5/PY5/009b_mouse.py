import py5  # Importa la biblioteca py5 para gráficos.

def setup():
    """Función que se ejecuta una vez al inicio del programa."""
    py5.size(400, 300)  # Establece el tamaño de la ventana a 400x300 píxeles.
    py5.background(255)  # Establece el color de fondo a blanco (255).
    print("py5 funcionando correctamente")  # Imprime un mensaje en la consola para verificar que py5 se está ejecutando.


def draw():
    """Función que se ejecuta continuamente en cada frame."""
    py5.background(255)  # Limpia el fondo a blanco en cada frame para evitar que los círculos se acumulen.

    # Solo dibujar el círculo si el mouse está dentro de la ventana
    if 0 <= py5.mouse_x <= py5.width and 0 <= py5.mouse_y <= py5.height:  # Verifica si las coordenadas del mouse están dentro de los límites de la ventana.
        py5.fill(255, 0, 0)  # Establece el color de relleno a rojo (R=255, G=0, B=0).
        py5.circle(py5.mouse_x, py5.mouse_y, 20)  # Dibuja un círculo centrado en la posición del mouse con un diámetro de 20 píxeles.


py5.run_sketch()  # Inicia el programa py5.
