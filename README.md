# Facial Landmarks Detection App

Una aplicación web para detectar landmarks faciales usando MediaPipe y Streamlit.

## Descripción

Esta aplicación permite detectar y visualizar hasta 478 puntos clave en rostros humanos. Utiliza MediaPipe para la detección y Streamlit para la interfaz web interactiva.

## Estructura del Proyecto

```
facial-landmarks-app/
│
├── venv/                    # Entorno virtual (no subir a Git)
│
├── src/
│   ├── detector.py          # Lógica de detección de landmarks
│   ├── utils.py             # Funciones auxiliares (conversión de imágenes)
│   └── config.py            # Configuración (parámetros del modelo)
│
├── app.py                   # Aplicación Streamlit principal
│
├── requirements.txt         # Dependencias del proyecto
├── .gitignore              # Archivos a ignorar en Git
└── README.md               # Documentación del proyecto
```

## Instalación

1. Crear entorno virtual:
   ```
   python -m venv venv
   ```

2. Activar el entorno virtual:
   - En Windows: `venv\Scripts\activate`
   - En Linux/Mac: `source venv/bin/activate`

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Ejecutar la aplicación:
   ```
   streamlit run app.py
   ```

## Uso

1. Abre la aplicación en tu navegador (generalmente http://localhost:8501).
2. Sube una imagen con un rostro usando el uploader.
3. La aplicación mostrará la imagen original y la procesada con landmarks detectados.
4. Verás métricas como número de rostros detectados y precisión.

## Dependencias

- MediaPipe: Para detección de landmarks faciales (requiere Python 3.7-3.11).
- OpenCV: Procesamiento de imágenes.
- Streamlit: Interfaz web.
- Pillow: Manejo de imágenes PIL.
- NumPy: Operaciones numéricas.
- Requests: Descargas HTTP.

## Notas

- Asegúrate de que el rostro esté bien iluminado y mirando hacia la cámara para mejores resultados.
- La aplicación detecta hasta 1 rostro por imagen por defecto.
- Desarrollado como parte del Laboratorio 2 - IFTS24.

## Deployment

Para desplegar en Streamlit Cloud:

1. Sube el proyecto a GitHub (sin la carpeta venv).
2. Conecta tu repositorio en Streamlit Cloud.
3. Configura el archivo principal como `app.py`.

## Contribución

Siéntete libre de contribuir mejorando el código o agregando nuevas funcionalidades.