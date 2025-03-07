import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos
df_1 = pd.read_csv("dataset_clean/Indicadores del desarrollo humano.csv")

# Mostrar las columnas del dataset para diagnóstico
st.write("Columnas disponibles en el dataset:", df_1.columns.tolist())

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
    if df_subset.empty:
        st.warning("No hay datos disponibles para las columnas seleccionadas.")
    else:
        # Obtener el valor de la última fila
        last_values = df_subset.iloc[-1]

        # Crear DataFrame para el gráfico de barras
        df_last = pd.DataFrame({
            'Región': regions,
            selected_variable: last_values.values
        })

        # Graficar barras
        st.header(f"{selected_variable} - Último Año")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=df_last, x='Región',
                    y=selected_variable, palette='coolwarm')
        ax.set_title(f"{selected_variable} (Último Año Disponible)")
        ax.set_ylabel(selected_variable)
        ax.set_xlabel('Región')
        plt.tight_layout()
        st.pyplot(fig)

        # Mostrar el año (buscando una columna que represente años)
        year_col = None
        for col in df_1.columns:
            if 'año' in col.lower() or 'year' in col.lower():
                year_col = col
                break
        if year_col:
            last_year = df_1[year_col].iloc[-1]
            st.write(f"Datos correspondientes al año: {last_year}")
        else:
            st.warning("No se encontró una columna de años en el dataset.")

# Sección: Tendencias (2000-2018)
st.header("Tendencias (2000-2018)")
if year_col is None:
    st.error("No se encontró una columna de años en el dataset. Por favor, revisa las columnas disponibles.")
else:
    # Filtrar datos para los años 2000-2018
    df_trend = df_1[(df_1[year_col] >= 2000) & (df_1[year_col] <= 2018)].copy()

    # Verificar si las columnas existen y hay datos
    if missing_cols:
        st.error(
            f"No se puede generar la tendencia debido a columnas faltantes: {missing_cols}")
    elif df_trend.empty:
        st.warning("No hay datos disponibles para los años 2000-2018.")
    else:
        # Preparar datos para la gráfica de tendencias
        df_trend = df_trend[[year_col] +
                            columns_to_use].replace('..', pd.NA).dropna()

        # Convertir a formato largo para seaborn
        df_trend_long = df_trend.melt(id_vars=[year_col], value_vars=columns_to_use,
                                      var_name='Región', value_name=selected_variable)
        df_trend_long['Región'] = df_trend_long['Región'].str.replace(
            f"{selected_variable}_", "")

        # Graficar tendencias
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df_trend_long, x=year_col,
                     y=selected_variable, hue='Región', palette='coolwarm')
        ax.set_title(f"Tendencia de {selected_variable} (2000-2018)")
        ax.set_xlabel("Año")
        ax.set_ylabel(selected_variable)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

# Sección: Correlación
st.header("Matriz de Correlación")
if not missing_cols:
    corr_matrix = df_1[columns_to_use].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    plt.tight_layout()
    st.pyplot(fig)

# Conclusiones
st.header("Conclusiones")
st.write("""
- Se identificaron valores atípicos en las ventas que podrían indicar éxitos inesperados.
- Las tendencias muestran un crecimiento sostenido en los últimos años.
- Existe una correlación positiva fuerte entre jugadores activos e ingresos.
""")
