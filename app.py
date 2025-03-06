import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos (ajusta la ruta según tu archivo)
df_1 = pd.read_csv(
    "dataset_clean/Indicadores del desarrollo humano.csv")

# Título del dashboard
st.title("Análisis de inversión en el sector del Gaming")

# Sección: Introducción
st.header("Introducción")
st.write("Este dashboard muestra un análisis exploratorio de datos del sector gaming, incluyendo valores atípicos, tendencias y correlaciones.")

# Lista de variables base (sin sufijo de región)
variables = [
    'INB per cápita, PPA (a $ internacionales actuales)',
    'Tasa de fertilidad, total (nacimientos por cada mujer)',
    'Área selvática  (kilómetros cuadrados)',
    'Crecimiento del PIB (% anual)',
    'Tiempo necesario para iniciar un negocio (días)',
    'Crédito interno proporcionado por el sector financiero (% del PIB)',
    'Recaudación impositiva (% del PIB)',
    'Migración neta',
    'Inversión extranjera directa, entrada neta de capital (balanza de pagos, US$ a precios actuales)',
    'Desempleo, total (% de la población activa total) (estimación modelado OIT)',
    'Población entre 0 y 14 años de edad, total'
]

# Regiones
regions = ['USA', 'EU', 'JPN', 'WLD']

# Título del dashboard
st.title("Comparación de Variables por Región (Último Año)")

# Dropdown para seleccionar la variable
selected_variable = st.selectbox("Selecciona una variable:", variables)

# Construir las columnas correspondientes a cada región
columns_to_use = [f"{selected_variable}_{region}" for region in regions]

# Verificar si las columnas existen en el DataFrame
missing_cols = [col for col in columns_to_use if col not in df_1.columns]
if missing_cols:
    st.error(
        f"Las siguientes columnas no están en el DataFrame: {missing_cols}")
else:
    # Seleccionar y limpiar datos
    df_subset = df_1[columns_to_use].replace('..', pd.NA).dropna()

    # Obtener el valor de la última fila
    last_values = df_subset.iloc[-1]

    # Crear DataFrame para el gráfico
    df_last = pd.DataFrame({
        'Región': regions,
        selected_variable: last_values.values
    })

    # Graficar barras (sin invertir el eje Y)
    st.header(f"{selected_variable} - Último Año")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=df_last, x='Región',
                y=selected_variable, palette='coolwarm')

    ax.set_title(f"{selected_variable} (Último Año Disponible)")
    ax.set_ylabel(selected_variable)
    ax.set_xlabel('Región')

    # Mostrar el año del índice si está disponible
    last_year = df_subset.index[-1]
    st.write(f"Datos correspondientes al año: {last_year}")

    st.pyplot(fig)


# Sección: Tendencias
st.header("Tendencias")
fig, ax = plt.subplots()
# Cambia 'año' y 'ventas' por tus columnas
sns.lineplot(x='año', y='ventas', data=df_1)
plt.xlabel("Año")
plt.ylabel("Ventas")
st.pyplot(fig)

# Sección: Correlación
st.header("Matriz de Correlación")
columns_to_use = ['ventas', 'jugadores_activos',
                  'ingresos']  # Ajusta tus columnas
corr_matrix = df_1[columns_to_use].corr()
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Conclusiones
st.header("Conclusiones")
st.write("""
- Se identificaron valores atípicos en las ventas que podrían indicar éxitos inesperados.
- Las tendencias muestran un crecimiento sostenido en los últimos años.
- Existe una correlación positiva fuerte entre jugadores activos e ingresos.
""")
