# -*- coding: utf-8 -*-
"""
Created on Thu May 25 18:27:28 2023

@author: Juan
"""

import pandas as pd
from bs4 import BeautifulSoup
import json

def formatear_matriz_precios_carrefour(df_matriz):
    '''
    Parameters
    ----------
    df_matriz : DataFrame
        Información de precios sin formatear

    Returns
    -------
    df_productos : DataFrame
        Información de precios plana y preprocesada

    '''
    
    # Utiliza json_normalize() para aplanar los diccionarios en columnas planas
    df_matriz_flat = pd.json_normalize(df_matriz.to_dict('records'))
    
    # Defino las columnas con las que me quedo
    df_productos = df_matriz_flat[['@id', 'description', 'image', 'mpn', 'name', 'sku', 'brand.name', 'offers.lowPrice', 'offers.highPrice']]
    
    # Las renombro
    df_productos.rename(columns={'@id': 'url_producto',
                       'description': 'descripcion',
                       'image': 'imagen',
                       'mpn': 'mpn',
                       'name': 'producto',
                       'sku': 'sku',
                       'brand.name': 'marca',
                       'offers.lowPrice': 'precio_bajo',
                       'offers.highPrice': 'precio_alto'}, inplace=True)
    
    # Reordena las columnas
    column_order = ['producto', 'marca', 'descripcion', 'url_producto', 'imagen', 'mpn', 'sku', 'precio_bajo', 'precio_alto']
    df_productos = df_productos[column_order]
    
    return df_productos


def scraping_carrefour_argentina(lista_rubros, driver_chrome):
    """   
    Parameters
    ----------
    lista_rubros : list
        Lista de strings con los rubros a scrapear de Carrefour

    Returns
    -------
    df_productos : DataFrame
        Información de precios de todos los rubros solicitados
    """
    
    # Inicializo el df donde voy a guardar los productos
    df_matriz = pd.DataFrame()

    # Por cada rubro, voy a acceder a 50 páginas x 16 productos
    for rubro in lista_rubros:

        # Recorro 50 páginas del almacen
        for i in range(1, 51, 1):
        
            # Indicador gráfico del script (scraping general)
            print(f'Rubro {rubro} - Página {i}/50:')
            
            # Request selenium
            url = f'https://www.carrefour.com.ar/{rubro}/?page={i}'
            driver_chrome.get(url)
            html_content = driver_chrome.page_source
            
            # Parseo el div del html que tiene el json con los productos     
            soup = BeautifulSoup(html_content, 'html.parser')
            data_json = [json.loads(x.string) for x in soup.find_all("script", type="application/ld+json")]
        
            # Algunas veces no devuelve nada, para explorar
            if len(data_json)>0:
        
                # Algunas veces genera una lista adicional con datos, la desestimo
                if len(data_json)==1:
                    productos_json = data_json[0]['itemListElement']
                else:
                    productos_json = data_json[1]['itemListElement']
                
                # Recorro los 16 productos de la grilla
                i_p = 1
                for producto_web in productos_json:
                    
                    # Indicador gráfico del script (página)
                    print(f'\t-- Item {i_p}/16.')
            
                    # Tomo el item y lo guardo en el df
                    item = producto_web['item']
                    df_matriz = df_matriz.append(item, ignore_index=True)
                    
                    # Sumo 1 al contador
                    i_p+=1
        
    df_precios = formatear_matriz_precios_carrefour(df_matriz)
    
    return df_precios