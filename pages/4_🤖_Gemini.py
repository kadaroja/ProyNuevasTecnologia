import streamlit as st
import google.generativeai as genai

# Configura la API Key de Google Generative AI
genai.configure(api_key=st.secrets.GEMINI.api_key)

# Selecciona el modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Crea la interfaz de usuario con Streamlit
st.title("🔍 Campos Laborales para Carreras Estudiantiles")
user_input = st.text_input("Ingresa el nombre de la carrera que te gustaría conocer los campos laborares donde te puedes desempeñar:")

# Genera el texto si se presiona el botón
if st.button("Conoce la respuesta"):
    if user_input:
        # Crea un prompt específico para generar información sobre los campos laborales
        prompt = f"¿Cuáles son los campos laborales para la carrera de {user_input}?"
        
        # Llama al modelo Gemini para generar la respuesta
        response = model.generate_content(prompt)
        
        # Muestra la respuesta generada
        st.write("Campos Laborales para la carrera de", user_input, ":")
        
        # Procesar y mostrar solo los campos laborales (eliminar ofertas laborales y gráficos)
        campos_laborales = response.text.split("\n")  # Suponiendo que cada campo laboral esté en una nueva línea
        
        for campo in campos_laborales:
            if campo.strip():  # Solo mostrar líneas no vacías
                st.write(f"- {campo.strip()}")
    else:
        st.write("Por favor ingresa una carrera estudiantil.")
