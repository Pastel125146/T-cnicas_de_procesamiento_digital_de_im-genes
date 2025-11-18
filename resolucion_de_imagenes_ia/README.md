# Sistema de Resolución de Imágenes con IA

Una aplicación web interactiva construida con Streamlit que utiliza modelos de inteligencia artificial avanzados para mejorar la resolución de imágenes, restaurar de rostros de fotos antiguas y aplicar colorización automática.

## Usuario Objetivo

**Persona: María González**

**Nombre:** María González
**Edad:** 22 años
**Ocupación:** Estudiante de Bellas Artes en la universidad
**Contexto tecnológico:** Intermedio - usa Photoshop y herramientas básicas de edición, conoce redes sociales pero no ha trabajado con IA avanzada.

**Problema actual:**
Necesito mejorar la resolución de mis dibujos escaneados y fotos de mis obras de arte para presentaciones y portafolios, pero las imágenes salen pixeladas y de baja calidad.

**Solución actual:**
Uso Photoshop para intentar mejorar manualmente, pero toma mucho tiempo y los resultados no son profesionales.

**Frustraciones:**
- Pierdo mucho tiempo editando imágenes manualmente
- Las herramientas gratuitas no dan resultados buenos para arte

**Objetivos:**
- Mejorar rápidamente la calidad de mis imágenes artísticas
- Crear portafolios impresionantes para concursos y exposiciones

**Contexto de uso:**
En su laptop en la universidad o en casa, cuando prepara trabajos finales o portafolios, sube imágenes y aplica mejoras con unos clics.

## Características Principales

- **Mejora de Resolución**: Utiliza Real-ESRGAN (x4plus y x4plus-anime) para aumentar la resolución hasta 4x.
- **Restauración Facial**: Integración con GFPGAN para restaurar rostros en fotos antiguas.
- **Colorización Automática**: Modelo de Zhang basado en OpenCV y Caffe para colorizar imágenes en blanco y negro.
- **Ajustes Avanzados**: Controles para desenfoque, enfoque, resaltar detalles, suavizar, iluminación y reducción de ruido.
- **Análisis de Imagen**: Métricas automáticas (PSNR, SSIM) y análisis avanzado opcional con Gemini AI.
- **Interfaz Intuitiva**: Diseño moderno con Streamlit, fácil de usar sin conocimientos técnicos avanzados.

## Requisitos del Sistema

- Python 3.9+
- Windows/Linux/macOS
- Conexión a internet (para análisis con Gemini AI opcional)

## Instalación y Uso

### 1. Preparación del Entorno

```bash
# Activar entorno virtual
venv\Scripts\activate  # En Windows
# o
source venv/bin/activate  # En Linux/macOS

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador web predeterminado en `http://localhost:8501`.

### 3. Uso Básico

1. Sube una imagen (JPG, PNG).
2. Selecciona el modelo de super-resolución.
3. Activa opciones como restauración facial si aplica.
4. Haz clic en "🚀 Mejorar Resolución" o "🧬 Restaurar rostros de fotos dañadas".
5. Ajusta parámetros avanzados según necesites.
6. Descarga el resultado.

## Modelos Incluidos

- **Real-ESRGAN**: Para upscaling general y anime.
- **GFPGAN**: Para restauración facial.
- **Colorización Zhang**: Para colorizar imágenes automáticamente.
- **Haar Cascade**: Para detección de rostros.

## Estructura del Proyecto

```
RESOLUCION_DE_IMAGENES/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── .env                   # Variables de entorno (API keys)
├── .gitignore            # Archivos ignorados por Git
├── models/               # Modelos auxiliares
│   ├── colorization/     # Modelos de colorización
│   ├── eccv16.py         # Script de procesamiento
│   └── haarcascade_frontalface_default.xml
├── gfpgan/               # Modelos GFPGAN
├── realesrgan/           # Modelos Real-ESRGAN
├── weights/              # Pesos adicionales
└── venv/                 # Entorno virtual (no versionado)
```

## Configuración Avanzada

### API Key de Gemini (Opcional)

Para análisis avanzado con IA:
1. Obtén una API key gratuita en [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea un archivo `.env` con:
   ```
   GEMINI_API_KEY=tu_api_key_aqui
   ```

### Personalización

Los modelos y pesos están incluidos, pero puedes actualizarlos descargando versiones más recientes de los repositorios oficiales.

## Contribución

Si encuentras bugs o tienes sugerencias:
1. Abre un issue en el repositorio.
2. Describe el problema o mejora propuesta.
3. Incluye capturas de pantalla si aplica.

## Licencias

- **Streamlit**: Apache 2.0
- **Real-ESRGAN**: MIT
- **GFPGAN**: MIT
- **Modelos de colorización**: Licencia académica (no comercial)

## Créditos

- Basado en modelos de investigación de Tencent ARC, Xintao Wang, et al.
- Interfaz desarrollada con Streamlit.
- Inspirado en herramientas de procesamiento de imágenes con IA.

---

**Nota**: Esta aplicación es para uso personal y educativo. Los modelos de IA pueden tener limitaciones en ciertos tipos de imágenes.
