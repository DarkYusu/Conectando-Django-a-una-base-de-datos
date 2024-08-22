from django import forms
from .models import Propiedad

class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'cantidad_estacionamientos', 
                  'cantidad_habitaciones', 'cantidad_banos', 'direccion', 'comuna', 'tipo_inmueble', 'precio_mensual']