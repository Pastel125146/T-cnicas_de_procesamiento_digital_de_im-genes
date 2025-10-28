# src/utils.py
"""
Funciones auxiliares para procesamiento de imágenes.
"""
import cv2
import numpy as np
from PIL import Image
import math
import json


def pil_to_cv2(pil_image):
    """
    Convierte una imagen PIL a formato OpenCV (numpy array BGR).
    
    Args:
        pil_image (PIL.Image): Imagen en formato PIL
    
    Returns:
        numpy.ndarray: Imagen en formato OpenCV (BGR)
    """
    # Convertir PIL a RGB numpy array
    rgb_array = np.array(pil_image.convert('RGB'))
    # Convertir RGB a BGR (formato OpenCV)
    bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
    return bgr_array


def cv2_to_pil(cv2_image):
    """
    Convierte una imagen OpenCV a formato PIL.
    
    Args:
        cv2_image (numpy.ndarray): Imagen en formato OpenCV (BGR)
    
    Returns:
        PIL.Image: Imagen en formato PIL (RGB)
    """
    # Convertir BGR a RGB
    rgb_array = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    # Convertir a PIL
    pil_image = Image.fromarray(rgb_array)
    return pil_image


def resize_image(image, max_width=800):
    """
    Redimensiona la imagen manteniendo el aspect ratio.
    
    Args:
        image (numpy.ndarray): Imagen OpenCV
        max_width (int): Ancho máximo deseado
    
    Returns:
        numpy.ndarray: Imagen redimensionada
    """
    alto, ancho = image.shape[:2]
    
    if ancho > max_width:
        ratio = max_width / ancho
        nuevo_ancho = max_width
        nuevo_alto = int(alto * ratio)
        image = cv2.resize(image, (nuevo_ancho, nuevo_alto))
    
    return image
def calcular_apertura_boca(landmarks, alto, ancho):
    """
    Calcula la apertura de la boca basada en la distancia entre los labios.

    Args:
        landmarks: Objeto de landmarks de MediaPipe
        alto (int): Alto de la imagen
        ancho (int): Ancho de la imagen

    Returns:
        float: Distancia en píxeles entre el labio superior e inferior
    """
    # Landmark 13: labio superior
    # Landmark 14: labio inferior
    punto_superior = landmarks.landmark[13]
    punto_inferior = landmarks.landmark[14]

    y1 = punto_superior.y * alto
    y2 = punto_inferior.y * alto

    distancia = abs(y2 - y1)
    return distancia


def calcular_apertura_ojos(landmarks, alto, ancho):
    """
    Calcula la apertura de los ojos basada en la distancia entre párpados.

    Args:
        landmarks: Objeto de landmarks de MediaPipe
        alto (int): Alto de la imagen
        ancho (int): Ancho de la imagen

    Returns:
        tuple: (apertura_ojo_izquierdo, apertura_ojo_derecho) en píxeles
    """
    # Ojo izquierdo: landmarks 159 (párpado superior) y 145 (párpado inferior)
    # Ojo derecho: landmarks 386 (párpado superior) y 374 (párpado inferior)

    # Ojo izquierdo
    superior_izq = landmarks.landmark[159]
    inferior_izq = landmarks.landmark[145]
    apertura_izq = abs((superior_izq.y - inferior_izq.y) * alto)

    # Ojo derecho
    superior_der = landmarks.landmark[386]
    inferior_der = landmarks.landmark[374]
    apertura_der = abs((superior_der.y - inferior_der.y) * alto)

    return apertura_izq, apertura_der


def calcular_inclinacion_cabeza(landmarks, alto, ancho):
    """
    Calcula la inclinación de la cabeza usando landmarks de los ojos.

    Args:
        landmarks: Objeto de landmarks de MediaPipe
        alto (int): Alto de la imagen
        ancho (int): Ancho de la imagen

    Returns:
        float: Ángulo de inclinación en grados
    """
    # Usar landmarks de los ojos para calcular la inclinación
    # Landmark 33: esquina externa ojo izquierdo
    # Landmark 263: esquina externa ojo derecho

    ojo_izq = landmarks.landmark[33]
    ojo_der = landmarks.landmark[263]

    # Calcular la diferencia en coordenadas Y
    delta_y = (ojo_der.y - ojo_izq.y) * alto
    delta_x = (ojo_der.x - ojo_izq.x) * ancho

    # Calcular ángulo en radianes y convertir a grados
    angulo_radianes = math.atan2(delta_y, delta_x)
    angulo_grados = math.degrees(angulo_radianes)

    return angulo_grados


def landmarks_to_dict(landmarks, alto, ancho):
    """
    Convierte landmarks a diccionario exportable.

    Args:
        landmarks: Objeto de landmarks de MediaPipe
        alto (int): Alto de la imagen
        ancho (int): Ancho de la imagen

    Returns:
        list: Lista de diccionarios con coordenadas de landmarks
    """
    data = []
    for idx, punto in enumerate(landmarks.landmark):
        data.append({
            "id": idx,
            "x": punto.x * ancho,
            "y": punto.y * alto,
            "z": punto.z
        })
    return data
