import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos
df_1 = pd.read_csv("dataset_clean/Indicadores del desarrollo humano.csv")

# Mostrar columnas para diagnóstico (opcional, puedes comentarlo después de verificar)
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
    'Población entre 0 y 14 años de edad, total',
    'Superficie (kilómetros cuadrados)',
    'INB per cápita, método Atlas (US$ a precios actuales)',
    'Población activa, mujeres (% de la población activa total)'
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

        # Mostrar el año
        last_year = df_1['Año'].iloc[-1]
        st.write(f"Datos correspondientes al año: {last_year}")

# Sección: Tendencias (2000-2018)
st.header("Tendencias (2000-2018)")
# Filtrar datos para los años 2000-2018
df_trend = df_1[(df_1['Año'] >= 2000) & (df_1['Año'] <= 2018)].copy()

# Verificar si las columnas existen y hay datos
if missing_cols:
    st.error(
        f"No se puede generar la tendencia debido a columnas faltantes: {missing_cols}")
elif df_trend.empty:
    st.warning("No hay datos disponibles para los años 2000-2018.")
else:
    # Preparar datos para la gráfica de tendencias
    df_trend = df_trend[['Año'] + columns_to_use].replace('..', pd.NA).dropna()

    # Convertir a formato largo para seaborn
    df_trend_long = df_trend.melt(id_vars=['Año'], value_vars=columns_to_use,
                                  var_name='Región', value_name=selected_variable)
    df_trend_long['Región'] = df_trend_long['Región'].str.replace(
        f"{selected_variable}_", "")

    # Graficar tendencias
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df_trend_long, x='Año', y=selected_variable,
                 hue='Región', palette='coolwarm')
    ax.set_title(f"Tendencia de {selected_variable} (2000-2018)")
    ax.set_xlabel("Año")
    ax.set_ylabel(selected_variable)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Sección: Correlación (primera matriz)
st.header("Matriz de Correlación (Regiones)")
if not missing_cols:
    corr_matrix = df_1[columns_to_use].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlación entre regiones")
    plt.tight_layout()
    st.pyplot(fig)

# Nueva sección: Correlación específica para USA
st.header("Matriz de Correlación (Variables seleccionadas - USA)")
usa_selected_cols = [
    'INB per cápita, PPA (a $ internacionales actuales)_USA',
    'Crecimiento del PIB (% anual)_USA',
    'Tiempo necesario para iniciar un negocio (días)_USA',
    'Crédito interno proporcionado por el sector financiero (% del PIB)_USA',
    'Recaudación impositiva (% del PIB)_USA',
    'Inversión extranjera directa, entrada neta de capital (balanza de pagos, US$ a precios actuales)_USA',
    'Población entre 0 y 14 años de edad, total_USA'
]

# Verificar si las columnas existen en el DataFrame
usa_missing_cols = [
    col for col in usa_selected_cols if col not in df_1.columns]
if usa_missing_cols:
    st.error(
        f"Las siguientes columnas no están en el DataFrame: {usa_missing_cols}")
else:
    # Calcular la matriz de correlación para las columnas seleccionadas
    usa_corr_matrix = df_1[usa_selected_cols].corr()

    # Simplificar nombres de las columnas para las etiquetas
    short_labels = [
        'INB per cápita (PPA)',
        'Crecimiento del PIB (% anual)',
        'Tiempo iniciar negocio (días)',
        'Crédito interno (% PIB)',
        'Recaudación impositiva (% PIB)',
        'Inversión extranjera (US$)',
        'Población 0-14 años'
    ]

    # Graficar la matriz de correlación
    fig, ax = plt.subplots(figsize=(12, 10))  # Aumentar el tamaño del gráfico
    sns.heatmap(usa_corr_matrix, annot=True, cmap='coolwarm', ax=ax, fmt='.2f',
                xticklabels=short_labels, yticklabels=short_labels,  # Usar etiquetas cortas
                # Tamaño de los números dentro del heatmap
                annot_kws={"size": 10},
                cbar_kws={'label': 'Correlación'})  # Etiqueta para la barra de color

    ax.set_title("Correlación de variables seleccionadas (USA)",
                 fontsize=14, pad=20)
    # Rotar etiquetas del eje X
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)  # Tamaño de las etiquetas del eje Y
    plt.tight_layout(pad=3.0)  # Ajustar márgenes para evitar cortes
    st.pyplot(fig)

# Conclusiones
st.header("Conclusiones")
st.write("""
1. La tasa de fertilidad está en rangos muy malos, y es necesario incrementarla en todas las regiones, y mantenerla en WLD.
2. Japón no es una región recomendable para invertir: 
   1. No crecerá en superficie ni en población:
      1. No tiene casi área selvática.
      2. La población continuará avejentándose.
      3. Probablemente necesite aumentar la recaudación impositiva para ayudar a los más ancianos.
   2. Tiene un stock de deuda muy alto, por lo cual:
      1. Necesitará aumentar la recaudación impositiva, impactando negativamente en las inversiones.
      2. No puede pedir más deuda para crecer.
3. La Unión Europea está en mejores condiciones que Japón, pero de a poco se está acercando a sus prácticas negativas, es decir, se está japonizando. Por lo cual, es una región mejor que Japón pero tampoco sería un país recomendable para invertir.
4. Estados Unidos es una región aceptable para invertir al presente:
   1. Continúa siendo un pais atractivo para migraciones, es la más elevada entre los 4.
   2. Tiene mucha área selvática para recibir migraciones.
   3. Tiene tanta población entre 0 y 14 como toda la Unión Europea.
   4. Es quien recibe más inversión extranjera.
   5. La recaudación como porcentaje del PIB es la menor.
   6. El tiempo en dias para iniciar un negocio es de solo 5 días.
5. Señales de alarma para Estados Unidos:
   1. Si bien aumentó su stock de deuda, está muy lejos de Japón por ejemplo.
   2. Su tasa de fertilidad ha ido retrocediendo significativamente en los últimos años y está por debajo de 2, dependiendo de las migraciones para aumentar su población y generar empleo.
6. El resto del mundo es una región aceptable para invertir, quizás, pensando más en el futuro:
   1. Cuenta con la tasa de fertilidad más elevada y con mucha población activa.
   2. Cuenta con mucha área selvática para aumentar zonas para vivir.
   3. Recibe también bastante inversión extranjera.
   4. La recaudación es superior a Estados Unidos pero va por detrás.
   5. El tiempo en dias para iniciar un negocio no es poco aún, pero continua disminuyendo.
   6. No tiene las señales de alarma que tiene Estados Unidos.
7. El resto del mundo presenta el problema de que cuenta con paises de Asia (excepto Japón), Africa, Oceania, y América Latina, y el resto de Europa que no está dentro de la Unión Europea. Y lo peor de ello, es que China e India son los más importantes por lejos respecto a los otros, es decir, no es un región que nos ayude a identificar para invertir.
8. Finalmente, el pais más recomendable en este primer análisis es USA, y WLD es una buena opción pero hay que hacer un análisis dentro de este, o separar mejor las regiones, quizas: China, India, Resto de paises desarrollados, América Latina, Africa, y resto.
""")
