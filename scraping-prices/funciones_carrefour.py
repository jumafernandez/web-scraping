# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import json
from funciones_generales import fecha_hora_actual_str

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
    df_productos = df_matriz_flat[['@id', 'mpn', 'name', 'sku', 'brand.name', 'offers.lowPrice', 'offers.highPrice', 'rubro']]
    
    # Las renombro
    df_productos.rename(columns={'@id': 'url_producto',
                                 'mpn': 'mpn',
                                 'name': 'producto',
                                 'sku': 'sku',
                                 'brand.name': 'marca',
                                 'offers.lowPrice': 'precio_bajo',
                                 'offers.highPrice': 'precio_alto',
                                 'rubro': 'rubro'}, inplace=True)

    # Agrego la columna con la fecha del relevamiento
    df_productos['fecha_relevamiento'] = fecha_hora_actual_str()
    
    # Reordena las columnas
    column_order = ['fecha_relevamiento', 'producto', 'marca', 'rubro', 'url_producto', 'mpn', 'sku', 'precio_bajo', 'precio_alto']
    df_productos_ordenados = df_productos[column_order]
    
    return df_productos_ordenados


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

        # Recorro 50 páginas de cada rubro (es el máximo de carrefour)
        # o hasta que en 3 requests no se recuperen productos
        requests_negativos = 0
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
                
                
                # Si tiene productos los persiste
                if (len(productos_json)>0):

                    # Cada vez que se encuentran productos se inicializa el contador de requests negativos
                    requests_negativos = 0
                    # Recorro los 16 productos de la grilla
                    i_p = 1               
                   
                    # Los voy guardando
                    for producto_web in productos_json:
                        
                        # Indicador gráfico del script (página)
                        print(f'\t-- Item {i_p}/16.')
                
                        # Si hay productos los guardo 
                        # (algunos rubros tienen menos productos)
                        if 'item' in producto_web.keys():
                            # Tomo el item y lo guardo en el df
                            item = producto_web['item']
                            item['rubro'] = rubro
                            df_matriz = df_matriz.append(item, ignore_index=True)
                            
                            # Sumo 1 al contador
                            i_p+=1
            
                else: # En caso que no recupere productos
                    requests_negativos+=1
                    if requests_negativos==3:
                        print ("||| 3 Requests consecutivos sin productos recuperados, se pasa al siguiente rubro |||")
                        break
        
    return df_matriz