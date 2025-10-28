# app.py
"""
Aplicación Streamlit para detección de landmarks faciales.
Optimizada para evitar errores de frontend (removeChild).
"""
import streamlit as st
from PIL import Image
from src.detector import FaceLandmarkDetector
from src.utils import (
    pil_to_cv2, cv2_to_pil, resize_image,
    calcular_apertura_boca, calcular_apertura_ojos, calcular_inclinacion_cabeza,
    landmarks_to_dict
)
from src.config import TOTAL_LANDMARKS
import json

# ====================================
# CONFIGURACIÓN DE LA PÁGINA
# ====================================
st.set_page_config(
    page_title="Detector de Landmarks Faciales",
    layout="centered",
    page_icon="💡"
)

# ====================================
# ENCABEZADO PRINCIPAL
# ====================================
st.title("💡 Detector de Landmarks Faciales")
st.markdown("""
Esta aplicación detecta **478 puntos clave** en rostros humanos usando *MediaPipe*.
Subí una imagen con un rostro y mirá cómo la visión por computadora hace su magia.
""")

# ====================================
# SIDEBAR INFORMATIVA
# ====================================
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    ### ¿Qué son los Landmarks?
    Son puntos de referencia que mapean:
    - 👁️ Ojos (iris, párpados)
    - 👃 Nariz (puente, fosas)
    - 👄 Boca (labios, comisuras)
    - 🧠 Contorno facial
    
    ### Aplicaciones
    - 🎭 Filtros AR (Instagram, Snapchat)
    - 😃 Análisis de expresiones
    - 🎬 Animación facial
    - 🔐 Autenticación biométrica
    """)
    st.divider()
    st.caption("Desarrollado en el Laboratorio 2 - IFTS24")

# ====================================
# SUBIDA DE IMAGEN
# ====================================
uploaded_file = st.file_uploader(
    "📤 Subí una imagen con un rostro",
    type=["jpg", "jpeg", "png"],
    help="Formatos aceptados: JPG, JPEG, PNG"
)

# ====================================
# PLACEHOLDERS DINÁMICOS
# ====================================
placeholder_original = st.empty()
placeholder_resultado = st.empty()
placeholder_demo = st.empty()
placeholder_metrics = st.empty()
placeholder_json = st.empty()

# ====================================
# PROCESAMIENTO DE IMAGEN
# ====================================
if uploaded_file:
    imagen_original = Image.open(uploaded_file)
    imagen_cv2 = pil_to_cv2(imagen_original)
    imagen_cv2 = resize_image(imagen_cv2, max_width=800)

    # Mostrar imagen original
    st.subheader("📸 Imagen Original")
    placeholder_original.image(cv2_to_pil(imagen_cv2))

    # Detección de landmarks
    with st.spinner("🧠 Detectando landmarks faciales..."):
        detector = FaceLandmarkDetector()
        imagen_procesada, landmarks, info = detector.detect(imagen_cv2)
        detector.close()

    # Mostrar resultado
    st.subheader("✅ Landmarks Detectados")
    placeholder_resultado.image(cv2_to_pil(imagen_procesada))

    # Métricas y análisis
    placeholder_metrics.empty()
    if info["deteccion_exitosa"]:
        with placeholder_metrics.container():
            st.success("🎯 Detección exitosa")
            st.write(f"**Rostros detectados:** {info['rostros_detectados']}")
            st.write(f"**Landmarks detectados:** {info['total_landmarks']}/{TOTAL_LANDMARKS}")
            porcentaje = (info['total_landmarks'] / TOTAL_LANDMARKS) * 100
            st.metric("Precisión estimada", f"{porcentaje:.1f}%")

            st.subheader("😃 Análisis de Expresiones Faciales")
            alto, ancho = imagen_cv2.shape[:2]
            apertura_boca = calcular_apertura_boca(landmarks, alto, ancho)
            apertura_ojos_izq, apertura_ojos_der = calcular_apertura_ojos(landmarks, alto, ancho)
            inclinacion_cabeza = calcular_inclinacion_cabeza(landmarks, alto, ancho)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Apertura Boca", f"{apertura_boca:.1f} px")
            with col2:
                st.metric("Ojo Izq", f"{apertura_ojos_izq:.1f} px")
                st.metric("Ojo Der", f"{apertura_ojos_der:.1f} px")
            with col3:
                st.metric("Inclinación Cabeza", f"{inclinacion_cabeza:.1f}°")

        # Botón de descarga JSON
        landmarks_json = json.dumps(landmarks_to_dict(landmarks, alto, ancho), indent=2)
        placeholder_json.download_button(
            label="📥 Descargar Landmarks (JSON)",
            data=landmarks_json,
            file_name="landmarks.json",
            mime="application/json"
        )
    else:
        st.error("🚫 No se detectó ningún rostro en la imagen")
        st.info("""
        **Consejos**:
        - Asegurate de que el rostro esté bien iluminado
        - Que mire hacia la cámara
        - Probá con una imagen más nítida
        """)

# ====================================
# PANTALLA INICIAL (SIN IMAGEN)
# ====================================
else:
    st.info("Subí una imagen para comenzar la detección 👇")
    st.markdown("### Ejemplo de Resultado")
    placeholder_demo.image(
        "https://ai.google.dev/static/mediapipe/images/solutions/face_landmarker_keypoints.png?hl=es-419",
        caption="MediaPipe detecta 478 landmarks faciales",
        width=400
    )



