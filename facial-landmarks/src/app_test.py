import streamlit as st

st.title("Test App")
st.write("Si ves esto, Streamlit Cloud funciona correctamente")

uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Imagen subida")
    st.success("Imagen procesada exitosamente")
else:
    st.info("Sube una imagen para probar")