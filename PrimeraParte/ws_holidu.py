from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Especifica la ruta de geckodriver
driver_path = 'C:\\Users\\jhers\\OneDrive\\Escritorio\\driver\\geckodriver.exe'
options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override", 
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

# Iniciar el navegador con el servicio
service = Service(driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Listas para almacenar datos
lst_titulo = []
lst_ubi = []
lst_hab = []
lst_precio = []
lst_puntuacion = []

# Navegar a la página
url = 'https://www.holidu.es/s/Barcelona--Catalu%C3%B1a--Espa%C3%B1a?checkin=2024-11-20&checkout=2024-11-21'
driver.get(url)

# Espera a que cargue la página
time.sleep(30)

# Número de propiedades a extraer
max_properties = 100

try:
    # Scroll hasta que se carguen suficientes propiedades
    while len(lst_titulo) < max_properties:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'OfferItem')))
        propiedades = driver.find_elements(By.CLASS_NAME, 'OfferItem')

        # Extraer datos de las propiedades
        for propiedad in propiedades:
            if len(lst_titulo) >= max_properties:
                break
            
            try:
                # Extraer título
                titulo = propiedad.find_element(By.CSS_SELECTOR, 'div[data-elem-tracking-id="TITLE"] span').text
                lst_titulo.append(titulo)
            except Exception as e:
                lst_titulo.append(None)
                print(f"Error al obtener el título: {e}")

            try:
                # Extraer ubicación
                ubicacion = propiedad.find_element(By.CSS_SELECTOR, 'span[data-testid="LocationLine"] button span').text
                lst_ubi.append(ubicacion)
            except Exception as e:
                lst_ubi.append(None)
                print(f"Error al obtener la ubicación: {e}")

            try:
                # Extraer descripcion
                habitaciones_div = propiedad.find_element(By.CSS_SELECTOR, 'div.flex.flex-wrap.text-xs.text-grey-800')
                habitaciones_text = [element.text for element in habitaciones_div.find_elements(By.TAG_NAME, 'div')]
                lst_hab.append(', '.join(habitaciones_text))  
            except Exception as e:
                lst_hab.append(None)
                print(f"Error al obtener la descripcion: {e}, HTML de propiedad: {propiedad.get_attribute('outerHTML')}")

            try:
                # Extraer precio
                precio = propiedad.find_element(By.CSS_SELECTOR, 'div.whitespace-nowrap.text-sm.text-black-ultra').text
                lst_precio.append(precio)
            except Exception as e:
                lst_precio.append(None)
                print(f"Error al obtener el precio: {e}")

            try:
                # Extraer puntuación
                puntuacion = propiedad.find_element(By.CSS_SELECTOR, 'div.ml-xxs.text-sm.font-bold.text-black-ultra').text
                lst_puntuacion.append(puntuacion)
            except Exception as e:
                lst_puntuacion.append(None)
                print(f"Error al obtener la puntuación: {e}")

        # Hacer scroll hacia abajo para cargar más propiedades
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3) 

except Exception as e:
    print(f"Error al cargar la página: {e}")

# # Imprimir resultados en consola para verificar los errores
# print("Resultados extraídos:")
# for i in range(len(lst_titulo)):
#     print(f"Título: {lst_titulo[i]}, Ubicación: {lst_ubi[i]}, Descripción: {lst_hab[i]}, Precio: {lst_precio[i]}, Puntuación: {lst_puntuacion[i]}")

# Guardar los datos en un archivo CSV
with open('propiedades_holidu.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Título', 'Ubicación', 'Descripcion', 'Precio', 'Puntuación'])  # Escribe la cabecera
    for i in range(len(lst_titulo)):
        writer.writerow([lst_titulo[i], lst_ubi[i], lst_hab[i], lst_precio[i], lst_puntuacion[i]])  # Escribe los datos

print("Datos guardados en propiedades_holidu.csv")

# Cerrar el navegador
driver.quit()
