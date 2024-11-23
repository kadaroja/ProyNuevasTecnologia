import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

st.markdown("""Este código lee datos de una hoja de cálculo de Google llamada "Sheet1", donde tenemos una data de diferentes personas, con los procesa con Pandas y actualiza una segunda hoja llamada "Sheet2" con una tabla dinámica que consolida la cantidad de registros de `primer_nombre`.""") 

# Definir los permisos para acceder a Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Obtener el ID de la hoja de cálculo desde la interfaz de Streamlit
SPREADSHEET_ID = st.text_input("ID de la hoja de cálculo")
RANGE1 = "Sheet1!A:G"  # Rango con las columnas necesarias
RANGE2 = "Sheet2!A:B"  # Rango de la hoja de destino

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

# Función para crear una tabla que agrupe por `primer_nombre` y cuente la cantidad
def create_summary_table(df):
    # Agrupar por `primer_nombre` y contar las ocurrencias
    summary = df.groupby('primer_nombre').size().reset_index(name='Cantidad')
    return summary

# Botón para leer los datos y procesar la tabla resumen
if st.button("Analizar datos de Google Sheet"):
    df = read_sheet()
    st.header("Datos de Sheet1")
    st.dataframe(df)

    # Crear la tabla de resumen
    summary_df = create_summary_table(df)
    
    # Mostrar la tabla de resumen
    st.header("Tabla de Sumatoria por Primer Nombre")
    st.dataframe(summary_df)
    
    # Actualizar la hoja de cálculo con la tabla de sumatoria
    result = update_sheet(summary_df)
    st.success(f"Hoja actualizada. {result.get('updatedCells')} celdas actualizadas.")
    st.dataframe(summary_df)
