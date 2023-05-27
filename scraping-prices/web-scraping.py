from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from funciones_carrefour import scraping_carrefour_argentina, formatear_matriz_precios_carrefour
from funciones_generales import fecha_hora_actual_str

# Dirección al driver de Chrome para Selenium
CHROME_DRIVER_PATH = "C:/Users/Juan/Documents/GitHub/web-scraping/chromedriver"

# Configuración de selenium
options = Options()
options.add_argument("--headless")
service = Service(CHROME_DRIVER_PATH)
driver_chrome = webdriver.Chrome(service=service, options=options)


# Rubro único, usado para testeo
# rubros_relevamiento = ['Frutas-y-verduras']

# Me quedo con los rubros que quiero scrapear
rubros_relevamiento = ['Almacen',
                       'Bebidas',
                       'Carnes-y-pescados',
                       'Desayuno-y-merienda',
                       'Lacteos-y-productos-frescos',
                       'Carnes-y-pescados',
                       'Frutas-y-verduras',
                       'Panaderia',
                       'Congelados',
                       'Limpieza',
                       'Electro-y-tecnologia',
                       'Bazar-y-textil',
                       'Perfumeria']
                       
# Realizo e scraping que devuelve un df
matriz_carrefour_cruda = scraping_carrefour_argentina(rubros_relevamiento, driver_chrome)

# Formatea y ordena la matriz
matriz_carrefour_formateada = formatear_matriz_precios_carrefour(matriz_carrefour_cruda)

# Persiste la matriz en un csv
matriz_carrefour_formateada.to_csv(f'data/matriz-carrefour-{fecha_hora_actual_str()}.csv', index=False, sep='|')
