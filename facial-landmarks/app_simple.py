# app_simple.py
"""
Aplicación Streamlit simplificada para detección de landmarks faciales.
Usa face_recognition en lugar de MediaPipe para mejor compatibilidad con Streamlit Cloud.
"""
import streamlit as st
import face_recognition
import cv2
import numpy as np
from PIL import Image


# Configuración de la página
st.set_page_config(
    page_title="Detector de Landmarks Faciales",
    layout="centered"
)

# Título y descripción
st.title("Detector de Landmarks Faciales")
st.markdown("Aplicación para detectar puntos clave en rostros humanos usando face_recognition.")

# Uploader de imagen
uploaded_file = st.file_uploader(
    "Sube una imagen con un rostro",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        # Cargar imagen con PIL
        image = Image.open(uploaded_file)
        image_array = np.array(image)

        # Convertir a RGB si es necesario
        if image_array.shape[2] == 4:  # RGBA
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        elif len(image_array.shape) == 2:  # Grayscale
            image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)

        # Redimensionar si es muy grande
        height, width = image_array.shape[:2]
        if width > 800:
            ratio = 800 / width
            new_width = 800
            new_height = int(height * ratio)
            image_array = cv2.resize(image_array, (new_width, new_height))

        # Mostrar imagen original
        st.subheader("Imagen Original")
        st.image(image_array, channels="RGB", use_container_width=True)

        # Detectar rostros y landmarks
        with st.spinner("Detectando landmarks..."):
            # Encontrar ubicaciones de rostros
            face_locations = face_recognition.face_locations(image_array)

            # Obtener landmarks faciales
            face_landmarks_list = face_recognition.face_landmarks(image_array)

        # Dibujar landmarks en la imagen
        image_with_landmarks = image_array.copy()

        for face_landmarks in face_landmarks_list:
            # Dibujar landmarks para cada rostro
            for facial_feature in face_landmarks.keys():
                for point in face_landmarks[facial_feature]:
                    cv2.circle(image_with_landmarks, point, 2, (0, 255, 0), -1)

        # Mostrar imagen procesada
        st.subheader("Landmarks Detectados")
        st.image(image_with_landmarks, channels="RGB", use_container_width=True)

        # Mostrar información
        num_faces = len(face_locations)
        total_landmarks = sum(len(landmarks) for face_landmarks in face_landmarks_list for landmarks in face_landmarks.values())

        if num_faces > 0:
            st.success("Detección exitosa")
            st.write(f"Rostros detectados: {num_faces}")
            st.write(f"Landmarks detectados: {total_landmarks}")
        else:
            st.error("No se detectó ningún rostro")

    except Exception as e:
        st.error(f"Error procesando la imagen: {str(e)}")

else:
    st.info("Sube una imagen para comenzar")
