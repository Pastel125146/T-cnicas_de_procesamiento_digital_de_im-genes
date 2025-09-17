import py5  # Importa la librería py5 para gráficos interactivos


def setup():
    """Se ejecuta una vez al inicio."""
    py5.size(500, 500)  # Define el tamaño de la ventana en 500x500 píxeles
    py5.background(0)  # Pone el fondo inicial en negro
    print("py5 funcionando correctamente")  # Mensaje en consola para confirmar que se ejecuta bien


def draw():
    """Se ejecuta en cada frame (aprox. 60 veces por segundo)."""
    py5.background(0)  # Redibuja el fondo negro cada frame para limpiar la pantalla

    # Calculamos las coordenadas del centro de la ventana
    cx, cy = py5.width // 2, py5.height // 2

    # Dibujar el círculo solo si el mouse está dentro de la ventana
    if 0 <= py5.mouse_x <= py5.width and 0 <= py5.mouse_y <= py5.height:
        # Calculamos la distancia entre el mouse y el centro
        dist_mouse = py5.dist(py5.mouse_x, py5.mouse_y, cx, cy)

        # Mapeamos la distancia a un tamaño de círculo (cerca = grande, lejos = chico)
        input_min, input_max = 0, py5.width // 2  # Rango de distancias posibles (mínimo = centro, máximo = borde)
        output_min, output_max = 80, 20  # Rango de diámetros del círculo (máximo tamaño = 80, mínimo tamaño = 20)
        circle_size = output_min + (dist_mouse - input_min) * (output_max - output_min) / (input_max - input_min)

        # Aseguramos que el tamaño no se salga del rango [20, 80]
        circle_size = max(20, min(circle_size, 80))

        # Dibujamos el círculo blanco en la posición del mouse
        py5.fill(255)  # Relleno blanco
        py5.no_stroke()  # Sin borde
        py5.circle(py5.mouse_x, py5.mouse_y, circle_size)  # Dibuja el círculo con diámetro dinámico

        # Mostrar información en pantalla
        py5.fill(255)  # Texto en blanco
        py5.text_size(16)
        py5.text(f"Distancia al centro: {dist_mouse:.2f}", 10, 20)
        py5.text(f"Tamaño del círculo: {circle_size:.2f}", 10, 40)

    # Dibujamos un triángulo rojo en el centro (encima del círculo)
    py5.fill(255, 0, 0)  # Relleno rojo
    py5.no_stroke()  # Sin borde
    py5.triangle(cx - 10, cy + 10, cx + 10, cy + 10, cx, cy - 10)  # Triángulo pequeño apuntando hacia arriba


py5.run_sketch()  # Inicia la ejecución del sketch

# -- la posición la decide el mouse, pero el tamaño depende de la distancia al centro --

# ventana negra de 500x500
#  En el centro hay un triángulo rojo fijo
#  El mouse controla un círculo blanco cuyo tamaño depende de qué tan cerca está del centro
#  es más grande cuando se acerca, más chico cuando se aleja.
#  Arriba a la izquierda se muestra texto con la distancia al centro y el tamaño actual del círculo.





