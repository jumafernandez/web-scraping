from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from funciones_carrefour import scraping_carrefour_argentina

# Dirección al driver de Chrome para Selenium
CHROME_DRIVER_PATH = "C:/Users/Juan/Documents/GitHub/pimei-2023/chromedriver"  # Ruta constante del controlador de Chrome

# Configuración de selenium
options = Options()
options.add_argument("--headless")
service = Service(CHROME_DRIVER_PATH)
driver_chrome = webdriver.Chrome(service=service, options=options)

# Scrapea y persiste la matriz de precios en un csv
df_carrefour = scraping_carrefour_argentina(['Almacen', 'Bebidas'], driver_chrome)
df_carrefour.to_csv('matriz-carrefour.csv', index=False)
