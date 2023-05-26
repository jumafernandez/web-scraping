# -*- coding: utf-8 -*-

from datetime import datetime

def fecha_hora_actual_str():
    # Obtén la fecha y hora actual
    fecha_hora_actual = datetime.now()
    
    # Formatea la fecha y hora en una cadena de texto
    fecha_hora_str = fecha_hora_actual.strftime("%Y%m%d-%H%M%S")
    
    # Retorna la fecha y hora actual en formato de cadena
    return fecha_hora_str
