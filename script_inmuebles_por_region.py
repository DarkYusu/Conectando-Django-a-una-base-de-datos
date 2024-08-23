import django
import os

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arriendahogar_proyecto.settings')
django.setup()

from arrendahogar_aplicacion.models import Propiedades, Comunas, Regiones

def exportar_inmuebles_por_region():
    # Realiza la consulta para obtener propiedades, comunas y regiones
    propiedades = Propiedades.objects.select_related('comuna__region').values(
        'nombre', 'descripcion', 'comuna__region__nombre'
    ).order_by('comuna__region__nombre')
    
    # Diccionario para almacenar inmuebles por región
    inmuebles_por_region = {}
    
    for propiedad in propiedades:
        region = propiedad['comuna__region__nombre']
        if region not in inmuebles_por_region:
            inmuebles_por_region[region] = []
        inmuebles_por_region[region].append(f"Nombre: {propiedad['nombre']}\nDescripción: {propiedad['descripcion']}\n")
    
    # Guardar en archivo de texto
    with open('inmuebles_por_region.txt', 'w', encoding='utf-8') as archivo:
        for region, inmuebles in inmuebles_por_region.items():
            archivo.write(f"Región: {region}\n")
            archivo.write('-' * 20 + '\n')
            archivo.writelines(inmuebles)
            archivo.write('\n')

if __name__ == "__main__":
    exportar_inmuebles_por_region()
