# app_cloud.py
"""
Aplicación Streamlit simplificada para detección de landmarks faciales.
Versión optimizada para Streamlit Community Cloud.
"""
import streamlit as st
from PIL import Image
from src.detector import FaceLandmarkDetector
from src.utils import pil_to_cv2, cv2_to_pil, resize_image
from src.config import TOTAL_LANDMARKS


# Configuración de la página
st.set_page_config(
    page_title="Detector de Landmarks Faciales",
    layout="centered"
)

# Título y descripción
st.title("Detector de Landmarks Faciales")
st.markdown("Aplicación para detectar puntos clave en rostros humanos usando MediaPipe.")

# Uploader de imagen
uploaded_file = st.file_uploader(
    "Sube una imagen con un rostro",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        # Cargar imagen
        imagen_original = Image.open(uploaded_file)

        # Convertir a formato OpenCV
        imagen_cv2 = pil_to_cv2(imagen_original)

        # Redimensionar si es muy grande
        imagen_cv2 = resize_image(imagen_cv2, max_width=800)

        # Mostrar imagen original
        st.subheader("Imagen Original")
        st.image(cv2_to_pil(imagen_cv2), use_container_width=True)

        # Detectar landmarks
        with st.spinner("Detectando landmarks..."):
            detector = FaceLandmarkDetector()
            imagen_procesada, landmarks, info = detector.detect(imagen_cv2)
            detector.close()

        # Mostrar imagen procesada
        st.subheader("Landmarks Detectados")
        st.image(cv2_to_pil(imagen_procesada), use_container_width=True)

        # Mostrar información
        if info["deteccion_exitosa"]:
            st.success("Detección exitosa")
            st.write(f"Rostros detectados: {info['rostros_detectados']}")
            st.write(f"Landmarks detectados: {info['total_landmarks']}/{TOTAL_LANDMARKS}")
        else:
            st.error("No se detectó ningún rostro")

    except Exception as e:
        st.error(f"Error procesando la imagen: {str(e)}")

else:
    st.info("Sube una imagen para comenzar")