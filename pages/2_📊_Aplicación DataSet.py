import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

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

    ### El proyecto
    El proyecto consiste en el desarrollo de una herramienta de gestión de asistencia de empleados mediante la generación y análisis de datos. Utiliza tecnología de visualización 
        interactiva en Streamlit para representar patrones de asistencia y facilita la toma de decisiones informadas.        
    ### Objetivo principal
    El objetivo principal es optimizar la supervisión y análisis de asistencia de empleados, proporcionando visualizaciones de datos que permitan identificar patrones, 
    reducir ausentismo y mejorar la eficiencia en la gestión de personal.
    ### Su importancia
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
    
    # Resumen de conteo por año
    if 'Ano' in df.columns:
        st.subheader("Conteo de registros por Año")
        conteo_por_ano = df['Ano'].value_counts().sort_index()  # Cuenta los registros por año
        st.write(conteo_por_ano)  
    
#----------------------------------------------------------

#Analítica 2
#----------------------------------------------------------
with st.container():
    st.title("Filtro Final Dinámico")
    st.markdown("""
    * Muestra un resumen dinámico del DataFrame filtrado. 
    * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
    * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
    """)
    
    # Filtros interactivos
    st.sidebar.header("Filtros de Datos")
    
    # Filtro por años (selección múltiple)
    años_filtrados = st.sidebar.multiselect("Selecciona los Años", df['Ano'].unique(), default=df['Ano'].unique())
    
    # Filtro por departamentos (selección múltiple)
    departamentos_filtrados = st.sidebar.multiselect("Selecciona los Departamentos", df['Nombre del Departamento'].unique(), default=df['Nombre del Departamento'].unique())
    
    # Filtro por nivel académico (por ejemplo, 'TECNICA PROFESIONAL')
    nivel_filtrado = st.sidebar.selectbox("Selecciona el Nivel Académico", df.columns[3:8])  # Asumiendo que los niveles académicos están en las columnas 3-7

    # Filtrado del DataFrame
    df_filtrado = df[(df['Ano'].isin(años_filtrados)) & (df['Nombre del Departamento'].isin(departamentos_filtrados))]

    # Mostrar criterios de filtro y DataFrame filtrado
    st.subheader("Criterios de Filtrado Aplicados")
    st.write("Años seleccionados:", años_filtrados)
    st.write("Departamentos seleccionados:", departamentos_filtrados)
    st.write("Nivel académico seleccionado:", nivel_filtrado)
    st.write("Datos Filtrados")
    st.write(df_filtrado)

    # Estadísticas descriptivas
    st.subheader("Estadísticas Descriptivas del DataFrame Filtrado")
    st.write(df_filtrado.describe())

    # Gráficos Dinámicos con Plotly
    st.subheader(f"Distribución del Nivel Académico: {nivel_filtrado}")
    
    # Histograma de los niveles educativos filtrados por año
    if st.checkbox("Mostrar histograma de distribución de nivel académico", value=True):
        fig = px.histogram(df_filtrado, 
                           x='Ano', 
                           y=nivel_filtrado, 
                           histfunc="sum",  # Utiliza la suma para visualizar el total por año
                           color='Ano',  # Colorear por año para hacerlo más visual
                           labels={nivel_filtrado: 'Número de Matrículas'},  # Etiqueta del eje Y
                           title=f"Distribución de {nivel_filtrado} por Año",
                           nbins=15,  # Cantidad de barras en el histograma
                           template="plotly",  # Estilo visual
                           color_discrete_sequence=px.colors.qualitative.Pastel1)  # Usar "Pastel1" en lugar de "pastel"
        st.plotly_chart(fig)
    
    # Gráfico de Histogramas por Departamento y Nivel Académico
    st.subheader(f"Histograma de {nivel_filtrado} por Departamento")
    if st.checkbox("Mostrar histograma por departamento", value=True):
        fig = px.histogram(df_filtrado, 
                           x='Nombre del Departamento', 
                           y=nivel_filtrado, 
                           histfunc="sum", 
                           color='Nombre del Departamento',  # Colorear por departamento
                           labels={nivel_filtrado: 'Número de Matrículas'},  # Etiqueta eje Y
                           title=f"Distribución de {nivel_filtrado} por Departamento",
                           nbins=20,  # Número de barras en el histograma
                           template="plotly",  # Estilo visual
                           color_discrete_sequence=px.colors.qualitative.Pastel1)  # Usar "Pastel1" en lugar de "pastel"
        st.plotly_chart(fig)
