# script_exportar_inmuebles.py

import django
import os

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arriendahogar_proyecto.settings')
django.setup()

from arrendahogar_aplicacion.models import Propiedades  # Importa el modelo Propiedades

def exportar_inmuebles():
    # Realiza la consulta para obtener nombre, descripción y comuna de los inmuebles
    propiedades = Propiedades.objects.values('nombre', 'descripcion', 'comuna').order_by('comuna')
    
    # Diccionario para almacenar inmuebles por comuna
    inmuebles_por_comuna = {}
    
    for propiedad in propiedades:
        comuna = propiedad['comuna']
        if comuna not in inmuebles_por_comuna:
            inmuebles_por_comuna[comuna] = []
        inmuebles_por_comuna[comuna].append(f"Nombre: {propiedad['nombre']}\nDescripción: {propiedad['descripcion']}\n")
    
    # Guardar en archivo de texto
    with open('inmuebles_por_comuna.txt', 'w', encoding='utf-8') as archivo:
        for comuna, inmuebles in inmuebles_por_comuna.items():
            archivo.write(f"Comuna: {comuna}\n")
            archivo.write('-' * 20 + '\n')
            archivo.writelines(inmuebles)
            archivo.write('\n')

if __name__ == "__main__":
    exportar_inmuebles()
