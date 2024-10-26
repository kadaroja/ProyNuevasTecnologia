import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

st.markdown("""
Este código lee datos de una hoja de cálculo de Google Sheets llamada "Sheet1", los procesa con Pandas y actualiza una segunda hoja llamada "Sheet2" con nuevos datos. La interfaz de usuario de Streamlit permite al usuario ingresar el ID de la hoja de cálculo y visualizar los datos procesados.            
    """)   

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = st.text_input("ID  hoja de cálculo")
RANGE1 = "Sheet1!A:E"
RANGE2 = "Sheet2!A:E"

google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]  
secrets_dict = google_sheet_credentials.to_dict()     
creds = None
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def read_sheet():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()      
    values = result.get('values', [])
    df = pd.DataFrame(values)
    return df

def update_sheet(df):
    body = {'values': df.values.tolist()}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE2,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result

# Botón para leer
if st.button("Analizar datos de Google Sheet"):  
    df = read_sheet()
    st.header("Datos hoja1")
    st.dataframe(df)
    df_update = pd.DataFrame({
        'Columna1': ['Nuevo1', 'Nuevo2', 'Nuevo3'],
        'Columna2': [1, 2, 3],
        'Columna3': ['A', 'B', 'C']
    })
    
    # Actualizar la hoja de cálculo
    result = update_sheet(df_update)
    st.header("Datos hoja2")
    st.success(f"Hoja actualizada. {result.get('updatedCells')} celdas actualizadas.")

    # Mostrar el DataFrame actualizado
    st.dataframe(df_update)



