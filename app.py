import streamlit as st
st.set_page_config(
    page_title="Sistema de Resolución de Imágenes con IA",
    layout="wide",
    initial_sidebar_state="expanded"
)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from PIL import Image
import numpy as np
import google.generativeai as genai
import torch
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import cv2
import time
import io

from huggingface_hub import hf_hub_download

# --- Colorización con modelo de Zhang (OpenCV + Caffe) ---

@st.cache_resource
def load_colorizer_zhang():
    """Carga el modelo de colorización de Zhang con pts_in_hull.npy"""
    model_dir = os.path.join(BASE_DIR, "models", "colorization")
    prototxt = os.path.join(model_dir, "colorization_deploy_v2.prototxt")
    caffemodel = os.path.join(model_dir, "colorization_release_v2.caffemodel")
    pts_path = os.path.join(model_dir, "pts_in_hull.npy")

    net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
    pts_in_hull = np.load(pts_path)  # 313x2

    # Cargar los cluster centers al blob final
    class8_ab = net.getLayerId('class8_ab')
    conv8_313_rh = net.getLayerId('conv8_313_rh')
    pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8_ab).blobs = [pts_in_hull.astype(np.float32)]
    net.getLayer(conv8_313_rh).blobs = [np.ones([1, 313], dtype=np.float32)]

    return net

def colorize_with_zhang(image: Image.Image, net):
    """Coloriza una imagen PIL usando el modelo de Zhang"""
    img_rgb = np.array(image.convert("RGB"))
    img_rgb = img_rgb.astype(np.float32) / 255.0
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    L = img_lab[:, :, 0]

    # Redimensionar a 224x224
    L_rs = cv2.resize(L, (224, 224))
    L_rs -= 50  # centrar

    net.setInput(cv2.dnn.blobFromImage(L_rs))
    ab_dec = net.forward()[0, :, :, :].transpose((1, 2, 0))  # HxWx2

    ab_dec_us = cv2.resize(ab_dec, (img_rgb.shape[1], img_rgb.shape[0]))
    img_lab_out = np.concatenate((L[:, :, np.newaxis], ab_dec_us), axis=2)
    img_bgr_out = cv2.cvtColor(img_lab_out, cv2.COLOR_LAB2RGB)
    img_bgr_out = np.clip(img_bgr_out, 0, 1)

    return Image.fromarray((img_bgr_out * 255).astype(np.uint8))

def safe_np(img):
    img = np.asarray(img)
    if img is None:
        raise ValueError("Imagen procesada es None")
    if img.dtype == object:
        img = img.astype(np.uint8)
    if len(img.shape) != 3 or img.shape[2] not in [1,3,4]:
        raise ValueError(f"Imagen inválida: shape={img.shape}, dtype={img.dtype}")
    return img
def safe_pil_from_np(img):
    img = np.asarray(img)
    if img is None:
        raise ValueError("Imagen es None")
    if img.dtype == object:
        img = img.astype(np.uint8)
    if len(img.shape) == 2:  # grayscale
        return Image.fromarray(img, mode="L")
    elif len(img.shape) == 3:
        if img.shape[2] == 3:
            return Image.fromarray(img, mode="RGB")
        elif img.shape[2] == 4:
            return Image.fromarray(img, mode="RGBA")
    raise ValueError(f"Imagen inválida: shape={img.shape}, dtype={img.dtype}")

FACE_CASCADE_PATH = os.path.join(BASE_DIR, "models", "haarcascade_frontalface_default.xml")

if "face_cascade" not in st.session_state:
    print("CARGANDO CASCADE EN:", FACE_CASCADE_PATH)
    if os.path.exists(FACE_CASCADE_PATH):
        cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
        if cascade.empty():
            st.error("❌ El archivo existe, pero OpenCV no pudo cargarlo (posible corrupción).")
            cascade = None
    else:
        st.error(f"❌ Archivo no encontrado en: {FACE_CASCADE_PATH}")
        cascade = None
    st.session_state["face_cascade"] = cascade
face_cascade = st.session_state["face_cascade"]

def get_selected_esrgan_method(processing_method):
    if processing_method == "Real-ESRGAN x4plus":
        return "x4plus"
    elif processing_method == "Real-ESRGAN x4plus-anime":
        return "x4plus-anime"
    return "x4plus"


# GFPGAN
from gfpgan import GFPGANer

# 🧠 Detección de rostro (OpenCV)
def detecta_rostros(image):
    if face_cascade is None or face_cascade.empty():
        return False

    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(40, 40)
    )

    return len(faces) > 0

# ============================================================
# 🧬 Restauración de foto antigua — Versión PRO corregida
# Sin cara plástica, sin efecto pintura, tonos naturales.
# ============================================================

def restaurar_foto_antigua(image):
    img = np.array(image.convert("RGB"))

    # --- 1. Limpieza suave pero NO agresiva ---
    # Solo remueve ruido fino sin borrar textura facial
    img = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)

    # --- 2. Scratch removal MUY controlado ---
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 120, 180)

    # Kernel reducido → evita tragarse rasgos de la cara
    kernel = np.ones((3, 3), np.uint8)
    scratches = cv2.dilate(edges, kernel, iterations=1)

    img = cv2.inpaint(img, scratches, 2, cv2.INPAINT_TELEA)

    # --- 3. Deblurring moderado ---
    # Te quedaba como "óleo"; bajamos intensidad
    blur = cv2.GaussianBlur(img, (3, 3), sigmaX=0.4)
    img = cv2.addWeighted(img, 1.15, blur, -0.15, 0)

    # --- 4. Restauración facial con blending adaptativo ---
    pil_img = Image.fromarray(img)
    if detecta_rostros(pil_img) and st.session_state.get("use_gfpgan", True):
        pil_img = restore_face_pro(pil_img)  # Nueva versión PRO
        img = np.array(pil_img)

    # --- 5. Upscale final (RealESRGAN) ---
    esrgan_method = get_selected_esrgan_method(
        st.session_state.get("processing_method_ui", "Real-ESRGAN x4plus")
    )

    img = safe_np(img)
    print("SANITY CHECK:", img.shape, img.dtype, type(img))
    final = upscale_image(safe_pil_from_np(img), method=esrgan_method, scale_factor=2)

    return final

def procesar_imagen_con_pasos(imagen, method, scale_factor):
    """Misma lógica de tu procesamiento, pero mostrando barra + pasos."""
    steps = [
        "Cargando modelo de super-resolución…",
        "Preparando la imagen…",
        "Aplicando mejora de resolución…",
        "Optimizando detalles finales…",
        "Finalizando procesamiento…"
    ]

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, step in enumerate(steps):
        status_text.write(step)
        time.sleep(0.4)  # reemplazar por delays reales si querés
        progress_bar.progress((i+1) / len(steps))

    # Ahora ejecutamos tu pipeline REAL
    processed = upscale_image(imagen, method=method, scale_factor=scale_factor)
    return processed

# Función de upscaling simple usando interpolación (siempre funciona)
def simple_upscale(image, scale_factor=2):
    """Upscaling simple pero efectivo usando interpolación bicúbica"""
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


# Cargar modelo Real-ESRGAN local (implementación oficial)
def load_realesrgan_model(model_name):
    try:
        import sys, os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'realesrgan'))

        from realesrgan import RealESRGAN
        import torch

        device = torch.device("cpu")

        # Determinar si es modelo anime
        anime = "anime" in model_name

        model = RealESRGAN(device, scale=4, anime=anime)

        return model

    except Exception as e:
        print(f"Error cargando Real-ESRGAN ({model_name}): {e}")
        return None


def upscale_image(image, method="x4plus", scale_factor=2):
    """Función principal de upscaling con múltiples métodos y fallbacks robustos"""

    # REAL-ESRGAN: x4plus / anime
    if method in ["x4plus", "x4plus-anime"]:
        try:
            model = load_realesrgan_model(method)
            if model:
                img_rgb = image.convert("RGB")
                upscaled = model.predict(img_rgb)
                return upscaled
        except Exception as e:
            print(f"Real-ESRGAN falló ({method}): {e}")

    # Fallback universal
    return simple_upscale(image, scale_factor)


# --- GFPGAN: Restauración de rostros ---
@st.cache_resource
def load_gfpgan():
    gfpganer = GFPGANer(
        model_path="https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth",
        upscale=1,
        arch='clean',
        channel_multiplier=2,
        bg_upsampler=None
    )
    return gfpganer

def restore_face_pro(image):
    gfpganer = load_gfpgan()
    img = np.array(image.convert("RGB"))

    # Procesar cara
    _, restored_faces, restored_img = gfpganer.enhance(
        img,
        has_aligned=False,
        only_center_face=False
    )

    if not restored_faces:
        return image

    return safe_pil_from_np(restored_img)

# --- Función para resaltar o suavizar detalles ---
def apply_frequency_filter(image, mode="resaltar"):
    """Aplica un filtro de frecuencia para resaltar o suavizar detalles."""
    img_arr = np.array(image).astype(np.float32)

    # Transformada rápida: filtro simple con kernel de enfoque/desenfoque
    if mode == "resaltar":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        img_arr = cv2.filter2D(img_arr, -1, kernel)
    elif mode == "suavizar":
        ksize = 5
        img_arr = cv2.GaussianBlur(img_arr, (ksize, ksize), 0)

    img_arr = np.clip(img_arr, 0, 255).astype(np.uint8)
    return safe_pil_from_np(img_arr)


def apply_denoising(image, level=50):
    """Aplica FastNlMeansDenoising Colored con intensidad variable."""
    img_arr = np.array(image.convert("RGB"))
    # Calculamos h y h_color en base al nivel (0-100)
    # Por ejemplo, h varía de 3 a 15, y h_color de 3 a 15
    h = max(3, int(level / 100 * 12 + 3)) # 3 a 15
    h_color = h

    # Aplicar densoising. El templateWindowSize y searchWindowSize se mantienen fijos o se ajustan menos
    img_denoised = cv2.fastNlMeansDenoisingColored(
        img_arr,
        None,
        h,          # h (luminancia)
        h_color,    # h_color (cromatismo)
        7,          # templateWindowSize
        21          # searchWindowSize
    )
    return safe_pil_from_np(img_denoised)


def analyze_images_basic(original: Image.Image, processed: Image.Image):
    """Análisis visual compacto y estilizado tipo 'tarjeta' usando solo Streamlit moderno."""
    try:
        orig_size = original.size
        proc_size = processed.size
        scale_factor = proc_size[0] / orig_size[0]

        orig_arr = np.array(original.convert("RGB"))
        proc_arr = np.array(processed.convert("RGB"))
        proc_crop = proc_arr[:orig_arr.shape[0], :orig_arr.shape[1]]

        # Métricas principales
        psnr = peak_signal_noise_ratio(orig_arr, proc_crop, data_range=255)
        ssim = structural_similarity(orig_arr, proc_crop, channel_axis=2, data_range=255, win_size=7)
        brightness = proc_arr.mean()
        contrast = proc_arr.std()
        saturation = np.std(proc_arr[...,1]-proc_arr[...,2])
        texture = cv2.Laplacian(proc_arr, cv2.CV_64F).var()

        metrics = [
            ("Resolución", f"{orig_size[0]}×{orig_size[1]} → {proc_size[0]}×{proc_size[1]} ({scale_factor:.1f}×)"),
            ("Nitidez (PSNR)", f"{psnr:.1f} dB — {'Alta' if psnr>=25 else 'Moderada' if psnr>=20 else 'Baja'}"),
            ("Estructura (SSIM)", f"{ssim:.3f} — {'Muy buena' if ssim>=0.8 else 'Aceptable' if ssim>=0.6 else 'Mejorable'}"),
            ("Brillo promedio", f"{brightness:.0f} — {'Oscuro' if brightness<80 else 'Claro' if brightness>180 else 'Equilibrado'}"),
            ("Contraste", f"{contrast:.1f} — {'Bajo' if contrast<40 else 'Alto' if contrast>85 else 'Moderado'}"),
            ("Saturación", f"{saturation:.1f} — {'Suave' if saturation<15 else 'Intensa' if saturation>60 else 'Equilibrada'}"),
            ("Textura fina", f"{texture:.1f} — {'Poca' if texture<50 else 'Excesiva' if texture>300 else 'Moderada'}")
        ]

        # Renderizar métricas con st.container tipo tarjeta
        for name, val in metrics:
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color:#1f1f1f;
                        color:#f0f0f0;
                        padding:10px 15px;
                        border-radius:8px;
                        box-shadow:0 2px 4px rgba(0,0,0,0.3);
                        margin-bottom:6px;">
                        <b>{name}:</b> {val}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Recomendaciones rápidas
        recommendations = []
        if brightness<80:
            recommendations.append("Explorar más iluminación")
        elif brightness>180:
            recommendations.append("Reducir luces para volumen")
        if contrast<40:
            recommendations.append("Aumentar sombras para dramatismo")
        elif contrast>85:
            recommendations.append("Suavizar contraste")
        if saturation<15:
            recommendations.append("Aumentar saturación")
        elif saturation>60:
            recommendations.append("Equilibrar colores")
        if texture<50:
            recommendations.append("Agregar textura suave")
        elif texture>300:
            recommendations.append("Reducir textura fina")

        if recommendations:
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color:#282828;
                        color:#ffd700;
                        padding:12px;
                        border-radius:8px;
                        box-shadow:0 2px 4px rgba(0,0,0,0.3);
                        margin-top:10px;">
                        <b>💡 Recomendaciones rápidas:</b> {' | '.join(recommendations)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"Error en análisis: {str(e)}")

def analyze_image_with_gemini(original: Image.Image, processed: Image.Image, api_key: str) -> str:
    """
    Análisis avanzado usando Gemini AI (modelo 2.0-flash).
    Compara la imagen original vs la procesada y devuelve un análisis educativo.
    """
    if not api_key:
        return "Análisis avanzado no disponible: Ingresa tu API key de Google en la barra lateral"

    try:
        # Configurar API de Gemini
        genai.configure(api_key=api_key)

        # Inicializar modelo Gemini correcto
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Función auxiliar: PIL -> bytes
        def pil_to_bytes(img: Image.Image) -> bytes:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()

        original_bytes = pil_to_bytes(original)
        processed_bytes = pil_to_bytes(processed)

        # Prompt educativo para análisis de imagen
        prompt = """
        Actúa como profesor de arte para estudiantes.
        Describe específicamente qué mejoras se lograron en términos de:
        - nitidez
        - detalle
        - color
        - artefactos visuales
        Explica de manera clara, educativa y útil para alumnos de arte digital.
        """

        # Generar respuesta de Gemini
        response = model.generate_content([
            prompt,
            {"mime_type": "image/png", "data": original_bytes},
            {"mime_type": "image/png", "data": processed_bytes},
        ])

        return response.text

    except Exception as e:
        return f"Error en análisis avanzado (Gemini): {str(e)}"

# Interfaz de Streamlit
st.title("Sistema de Resolución de Imágenes con IA")
st.write("Mejora la resolución de tus fotos antiguas usando modelos de difusión y análisis inteligente.")

# Sidebar para configuración
st.sidebar.header("🎨 Configuración del Sistema")

# Opciones de procesamiento
st.sidebar.subheader("⚙️ Opciones de Procesamiento")
processing_method = st.sidebar.selectbox(
    "Modelo de super-resolución:",
    ["Real-ESRGAN x4plus", "Real-ESRGAN x4plus-anime"],
    help="x4plus para fotos reales, x4plus-anime para ilustraciones 2D."
)

st.session_state["processing_method_ui"] = processing_method

scale_factor = 2.0  # Factor de escala fijo

st.sidebar.checkbox(
    "Restauración facial (GFPGAN)",
    value=True,
    key="use_gfpgan"
)

# Opciones de análisis
st.sidebar.subheader("🔍 Opciones de Análisis")
analysis_mode = st.sidebar.radio(
    "Tipo de análisis:",
    ["Básico automático (gratuito)", "Avanzado con IA (requiere API key)"],
    help="El análisis básico es gratuito y automático. El avanzado usa Gemini para explicaciones detalladas."
)

# API Keys
api_key = None
if analysis_mode == "Avanzado con IA (requiere API key)":
    api_key = st.sidebar.text_input("API Key de Google Gemini", type="password")
    st.sidebar.write("🔗 [Obtener API key gratuita](https://makersuite.google.com/app/apikey)")


# --- Ajustes avanzados de imagen ---
st.sidebar.subheader("🛠 Ajustes Avanzados de Imagen")
desenfoque_level = st.sidebar.slider("Desenfoque", 0, 100, 0, help="Cantidad de desenfoque a aplicar")
enfoque_level = st.sidebar.slider("Enfoque", 0, 100, 0, help="Incrementa la nitidez y define los bordes de la imagen")
resaltar_level = st.sidebar.slider("Resaltar Detalles", 0, 100, 0, help="Aumenta nitidez y realce de detalles")
suavizar_level = st.sidebar.slider("Suavizar Detalles", 0, 100, 0, help="Suaviza detalles finos y texturas")
iluminacion_level = st.sidebar.slider("Iluminación", 0, 100, 0, help="Ajuste de iluminación de la imagen")
sombra_level = st.sidebar.slider("Sombra/Contraste local", 0, 50, 0, help="Oscurece sombras y aumenta contraste local")

# NUEVO SLIDER
ruido_level = st.sidebar.slider("Limpieza de Ruido", 0, 100, 0, help="Elimina el ruido fino de la imagen")

# Información para estudiantes de arte
st.sidebar.subheader("🎓 Información para Artistas")
st.sidebar.info("""
💡 **Recomendaciones rápidas:**
- **Explorar más iluminación:** Imagen muy oscura → aumentar luces o exposición.
- **Reducir luces para volumen:** Imagen demasiado clara → bajar brillo.
- **Aumentar sombras para dramatismo:** Contraste bajo → enfatizar sombras.
- **Suavizar contraste:** Contraste alto → suavizar bordes y tonos.
- **Aumentar saturación:** Colores muy apagados → reforzar saturación.
- **Equilibrar colores:** Colores demasiado intensos → moderar saturación.
- **Agregar textura suave:** Textura baja → realzar detalles finos con filtros suaves.
- **Reducir textura fina:** Textura excesiva → aplicar suavizado o desenfoque leve.
""")

# 🎨 Colorización (moved)
st.sidebar.subheader("🎨 Colorización")
st.sidebar.info("Colorización con modelo de Zhang (OpenCV + Caffe) - Colorización automática basada en redes neuronales")
st.session_state.setdefault("colorizando", False)

# Upload de imagen
st.subheader("📤 Subir Imagen")
uploaded_file = st.file_uploader("Selecciona una imagen para mejorar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Cargar imagen
    original_image = Image.open(uploaded_file)

    # --- Inicializar variables de sesión ---
    if "img_mejorada" not in st.session_state:
        st.session_state["img_mejorada"] = None  # Imagen restaurada base
    if "img_final" not in st.session_state:
        st.session_state["img_final"] = None     # Imagen con ajustes aplicados

    # --- Layout de dos columnas ---
    col1, col2 = st.columns([1, 1.2])

    with col1:
        # Contenedor único para imagen principal
        final_container = st.empty()

        # Mostrar imagen original al inicio
        st.session_state["img_final"] = original_image
        final_container.image(
            st.session_state["img_final"],
            caption="🖼️ Imagen Original",
            width=600
        )

    # --- Botones alineados y con mismo estilo ---
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        mejorar = st.button(
            "🚀 Mejorar Resolución",
            type="primary",
            use_container_width=True
        )
    
    with col_btn2:
        restaurar = st.button(
            "🧬 Restaurar rostros de fotos dañadas",
            type="primary",  # << MATCH VISUAL
            use_container_width=True
        )

    # Acción del botón "Mejorar Resolución"
    if mejorar:
        processed_image = procesar_imagen_con_pasos(
            st.session_state["img_final"],
            method="x4plus" if processing_method=="Real-ESRGAN x4plus" else "x4plus-anime",
            scale_factor=scale_factor
        )
        st.session_state["img_mejorada"] = processed_image
        st.session_state["img_final"] = processed_image
        final_container.image(
            st.session_state["img_final"],
            caption="✨ Imagen Final Mejorada",
            width=600
        )

    # Acción del botón "Restaurar Foto Antigua"
    if restaurar:
        # Barra de progreso y texto
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Lista de pasos
        steps = [
            "Preparando imagen para restauración…",
            "Eliminando ruido fino…",
            "Corrigiendo rasguños y marcas…",
            "Suavizando detalles…",
            "Restaurando rostro si aplica…",
            "Upscale final para mayor detalle…",
            "Finalizando…"
        ]

        # Mostrar avance paso a paso
        for i, step in enumerate(steps):
            status_text.write(f"🛠 {step}")
            time.sleep(0.3)
            progress_bar.progress((i+1)/len(steps))

        # Procesamiento real
        final = restaurar_foto_antigua(st.session_state["img_final"])
        st.session_state["img_mejorada"] = final
        st.session_state["img_final"] = final

        # Actualizar la imagen en pantalla
        final_container.image(
            st.session_state["img_final"],
            caption="✨ Imagen Final Restaurada",
            width=600
        )
        st.success("Foto restaurada con éxito ✔️")

    # --- Aplicar ajustes dinámicamente ---
    if st.session_state["img_mejorada"]:
        img_to_show = st.session_state["img_mejorada"].copy()
        img_arr = np.array(img_to_show).astype(np.float32)

        # LIMPIEZA DE RUIDO (Aplicar antes que los filtros de frecuencia)
        if ruido_level > 0:
            # Usamos la nueva función apply_denoising con el nivel del slider
            img_to_show = apply_denoising(img_to_show, level=ruido_level)
            img_arr = np.array(img_to_show).astype(np.float32)

        # Desenfoque
        if desenfoque_level > 0:
            ksize = int(desenfoque_level // 5 * 2 + 1)
            img_arr = cv2.GaussianBlur(img_arr, (ksize, ksize), 0)
            img_arr = np.clip(img_arr, 0, 255)

        # Enfoque
        if enfoque_level > 0:
            k = enfoque_level / 50  # mezcla original vs sharpen
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]], dtype=np.float32)
            sharpened = cv2.filter2D(img_arr, -1, kernel)
            img_arr = cv2.addWeighted(img_arr, 1-k, sharpened, k, 0)
            img_arr = np.clip(img_arr, 0, 255)

        # Resaltar detalles
        if resaltar_level > 0:
            k = resaltar_level / 50  # intensidad
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]], dtype=np.float32)
            sharpened = cv2.filter2D(img_arr, -1, kernel)
            img_arr = cv2.addWeighted(img_arr, 1-k, sharpened, k, 0)
            img_arr = np.clip(img_arr, 0, 255)

        # Suavizar detalles
        if suavizar_level > 0:
            ksize = max(3, int(suavizar_level // 10 * 2 + 1))
            img_arr = cv2.GaussianBlur(img_arr, (ksize, ksize), 0)
            img_arr = np.clip(img_arr, 0, 255)

        # Iluminación
        if iluminacion_level != 0:
            factor = 1 + iluminacion_level / 100
            img_arr = img_arr * factor
            img_arr = np.clip(img_arr, 0, 255)

        # Sombra / contraste local
        if sombra_level > 0:
            alpha = 1 + sombra_level / 100 * 0.5  # Contraste máximo +50%
            beta = -sombra_level / 100 * 30       # Oscurecer sombras
            img_arr = np.clip(alpha*img_arr + beta, 0, 255)

        # Convertir de vuelta a imagen
        print("Min/Max antes de mostrar:", img_arr.min(), img_arr.max())
        img_arr = np.clip(img_arr, 0, 255).astype(np.uint8)
        img_to_show = safe_pil_from_np(img_arr)

        # Actualizar imagen final en sesión y contenedor
        st.session_state["img_final"] = img_to_show
        final_container.image(
            st.session_state["img_final"],
            caption="✨ Imagen Final Mejorada",
            width=600
        )

        # Análisis al lado derecho
        with col2:
            if analysis_mode == "Básico automático (gratuito)":
                analyze_images_basic(original_image, st.session_state["img_final"])

            elif analysis_mode == "Avanzado con IA (requiere API key)" and api_key:
                # Expander y botón para análisis manual
                with st.expander("🔍 Análisis Avanzado de Imagen con IA"):
                    if st.button("🧠 Generar Análisis Avanzado"):
                        with st.spinner("Generando análisis avanzado con Gemini... ⏳"):
                            gemini_result = analyze_image_with_gemini(original_image, st.session_state["img_final"], api_key)
                            st.session_state["gemini_result"] = gemini_result

                    # Mostrar solo si ya se generó
                    gemini_result = st.session_state.get("gemini_result", None)
                    if gemini_result:
                        st.markdown(
                            f"<div style='font-family:sans-serif; line-height:1.5;'>{gemini_result}</div>",
                            unsafe_allow_html=True
                        )

            # --- BOTONES DE ACCIÓN ADICIONALES ---
            st.markdown("### ⚡ Acciones Rápidas")
            button_labels = [
                "🎨 Colorización",
                "🧼 Limpiar Ruido", # Nuevo botón
                "💡 Iluminación",
                "🔍 Enfoque",
                "🌓 Sombra/Contraste",
                "✨ Resaltar Detalles",
                "💨 Desenfoque",
                "🌫 Suavizar Detalles"
            ]

            # Creamos las columnas para el diseño de 3
            columns = st.columns(3)

            for i, label in enumerate(button_labels):
                col = columns[i % 3] # Asigna cíclicamente a col1, col2, col3

                # Deshabilitar el botón de colorización mientras se está procesando
                disabled = False
                if label == "🎨 Colorización" and st.session_state.get("colorizando", False):
                    disabled = True

                if col.button(label, type="secondary", use_container_width=True, disabled=disabled):
                    # type="secondary" para diferenciarlos visualmente del botón principal
                    if label == "🎨 Colorización":
                        if st.session_state.get("img_final"):
                            st.session_state["colorizando"] = True
                            try:
                                with st.spinner("Aplicando colorización con modelo Zhang… ⏳"):
                                    net = load_colorizer_zhang()
                                    st.session_state["img_final"] = colorize_with_zhang(
                                        st.session_state["img_final"], net
                                    )
                                st.success("Colorización aplicada ✅")
                                final_container.image(
                                    st.session_state["img_final"],
                                    caption="✨ Imagen Final Mejorada",
                                    width=600
                                )
                            except Exception as e:
                                st.error(f"Colorización falló: {e}")
                            finally:
                                st.session_state["colorizando"] = False

                    # NUEVO: Lógica del botón de Limpiar Ruido
                    elif label == "🧼 Limpiar Ruido":
                        st.session_state["img_final"] = apply_denoising(
                            st.session_state["img_final"], level=ruido_level
                        )
                        st.info(f"Limpieza de Ruido aplicada: {ruido_level}%")

                    # El resto de los botones de ajuste (Iluminación, Desenfoque, etc.)
                    # que simplemente aplican los valores del slider y fuerzan un re-run
                    elif label == "💨 Desenfoque":
                        st.session_state["img_final"] = apply_frequency_filter(
                            st.session_state["img_final"], mode="suavizar"
                        )
                        st.info(f"Desenfoque aplicado: {desenfoque_level}%")
                    elif label == "💡 Iluminación":
                        st.info(f"Ajuste de iluminación aplicado: {iluminacion_level}%")
                    elif label == "🔍 Enfoque":
                        st.session_state["img_final"] = apply_frequency_filter(
                            st.session_state["img_final"], mode="resaltar"
                        )
                        st.info(f"Enfoque aplicado: {enfoque_level}%")
                    elif label == "🌓 Sombra/Contraste":
                        st.info(f"Sombra/Contraste aplicado: {sombra_level}%")
                    elif label == "✨ Resaltar Detalles":
                        st.session_state["img_final"] = apply_frequency_filter(
                            st.session_state["img_final"], mode="resaltar"
                        )
                        st.info(f"Resaltar Detalles aplicado: {resaltar_level}%")
                    elif label == "🌫 Suavizar Detalles":
                        st.session_state["img_final"] = apply_frequency_filter(
                            st.session_state["img_final"], mode="suavizar"
                        )
                        st.info(f"Suavizar Detalles aplicado: {suavizar_level}%")

        # --- Línea decorativa antes de descargar ---
        st.markdown(
            """
            <hr style="
                border: 0;
                height: 2px;
                background: linear-gradient(to right, #ff6ec7, #ffcd3c, #6effc7, #6ec7ff);
                margin: 20px 0;
                border-radius: 5px;
            ">
            """,
            unsafe_allow_html=True
        )

        # --- Descargar ---
        st.subheader("💾 Descargar Resultado")
        if st.session_state["img_final"]:
            img_bytes = io.BytesIO()
            st.session_state["img_final"].save(img_bytes, format="PNG")
            img_bytes.seek(0)  # volver al inicio del buffer

            st.download_button(
                "⬇️ Descargar Imagen Mejorada",
                data=img_bytes,
                file_name=f"resultado_mejorado_{int(time.time())}.png",
                mime="image/png",
                type="primary"
            )

            # --- Mostrar comparación Original vs Mejorada ---
            st.markdown("### 🖼️ Comparación Antes / Después")
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.image(original_image, caption="📷 Original", use_column_width=True)
            with comp_col2:
                st.image(st.session_state["img_final"], caption="✨ Mejorada", use_column_width=True)