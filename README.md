# Analisis de inversión en el sector del gaming

Este repositorio contiene un análisis macro y micro del sector del sector del gaming. Se considera las principales regiones del mundo en cuanto a crecimiento del PIB, recaudación impositiva, crecimiento de natalidad, entre otros. Además, también se consideran tendencias en las consolas, plataformas, y géneros de videojuegos. Esto permitirá al inversor tener un conocimiento más profundo a la hora de desarrollar nuevos productos. En resumen, los objetivos del presente trabajo son:
* Analizar el mercado de videojuegos.
* Identificar posibles nichos para desarrollar nuevos productos.
* Encontrar los insights y presentarlos.

## Descripción
Se desarrollan dos fases para el proyecto:

- `Análisis exploratorio de los datos en Python.`
- `Tablero de control para toma de decisiones en Power BI.`


#### Análisis exploratorio de los datos

Primero se realizan diversas transformaciones como ser:

- `Selección de las columnas a analizar`.
- `Formateo de las columnas`.

Y luego se realiza el análisis exploratorio o EDA, abordando problemas como:

- `Valores faltantes o nulos.`
- `Datos duplicados`.
- `Valores outliers o anómalos`.
- `Análisis univariado y bivariado.`
- `Análisis de tendencias.`
- `Análisis de segmentos.` 

#### Tablero de control

Los insights provenientes del análisis exploratorio de los datos se vuelcan a dicho dashboard. En pos de ello, se contruyen gráficas y diversos KPIs que hay considerar para la consecuente toma de decisiones. Las hojas utilizadas son: 

- `Macro`
- `Consolas`
- `Steam`
- `Ventas`
- `Conclusiones`

Se adjunta el link en Onedrive:
https://1drv.ms/u/s!AluEGz41YFydmL4-87I5Pghlx-5Ivg?e=tQ52BH

## Instalación

1. Clona este repositorio:
   ```sh
   git clone https://github.com/JosueMonte/gaming
   ```

2. Instala los paquetes requeridos en el archivo llamado:
   ```sh
   requirements.txt
   ```

3. Para visualizar el dashboard será necesario intalar Power BI desktop:
   ```sh
   Microsoft Store: Power BI Desktop
   ```

## Estructura del repositorio

- `eda_1.ipynb`: Se realiza el análisis exploratorio para el análisis macro.
- `eda_2.ipynb`: Se realiza el análisis exploratorio para el análisis de las consolas.
- `eda_3.ipynb`: Se realiza el análisis exploratorio para el análisis de los juegos en Steam.
- `eda_4.ipynb`: Se realiza el análisis exploratorio para el análisis de las ventas.
- `dashboard.pbix`: Confección del tablero de control para la toma de decisiones.
- `/dataset_clean/`: Carpeta donde se alojan los archivos exportados de los eda.

## KPIs del dashboard

- `Ventas de consolas`: Se plantea el objetivo para el próximo año de aumentar un 10 %. 
- `Tiempo medio de juego`: Se plantea el objetivo para el próximo año de aumentar un 10 % el precio de los videojuegos.
- `Ventas por género`: Se plantea un objetivo para el próximo año de aumentar un 10 % las ventas por género.