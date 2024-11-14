import random
from faker import Faker
import streamlit as st 
import pandas as pd  
import firebase_admin  
from datetime import datetime, date, timedelta
from firebase_admin import credentials, firestore  
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.subheader("💻Control de Asistencia de Empleados")

# Verificar si ya existe una instancia de la aplicación
if not firebase_admin._apps:  
    # Cargar las credenciales de Firebase desde los secretos de Streamlit
    firebase_credentials = st.secrets["FIREBASE_CREDENTIALS"]  
    # Convertir las credenciales a un diccionario Python
    secrets_dict = firebase_credentials.to_dict()  
    # Crear un objeto de credenciales usando el diccionario 
    cred = credentials.Certificate(secrets_dict)  
    # Inicializar la aplicación de Firebase con las credenciales
    app = firebase_admin.initialize_app(cred)

# Obtener el cliente de Firestore
db = firestore.client()


tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''

    ### 📊 Nuestro Proyecto
    Consiste en el desarrollo de un panel de control digital diseñado específicamente para la gestión de la asistencia de empleados en una empresa.
    ### 🎯 Objetivo principal
    Es desarrollar un panel de control que permita al Administrador gestionar y monitorear la asistencia de los empleados de manera eficiente. Esto incluye el registro de entradas y salidas, la gestión de ausencias y tardanzas.
    ### 🚀 Su Importancia
    La implementación de este panel de control es crucial para las empresas por varias razones:

    - Eficiencia: Reduce el tiempo y el esfuerzo que el Administrador dedica a gestionar manualmente la asistencia, lo que permite enfocarse en tareas más estratégicas.
    - Precisión: Disminuye la probabilidad de errores en el cálculo de horas trabajadas y la generación de reportes, asegurando que la información sea más confiable.
    - Centralización: Al contar con un sistema único para la gestión de asistencia, se facilita el acceso a datos históricos y se mejora la toma de decisiones basadas en información precisa.
    - Transparencia: Permite a la empresa mantener un registro claro de la asistencia, lo que puede ser útil para auditorías y análisis de desempeño.
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
#Generador de datos
#----------------------------------------------------------
with tab_Generador:
    st.write('Esta función Python genera datos ficticios de Empleados y Asistencia y los carga en una base de datos Firestore, proporcionando una interfaz sencilla para controlar la cantidad de datos generados y visualizar los resultados.')
    # Inicializar Faker para Colombia
    fake = Faker('es_CO')

    departamentos = ["Administración", "Talento Humano", "Ventas", "Ti", "Servicio al cliente", "Legal", "Operaciones"]
    cargos = ["Gerente", "Auxiliar", "Analista", "Contador", "Supervisor", "Desarrollador", "Abogado"]
    novedades = ["Incapacidad", "Asiste", "Permiso Remunerado", "Ausencia Injustificada", "Vacaciones"]
    ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Cúcuta", "Bucaramanga"]

    def generate_fake_employees(n):
        employees = []
        for _ in range(n):
            fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=65)
            fecha_contratacion = fake.date_time_between(start_date='-5y', end_date='now')
            employee = {
                'tipo_documento_identidad': random.choice(["Tarjeta de Identidad", "Cédula de Ciudadanía", "Pasaporte"]),
                'numero_documento_identidad': fake.random_int(min=1000000, max=999999999),
                'primer_nombre': fake.first_name(),
                'primer_apellido': fake.last_name(),
                'fecha_nacimiento': datetime.combine(fecha_nacimiento, datetime.min.time()), 
                'edad': (datetime.now().date() - fecha_nacimiento).days // 365,
                'correo': fake.email(),
                'ciudad': random.choice(ciudades),
                'cargo': random.choice(cargos),
                'departamento': random.choice(departamentos),
                'telefono': fake.phone_number(),
                'estado_empleado': random.choice(["Activo", "Inactivo"]),
                'fecha_contratacion': fecha_contratacion, 
            }
            employees.append(employee)
        return employees

    def generate_fake_attendance(employees, n):
        attendance = []
        for _ in range(n):
            employee = random.choice(employees)
            fecha_entrada = fake.date_time_between(start_date=employee['fecha_contratacion'], end_date='now')
            fecha_salida = fecha_entrada + timedelta(hours=random.randint(6, 10))
            record = {
                'fecha_entrada': fecha_entrada,
                'fecha_salida': fecha_salida,
                'novedades_asistencia': random.choice(novedades),
                'numero_documento_identidad': employee['numero_documento_identidad']
            }
            attendance.append(record)
        return attendance
    
    def add_data_to_firestore(collection, data):
        for item in data:
            db.collection(collection).add(item)

    col1, col2 = st.columns(2)

    def delete_collection(collection_name):
        docs = db.collection(collection_name).get()
        for doc in docs:
            doc.reference.delete()

    with col1:
        st.subheader('Empleados')
        num_employees = st.number_input('Número de empleados a generar', min_value=1, max_value=300, value=10)
        if st.button('Generar y Añadir Empleados'):
            with st.spinner('Generando y añadiendo nuevos empleados...'):
                employees = generate_fake_employees(num_employees)
                add_data_to_firestore('empleados', employees)
            st.success(f'{num_employees} empleados añadidos a Firestore')
            st.dataframe(pd.DataFrame(employees))
            st.session_state.employees = employees

    # Botón para borrar empleados
        if st.button('Borrar Empleados'):
            with st.spinner('Borrando empleados...'):
                delete_collection('empleados') # type: ignore
            st.success('Todos los empleados eliminados de Firestore')

    with col2:
        st.subheader('Asistencia')
        num_attendance = st.number_input('Número de registros de asistencia a generar', min_value=1, max_value=1000, value=40)
        if st.button('Generar y Añadir Asistencia'):
            if 'employees' not in st.session_state or not st.session_state.employees:
                st.error('Por favor, genere empleados primero.')
            else:
                with st.spinner('Generando y añadiendo nuevos registros de asistencia...'):
                    attendance = generate_fake_attendance(st.session_state.employees, num_attendance)
                    add_data_to_firestore('asistencia', attendance)
                st.success(f'{num_attendance} registros de asistencia añadidos a Firestore')
                st.dataframe(pd.DataFrame(attendance))

        if st.button('Borrar Asistencia'):
            with st.spinner('Borrando registros de asistencia...'):
                delete_collection('asistencia')
            st.success('Todos los registros de asistencia eliminados de Firestore')

    def delete_collection(collection_name):
        docs = db.collection(collection_name).get()
        for doc in docs:
            doc.reference.delete()
#----------------------------------------------------------
#Datos
#----------------------------------------------------------
with tab_datos:
    st.write('Esta función muestra datos de Empleados y Registros almacenados en una base de datos Firestore, permitiendo una visualización organizada y fácil acceso a la información.')
    tab_employees, tab_attendance = st.tabs(["Empleados", "Asistencias"])
    with tab_employees:        
        # Obtener datos de una colección de Firestore
        employees = db.collection('empleados').stream()
        # Convertir datos a una lista de diccionarios
        employees_data = [doc.to_dict() for doc in employees]
        # Crear DataFrame
        df_employees = pd.DataFrame(employees_data)
        # Reordenar las columnas
        column_order = ['tipo_documento_identidad','numero_documento_identidad','primer_nombre', 'primer_apellido', 'fecha_nacimiento','edad','ciudad','correo','telefono','fecha_contratacion','cargo', 'departamento']
        df_employees = df_employees.reindex(columns=column_order)   
        
        st.dataframe(df_employees)
    with tab_attendance:       
        # Obtener datos de una colección de Firestore
        attendance = db.collection('asistencia').stream()
        # Convertir datos a una lista de diccionarios
        attendance_data = [doc.to_dict() for doc in attendance]
        # Crear DataFrame
        df_attendance = pd.DataFrame(attendance_data)
         # Reordenar las columnas
        column_order = ['numero_documento_identidad', 'fecha_entrada', 'fecha_salida', 'novedades_asistencia']
        df_attendance = df_attendance.reindex(columns=column_order)
        
        st.dataframe(df_attendance)

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio:    
    st.title("😎Análisis Exploratorio")

    # Obtener datos de empleados
    employees = db.collection('empleados').stream()
    employees_data = [doc.to_dict() for doc in employees]
    df_employees = pd.DataFrame(employees_data)

    # Obtener datos de asistencia
    attendance = db.collection('asistencia').stream()
    attendance_data = [doc.to_dict() for doc in attendance]
    df_attendance = pd.DataFrame(attendance_data)

    # Seleccionar el DataFrame a analizar
    df_to_analyze = st.selectbox("Seleccione el conjunto de datos a analizar:", ["Empleados", "Asistencia"])
    
    if df_to_analyze == "Empleados":
        df = df_employees
    else:
        df = df_attendance
    
    st.subheader("Primeras 5 filas del DataFrame")
    st.dataframe(df.head())

    # Mostrar la cantidad de filas y columnas
    st.subheader("Cantidad de filas y columnas")
    st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

    # Mostrar los tipos de datos de cada columna
    st.subheader("Tipos de datos de cada columna")
    st.write(df.dtypes)

    # Identificar y mostrar las columnas con valores nulos
    st.subheader("Columnas con valores nulos")
    st.write(df.isnull().sum())

    # Mostrar frecuencia de valores únicos para una columna categórica seleccionada
    st.subheader("Conteo de datos por columnas")
    categorical_columns = df.select_dtypes(include=['object']).columns
    selected_column = st.selectbox("Seleccione una columna categórica", categorical_columns)
    st.write(df[selected_column].value_counts())

    # Otra información importante
    st.subheader("Otra información importante")
   
    if df_to_analyze == "Empleados":
    # Distribución de edades con colores personalizados
        fig_age = px.histogram(
            df,
            x='edad',
            nbins=20,
            title='Distribución de edades de los empleados',
            color_discrete_sequence=['#FF69B4']  # Cambia este código hexadecimal por el color que desees
        )
        st.plotly_chart(fig_age)

        # Distribución por departamento
        fig_dept = px.pie(df, names='departamento', title='Distribución de empleados por departamento')
        st.plotly_chart(fig_dept)
    else:
        # Distribución de novedades de asistencia
        fig_novedades = px.pie(df, names='novedades_asistencia', title='Distribución de novedades de asistencia')
        st.plotly_chart(fig_novedades)

        # Histograma de fechas de entrada
        df['fecha_entrada'] = pd.to_datetime(df['fecha_entrada'])
        fig_entrada = px.histogram(df, x='fecha_entrada', title='Distribución de fechas de entrada')
        st.plotly_chart(fig_entrada)
#----------------------------------------------------------

#Analítica 2
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
   
    # Filtrar el DataFrame (ejemplo simple)
        dept_filter = st.multiselect("Seleccione el departamento", df_employees['departamento'].unique())
        if dept_filter:
            filtered_df = df_employees[df_employees['departamento'].isin(dept_filter)]
        else:
            filtered_df = df_employees  # Mostrar todos si no hay filtro

        st.write("Datos filtrados:", filtered_df)

    # Visualización dinámica con gráficos en Seaborn
        st.subheader("Gráficos de Distribución")

        col1, col2 = st.columns(2)

        # Configuramos una paleta de colores pastel
        pastel_palette = sns.color_palette("pastel")

        with col1:
            st.write("Distribución de Edades")
            fig, ax = plt.subplots()
            sns.histplot(filtered_df['edad'], kde=True, ax=ax, color=pastel_palette[2])  # Color pastel específico
            st.pyplot(fig)

        with col2:
            st.write("Distribución de Empleados por Departamento")
            fig, ax = plt.subplots()
            sns.countplot(data=filtered_df, x='departamento', palette=pastel_palette, ax=ax)  # Paleta de tonos pastel
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)

        # Gráfico de Distribución de Edades por Ciudad (Box plot)
        with col1:
            st.write("Distribución de Edades por Ciudad (Box plot)")
            fig, ax = plt.subplots()
            sns.boxplot(data=filtered_df, x='ciudad', y='edad', palette=pastel_palette, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)

        # Gráfico de Distribución de Edades por Cargo (Violin plot)
        with col2:
            st.write("Distribución de Edades por Cargo (Violin plot)")
            fig, ax = plt.subplots()
            sns.violinplot(data=filtered_df, x='cargo', y='edad', palette=pastel_palette, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)

