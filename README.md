# Prueba Data Engineering Jr

## Descripción General
# Este proyecto incluye dos componentes principales:
# 1. **Web Scraping**: Extrae información de un sitio web específico (https://www.holidu.es) sobre 
#    propiedades vacacionales en Barcelona, obteniendo el título, ubicación, descripción, precio y puntuación. 
#    Los datos se almacenan en el archivo `propiedades_holidu.csv`.
# 2. **Análisis de Datos (ETL y EDA)**: Se realiza el procesamiento ETL y EDA sobre datos de reservas 
#    (`Bookings.csv`) y propiedades (`Properties.csv`), combinándolos en un archivo limpio (`datos_limpios.csv`), 
#    el cual sirve como base para análisis y visualización.

## Configuración del Entorno
# - **Lenguaje**: Python 3.7
# - **Librerías necesarias**:
#   - `selenium`: Para la automatización del navegador y la extracción de datos.
#   - `pandas`: Para la manipulación de datos.
#   - `matplotlib`: Para visualización de datos.
#   - `seaborn`: Para gráficos estilizados.

# **Instalación de Librerías**:
# pip install selenium pandas matplotlib seaborn

# **GeckoDriver para Firefox**:
# Asegúrate de tener instalado GeckoDriver para Firefox. Descárgalo y colócalo en la ruta 
# `C:\\Users\\jhers\\OneDrive\\Escritorio\\driver\\geckodriver.exe`, o ajusta la ruta en el código si es diferente.

## Instalación

# 1. Clonar el Repositorio:
#    git clone https://github.com/JhersonAragon/PruebaTecnica.git

# 2. Ejecución
# - **Web Scraping**:
#    python web_scraping.py
#    Este script abrirá Firefox, navegará a la página de propiedades y realizará el scraping de los 
#    primeros 100 resultados de propiedades en Barcelona, guardando los datos en `propiedades_holidu.csv`.

# - **ETL y EDA**:
#    python main2.py
#    Este script realiza el procesamiento de datos, uniendo `Bookings.csv` y `Properties.csv` en `datos_limpios.csv` y 
#    muestra visualizaciones y estadísticas de interés.

# 3. Limpieza de Datos
#    Durante el proceso de ETL, los datos se limpiaron y transformaron con las siguientes decisiones:

#    - **Eliminación de duplicados**: Para evitar redundancia y garantizar integridad en el análisis.
#    - **Manejo de valores vacíos**:
#       - Columnas numéricas (`RoomRate`, `Revenue`, `ADR`): Los valores vacíos se reemplazaron por 0 para evitar distorsiones 
#         en los cálculos de medias y otras estadísticas.
#       - Columnas categóricas (`PropertyType`, `Channel`): Los valores vacíos fueron reemplazados por "Desconocido" para 
#         categorizar adecuadamente sin dejar datos nulos.
#    - **Fechas**: Se formatearon como `datetime`, aplicando ajustes para asegurar consistencia y precisión en las 
#       columnas de fechas en el archivo `Bookings.csv`.

## Descripción del Pipeline de ETL
# El pipeline de ETL consta de tres pasos principales:

# - **Extracción**:
#    Los datos se cargan desde `Bookings.csv` y `Properties.csv` a DataFrames de Pandas.
# - **Transformación**:
#    - Ajuste de formatos de fechas en el archivo de reservas (`Bookings.csv`).
#    - Unión de DataFrames de reservas y propiedades usando la columna `PropertyId`.
#    - Aplicación de reglas de limpieza de datos descritas anteriormente.
# - **Carga**:
#    - Los datos resultantes se guardan en `datos_limpios.csv`, que se usará para análisis y visualizaciones.

## Retos y Soluciones
# Durante el desarrollo, surgieron varios retos:

# - **Detección de bots en el scraping**:
#    La página detectaba el scraping a alta velocidad, bloqueando el acceso. Las soluciones implementadas fueron:
#       - Uso de una VPN para evitar bloqueos por IP.
#       - Ajuste de tiempos de espera (`time.sleep`) para que la interacción de scrolling y carga de página 
#         pareciera más natural.
# - **Limpieza y manejo de datos faltantes**:
#       - Columnas numéricas (`RoomRate` y `Revenue`): Los valores vacíos se reemplazaron por 0, para no afectar 
#         los análisis.
#       - Columnas categóricas (`PropertyType` y `Channel`): Se asignó "Desconocido" como valor predeterminado.
# - **Estandarización de fechas**:
#       - Las fechas se formatearon como `datetime` para facilitar comparaciones entre reservas y ocupación.

## Estructura de Archivos
# - `web_scraping.py`: Contiene el código de Selenium para el scraping de propiedades.
# - `main2.py`: Realiza el proceso ETL y análisis de datos.
# - `propiedades_holidu.csv`: Archivo de salida con los datos de propiedades extraídos.
# - `datos_limpios.csv`: Archivo final con los datos procesados para análisis.
# - `SegundaParte/Bookings.csv` y `SegundaParte/Properties.csv`: Archivos originales necesarios para la ejecución del proceso ETL.

## Notas Importantes
# - **Tiempo de Espera**: El código de scraping incluye `time.sleep(30)` para esperar la carga de la página. 
#    Puedes ajustar el tiempo según la velocidad de carga de tu conexión.
# - **Manejo de Errores**: El código maneja excepciones en la extracción de datos; cualquier error 
#    se registra en consola para diagnóstico.
# - **Límites de Extracción**: El script de scraping detiene la extracción al alcanzar 100 propiedades; 
#    puedes ajustar el límite modificando el parámetro `max_properties`.
