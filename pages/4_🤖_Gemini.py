import streamlit as st
import google.generativeai as genai

# Configura la API Key de Google Generative AI
genai.configure(api_key=st.secrets.GEMINI.api_key)

# Selecciona el modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Crea la interfaz de usuario con Streamlit
st.title("🤖 Generador de Texto con Gemini")
user_input = st.text_input("Ingresa tu texto:")

# Genera el texto si se presiona el botón
if st.button("Generar"):
    if user_input:
        response = model.generate_content(user_input)
        st.write("Respuesta:", response.text)
    else:
        st.write("Por favor ingresa un texto.")