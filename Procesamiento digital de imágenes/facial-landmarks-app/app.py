# app.py
"""
Aplicación Streamlit para detección de landmarks faciales.
"""
import streamlit as st
from PIL import Image
from src.detector import FaceLandmarkDetector
from src.utils import pil_to_cv2, cv2_to_pil, resize_image
from src.config import TOTAL_LANDMARKS

# Configuración de la página
st.set_page_config(page_title="Detector de Landmarks Faciales", layout="centered")

# Encabezado
st.title("💡 Detector de Landmarks Faciales")
st.markdown("""
Detecta **478 puntos clave** en rostros humanos usando *MediaPipe*.
Subí una imagen con un rostro y mirá cómo la visión por computadora hace su magia.
""")

# Sidebar informativa
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    ### ¿Qué son los Landmarks?
    - 👁️ Ojos
    - 👃 Nariz
    - 👄 Boca
    - 🧠 Contorno facial
    
    ### Aplicaciones
    - 🎭 Filtros AR
    - 😃 Análisis de expresiones
    - 🎬 Animación facial
    - 🔐 Autenticación biométrica
    """)
    st.caption("Desarrollado en el Laboratorio 2 - IFTS24")

# Subida de imagen
uploaded_file = st.file_uploader(
    "📤 Subí una imagen con un rostro",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    # Cargar y convertir
    imagen_original = Image.open(uploaded_file)
    imagen_cv2 = pil_to_cv2(imagen_original)
    imagen_cv2 = resize_image(imagen_cv2, max_width=800)

    # Imagen original
    st.subheader("📸 Imagen Original")
    st.image(cv2_to_pil(imagen_cv2), width=600)

    # Detectar landmarks
    with st.spinner("🧠 Detectando landmarks..."):
        detector = FaceLandmarkDetector()
        imagen_procesada, landmarks, info = detector.detect(imagen_cv2)
        detector.close()

    # Imagen procesada
    st.subheader("✅ Landmarks Detectados")
    st.image(cv2_to_pil(imagen_procesada), width=600)

    # Métricas
    if info.get("deteccion_exitosa", False):
        st.success("🎯 Detección exitosa")
        st.write(f"**Rostros detectados:** {info['rostros_detectados']}")
        st.write(f"**Landmarks detectados:** {info['total_landmarks']}/{TOTAL_LANDMARKS}")
        porcentaje = (info['total_landmarks'] / TOTAL_LANDMARKS) * 100
        st.write(f"**Precisión estimada:** {porcentaje:.1f}%")
    else:
        st.error("🚫 No se detectó ningún rostro")
        st.info("Asegurate de que la cara esté iluminada y mirando a la cámara.")

else:
    st.info("Subí una imagen para comenzar 👇")
    st.markdown("### Ejemplo de Resultado")
    st.image(
        "https://ai.google.dev/static/mediapipe/images/solutions/face_landmarker_keypoints.png?hl=es-419",
        width=400
    )

