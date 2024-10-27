import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Rutas de archivos que estoy utilizando
bookings_path = 'SegundaParte/Bookings.csv'
properties_path = 'SegundaParte/Properties.csv'
datos_limpios_path  = 'SegundaParte/datos_limpios.csv' 

# Estilo de Seaborn para los gráficos
sns.set_theme(style="whitegrid")

# Ya con las rutas parametrizadas procederé a realizar los procesos ETL y EDA

# Proceso ETL
# 1- Extracción -- Conversion a Dataframe
# Cargar los datos desde los CSV
bookings_df = pd.read_csv(bookings_path, encoding='utf-8')
properties_df = pd.read_csv(properties_path, encoding='utf-8')

# 2- Transformación
# Cambiar el formato de las fechas en Bookings
bookings_df['BookingCreatedDate'] = pd.to_datetime(bookings_df['BookingCreatedDate'], errors='coerce')
bookings_df['ArrivalDate'] = pd.to_datetime(bookings_df['ArrivalDate'], errors='coerce')
bookings_df['DepartureDate'] = pd.to_datetime(bookings_df['DepartureDate'], errors='coerce')

# Unir los DataFrames en base al PropertyId
merged_df = pd.merge(bookings_df, properties_df, on='PropertyId', how='left')

# Limpieza de datos
# Verificar y llenar valores faltantes en la clumna BookingCreatedDate
merged_df['RoomRate'].fillna(0, inplace=True)
merged_df['Revenue'].fillna(0, inplace=True)
merged_df['ADR'].fillna(0, inplace=True)
merged_df['PropertyType'].fillna('Desconocido', inplace=True)
merged_df['Channel'].fillna('Desconocido', inplace=True)
merged_df['BookingCreatedDate'].fillna(pd.to_datetime('today'), inplace=True)
merged_df.drop_duplicates(inplace=True)

# 3- Carga
# Guardar el DataFrame limpio en un nuevo archivo CSV
merged_df.to_csv(datos_limpios_path, index=False, encoding='utf-8')

print("El Proceso ETL esta completado. Los datos se han guardado en:", datos_limpios_path)

# Análisis Exploratorio de Datos (EDA)
# Resumen estadístico
print(merged_df.describe())

# Calcular la media de la tarifa de la habitación
mean_room_rate = merged_df['RoomRate'].mean()

# Visualización de la distribución de las tarifas de las habitaciones
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['RoomRate'], bins=30, kde=True, color='blue', stat='density', linewidth=0)
plt.axvline(mean_room_rate, color='red', linestyle='dashed', linewidth=1, label='Media')
plt.text(mean_room_rate + 10, 0.02, f'Media: {mean_room_rate:.2f}', color='red')
plt.title('Distribución de las Tarifas de las Habitaciones')
plt.xlabel('Tarifa de la Habitación')
plt.ylabel('Densidad')
plt.legend()
plt.show()

# Visualización de la tarifa promedio por tipo de propiedad utilizando un gráfico de barras
plt.figure(figsize=(10, 6))
avg_room_rate = merged_df.groupby('PropertyType')['RoomRate'].mean().reset_index()
sns.barplot(x='PropertyType', y='RoomRate', hue='PropertyType', data=avg_room_rate, palette='Set3', legend=False)
plt.title('Tarifa Promedio por Tipo de Propiedad')
plt.xlabel('Tipo de Propiedad')
plt.ylabel('Tarifa Promedio de la Habitación')
plt.xticks(rotation=45)
plt.show()
