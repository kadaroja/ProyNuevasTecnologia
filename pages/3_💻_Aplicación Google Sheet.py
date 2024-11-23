import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configuración de la página de Streamlit
st.set_page_config(layout="wide")

# Título de la página
st.subheader("Analizador de Datos de Google Sheets")
st.markdown("""
Este código lee datos de una hoja de cálculo de Google llamada "Sheet1", procesa los datos con Pandas y actualiza una segunda hoja llamada "Sheet2" con tablas dinámicas y gráficos.
""")

# Definir los permisos para acceder a Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Obtener el ID de la hoja de cálculo desde la interfaz de Streamlit
SPREADSHEET_ID = st.text_input("ID de la hoja de cálculo")
RANGE1 = "Sheet1!A:G"  # Rango con las columnas necesarias
RANGE2 = "Sheet2!A:C"  # Rango de la hoja de destino

# Cargar las credenciales de Google Sheets desde los secretos
google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]
secrets_dict = google_sheet_credentials.to_dict()
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Función para leer los datos de la hoja de cálculo
def read_sheet():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
    values = result.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])  # Leer encabezados y datos
    return df

# Función para actualizar los datos en Sheet2
def update_sheet(df):
    body = {'values': df.values.tolist()}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE2,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result

# Función para crear la tabla resumen por Ciudad
def create_city_summary(df):
    summary = df.groupby('ciudad').size().reset_index(name='Cantidad')
    return summary

# Función para crear la tabla resumen por Cargo
def create_cargo_summary(df):
    summary = df.groupby('cargo').size().reset_index(name='Cantidad')
    return summary

# Función para crear la tabla resumen por Departamento
def create_department_summary(df):
    summary = df.groupby('departamento').size().reset_index(name='Cantidad')
    return summary

# Función para crear los gráficos (pastel y barra) con colores pastel suaves
def create_graphs(df, column_name, title, chart_type='pie'):
    # Usamos la paleta de colores suaves Set2 (una paleta cualitativa)
    color_palette = px.colors.qualitative.Set2  # Usamos Set2, que tiene colores suaves y agradables
    
    if chart_type == 'pie':
        fig = px.pie(df, names=column_name, values="Cantidad", title=f'{title} (Pastel)', color_discrete_sequence=color_palette)
    else:
        fig = px.bar(df, x=column_name, y="Cantidad", title=f'{title} (Barra)', color_discrete_sequence=color_palette)
    return fig

# Botón para leer los datos y procesar
if st.button("Analizar datos de Google Sheet"):
    df = read_sheet()
    st.header("Datos de Sheet1")
    st.dataframe(df)

    # Crear tablas de resumen
    city_summary = create_city_summary(df)
    cargo_summary = create_cargo_summary(df)
    department_summary = create_department_summary(df)

    # Crear gráficos y asignar el tipo de gráfico correspondiente
    city_pie = create_graphs(city_summary, "ciudad", "Resumen por Ciudad", chart_type='pie')
    cargo_bar = create_graphs(cargo_summary, "cargo", "Resumen por Cargo", chart_type='bar')
    department_pie = create_graphs(department_summary, "departamento", "Resumen por Departamento", chart_type='pie')

    # Mostrar gráficos
    st.header("Resumen por Ciudad")
    st.write(city_summary)
    st.plotly_chart(city_pie)

    st.header("Resumen por Cargo")
    st.write(cargo_summary)
    st.plotly_chart(cargo_bar)

    st.header("Resumen por Departamento")
    st.write(department_summary)
    st.plotly_chart(department_pie)

    # Crear los datos para cargar en Sheet2 en el formato requerido
    sheet2_data = [
        ["Resumen por Ciudad"],  # Título para la tabla por ciudad
        ["ciudad", "Cantidad"],  # Encabezados
        *city_summary.values.tolist(),  # Datos de la tabla
        ["Resumen por Cargo"],  # Título para la tabla por cargo
        ["cargo", "Cantidad"],  # Encabezados
        *cargo_summary.values.tolist(),  # Datos de la tabla
        ["Resumen por Departamento"],  # Título para la tabla por departamento
        ["departamento", "Cantidad"],  # Encabezados
        *department_summary.values.tolist()  # Datos de la tabla
    ]

    # Actualizar la hoja de cálculo con los resúmenes
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE2,
        valueInputOption="USER_ENTERED", body={'values': sheet2_data}).execute()

    st.success(f"Hoja actualizada. {result.get('updatedCells')} celdas actualizadas.")
    st.dataframe(sheet2_data)
