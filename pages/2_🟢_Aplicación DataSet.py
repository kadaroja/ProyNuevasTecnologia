import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.subheader("Análisis y Filtrado de Datos")

df = pd.read_csv('./static/datasets/ventas.csv')


tad_descripcion, tab_Análisis_Exploratorio, tab_Filtrado_Básico, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Análisis Exploratorio", "Filtrado Básico", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''
    ## Plantilla Básica para Proyecto Integrador

    ### Introducción

    -   ¿Qué es el proyecto?
    -   ¿Cuál es el objetivo principal?
    -   ¿Por qué es importante?

    ### Desarrollo

    -   Explicación detallada del proyecto
    -   Procedimiento utilizado
    -   Resultados obtenidos

    ### Conclusión

    -   Resumen de los resultados
    -   Logros alcanzados
    -   Dificultades encontradas
    -   Aportes personales
    ''')    

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio:    
    st.title("Análisis Exploratorio")
    st.markdown("""
    * Muestra las primeras 5 filas del DataFrame.  **(df.head())**
    * Muestra la cantidad de filas y columnas del DataFrame.  **(df.shape)**
    * Muestra los tipos de datos de cada columna.  **(df.dtypes)**
    * Identifica y muestra las columnas con valores nulos. **(df.isnull().sum())**
    * Muestra un resumen estadístico de las columnas numéricas.  **(df.describe())**
    * Muestra una tabla con la frecuencia de valores únicos para una columna categórica seleccionada. **(df['columna_categorica'].value_counts())** 
    * Otra información importante           
    """)   
    
#----------------------------------------------------------
#Analítica 2
#----------------------------------------------------------
with tab_Filtrado_Básico:
        st.title("Filtro Básico")
        st.markdown("""
        * Permite filtrar datos usando condiciones simples. **(df[df['columna'] == 'valor'])**
        * Permite seleccionar una columna y un valor para el filtro. **(st.selectbox, st.text_input)**
        * Permite elegir un operador de comparación (igual, diferente, mayor que, menor que). **(st.radio)**
        * Muestra los datos filtrados en una tabla. **(st.dataframe)** 
        """)

#----------------------------------------------------------
#Analítica 3
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)



    




