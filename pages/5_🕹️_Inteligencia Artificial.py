import streamlit as st
import requests
import time

# Tu clave API de Hugging Face
HF_API_KEY = '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'  # Sustituye con tu clave API

# URL de la API de Hugging Face (Stable Diffusion alternativo)
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

# Función para generar una imagen
def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    data = {
        "inputs": prompt,
    }

    # Reintentos automáticos
    for _ in range(5):  # Hasta 5 intentos
        response = requests.post(API_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.content  # Imagen en binario
        elif response.status_code == 503:
            st.warning("El modelo está cargándose. Reintentando en 30 segundos...")
            time.sleep(30)  # Espera 30 segundos antes de reintentar
        else:
            st.error(f"Error al generar imágenes: {response.status_code}")
            st.write("Detalles del error:", response.text)
            return None
    st.error("No se pudo generar la imagen después de varios intentos.")
    return None

# Interfaz de Streamlit
def main():
    st.title("🕹️ Generador de Imágenes con Hugging Face")
    st.write("Escribe una palabra para generar imágenes con inteligencia artificial usando Stable Diffusion.")

    # Entrada del usuario
    prompt = st.text_input("Introduce una palabra o frase:")

    if st.button("Generar Imágenes"):
        if prompt:
            st.write(f"Generando 2 imágenes relacionadas para: **{prompt}**")

            # Variar los prompts ligeramente
            prompts = [
                f"{prompt}, estilo artístico",
                f"{prompt}, ilustración detallada"
            ]

            # Generar dos imágenes
            images = []
            for i, custom_prompt in enumerate(prompts):
                st.write(f"Generando imagen {i + 1} con el prompt: {custom_prompt}...")
                image_data = generate_image(custom_prompt)
                if image_data:
                    images.append(image_data)

            # Mostrar las imágenes generadas
            if images:
                st.write("**Imágenes generadas:**")
                cols = st.columns(2)  # Dividir en 2 columnas
                for i, img in enumerate(images):
                    with cols[i]:
                        st.image(img, caption=f"Imagen {i + 1}", use_column_width=True)
        else:
            st.warning("Por favor, ingresa una palabra o frase.")

if __name__ == "__main__":
    main()
