import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos (ajusta la ruta según tu archivo)
df = pd.read_csv("dataset_clean/Indicadores del desarrollo humano.csv")

# Título del dashboard
st.title("Análisis de inversión en el sector del Gaming")

# Sección: Introducción
st.header("Introducción")
st.write("Este dashboard muestra un análisis exploratorio de datos del sector gaming, incluyendo valores atípicos, tendencias y correlaciones.")

# Sección: Valores atípicos
st.header("Análisis de Valores Atípicos")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Histograma")
    fig, ax = plt.subplots()
    # Cambia 'ventas' por tu columna
    sns.histplot(df['ventas'], bins=20, kde=True)
    plt.xlabel("Ventas")
    st.pyplot(fig)
with col2:
    st.subheader("Boxplot")
    fig, ax = plt.subplots()
    sns.boxplot(y=df['ventas'])  # Cambia 'ventas' por tu columna
    plt.ylabel("Ventas")
    st.pyplot(fig)

# Sección: Tendencias
st.header("Tendencias")
fig, ax = plt.subplots()
# Cambia 'año' y 'ventas' por tus columnas
sns.lineplot(x='año', y='ventas', data=df)
plt.xlabel("Año")
plt.ylabel("Ventas")
st.pyplot(fig)

# Sección: Correlación
st.header("Matriz de Correlación")
columns_to_use = ['ventas', 'jugadores_activos',
                  'ingresos']  # Ajusta tus columnas
corr_matrix = df[columns_to_use].corr()
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
