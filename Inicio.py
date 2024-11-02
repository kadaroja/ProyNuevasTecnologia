import streamlit as st
from PIL import Image
import io
import base64

def image_to_base64(image):
    """Convierte una imagen PIL a base64 para usar en HTML."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

st.set_page_config(layout="wide", page_title="Proyecto Integrador", page_icon="💻")

# Cargar la imagen
image = Image.open("static/Logo.png")

# Centrar la imagen usando HTML
st.markdown(
    f"<div style='text-align: center;'><img src='data:image/png;base64,{image_to_base64(image)}' width='300'></div>",
    unsafe_allow_html=True
)

# Integrantes
st.write("En nuestro equipo encontrarás respaldo y profesionalismo, con habilidades destacadas e innovación en cada paso.")

_, col1, col2, _ = st.columns([1, 2, 2, 1])    # Columna vacía a la derecha e izquierda para centrar

with col1:
    st.image("static/Gabriel.png", width=80)  # Reemplaza con la ruta de la foto
    st.write("**Gabriel Patiño**")
    st.write("Product Owner")

with col2:
    st.image("static/Karla.png", width=130)  # Reemplaza con la ruta de la foto
    st.write("**Karla Rodriguez**")
    st.write("Scrum Master")
# Segunda fila con tres columnas
col3, col4, col5 = st.columns(3)

with col3:
    st.image("static/Alejandro.png", width=110)  # Reemplaza con la ruta de la foto
    st.write("**Alejandro Muñoz**")
    st.write("Desarrollador Web")

with col4:
    st.image("static\Usuario1.png", width=140)  # Reemplaza con la ruta de la foto
    st.write("**Carla Karina**")
    st.write("Desarrollador Web")

with col5:
    st.image("static/user.png", width=100)  # Reemplaza con la ruta de la foto
    st.write("**Victor Manuel**")
    st.write("Desarrollador Web")

# Descripción del proyecto
st.header("Concimiento")
st.write("""Somos estudiantes capacitados en la creación de proyectos en Streamlit, utilizando librerías como pandas y conectándonos a bases de datos con Firebase.""")

# Más información
st.header("Proyectos")
st.write("""Desarrollamos tres tipos de proyectos analizando diversas fuentes de datos para obtener información más precisa y fácil de comprender.""")

# redes sociales
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <a href="https://www.instagram.com">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" style="width: 40px; margin: 0 10px;">
        </a>
        <a href="https://www.facebook.com">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" style="width: 40px; margin: 0 10px;">
        </a>
        <a href="https://www.linkedin.com">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo.svg" alt="LinkedIn" style="width: 40px; margin: 0 10px;">
        </a>
    </div>
    """,
        unsafe_allow_html=True,
)