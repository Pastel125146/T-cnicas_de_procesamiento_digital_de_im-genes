# app.py
"""
Aplicación Streamlit para detección de landmarks faciales.
"""
import streamlit as st
from PIL import Image
from src.detector import FaceLandmarkDetector
from src.utils import pil_to_cv2, cv2_to_pil, resize_image
from src.config import TOTAL_LANDMARKS

# ====================================
# CONFIGURACIÓN DE LA PÁGINA
# ====================================
st.set_page_config(
    page_title="Detector de Landmarks Faciales",
    layout="centered"
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
# PROCESAMIENTO
# ====================================
if uploaded_file is not None:
    # Cargar y convertir imagen
    imagen_original = Image.open(uploaded_file)
    imagen_cv2 = pil_to_cv2(imagen_original)

    # Redimensionar si es muy grande
    imagen_cv2 = resize_image(imagen_cv2, max_width=800)

    # Mostrar imagen original
    st.subheader("📸 Imagen Original")
    st.image(cv2_to_pil(imagen_cv2))

    # Detección de landmarks
    with st.spinner("🧠 Detectando landmarks faciales..."):
        detector = FaceLandmarkDetector()
        imagen_procesada, landmarks, info = detector.detect(imagen_cv2)
        detector.close()

    # Mostrar resultado
    st.subheader("✅ Landmarks Detectados")
    st.image(cv2_to_pil(imagen_procesada))

    # Mostrar métricas
    st.divider()
    if info["deteccion_exitosa"]:
        st.success("🎯 Detección exitosa")

        st.write(f"**Rostros detectados:** {info['rostros_detectados']}")
        st.write(f"**Landmarks detectados:** {info['total_landmarks']}/{TOTAL_LANDMARKS}")

        porcentaje = (info['total_landmarks'] / TOTAL_LANDMARKS) * 100
        st.metric("Precisión estimada", f"{porcentaje:.1f}%")
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
    st.image(
        "https://ai.google.dev/static/mediapipe/images/solutions/face_landmarker_keypoints.png?hl=es-419",
        caption="MediaPipe detecta 478 landmarks faciales",
        width=400
    )
