import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.subheader("🧑‍🎓Matriculas a Educación Superior en Colombia")

# Usamos `on_bad_lines='skip'` en lugar de `error_bad_lines=False`
df = pd.read_csv(
    'static/datasets/ESTADISTICAS_DE_MATRICULA_POR_DEPARTAMENTOS.csv', 
    encoding='latin-1', 
    on_bad_lines='skip',
    sep=';'
)


tad_descripcion, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Análisis Exploratorio", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''

    ### Qué es el proyecto?
    El proyecto consiste en el desarrollo de una herramienta de gestión de asistencia de empleados mediante la generación y análisis de datos. Utiliza tecnología de visualización 
        interactiva en Streamlit para representar patrones de asistencia y facilita la toma de decisiones informadas.        
    ### Cuál es el objetivo principal?
    El objetivo principal es optimizar la supervisión y análisis de asistencia de empleados, proporcionando visualizaciones de datos que permitan identificar patrones, 
    reducir ausentismo y mejorar la eficiencia en la gestión de personal.
    ### Por qué es importante?
    Este proyecto es importante porque permite a las organizaciones contar con una herramienta visual e interactiva para gestionar la asistencia, lo que facilita la detección temprana
    de problemas y la implementación de medidas correctivas, mejorando la productividad y el ambiente laboral.
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

        # Muestra las primeras 5 filas del DataFrame
    st.subheader("Primeras 5 filas")
    st.write(df.head())
    
    # Muestra la cantidad de filas y columnas
    st.subheader("Cantidad de filas y columnas")
    st.write(df.shape)
    
    # Muestra los tipos de datos de cada columna
    st.subheader("Tipos de datos de cada columna")
    st.write(df.dtypes)
    
    # Muestra las columnas con valores nulos
    st.subheader("Columnas con valores nulos")
    st.write(df.isnull().sum())
    
    # Muestra un resumen estadístico
    st.subheader("Resumen estadístico")
    st.write(df.describe())
    
    # Muestra la frecuencia de valores únicos de una columna categórica
    # Asegúrate de reemplazar 'columna_categorica' con una columna real de tu DataFrame
    st.subheader("Frecuencia de valores de columna categórica")
    if 'Nombre del Departamento' in df.columns:
        st.write(df['Nombre del Departamento'].value_counts())
    else:
        st.write("La columna 'Nombre del Departamento' no existe en el DataFrame.")
    
    # Otra información importante (puedes agregar más análisis aquí según lo necesites)
    st.subheader("Otra información importante")
    st.write("Puedes agregar más visualizaciones o análisis aquí.")  
    
#----------------------------------------------------------

#Analítica 2
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)



    




