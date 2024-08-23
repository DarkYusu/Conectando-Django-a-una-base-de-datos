from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Propiedades, PropiedadesImagenes

# Formulario para Propiedades
class PropiedadesForm(forms.ModelForm):
    class Meta:
        model = Propiedades
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 
                  'cantidad_estacionamientos', 'cantidad_habitaciones', 'cantidad_banos',
                  'direccion', 'tipo_inmueble', 'precio_mensual', 'comuna']

# Formulario para las imágenes de la propiedad
class PropiedadesImagenesForm(forms.ModelForm):
    class Meta:
        model = PropiedadesImagenes
        fields = ['pi_url']

# Inline formset para gestionar múltiples imágenes asociadas a una propiedad
PropiedadesImagenesFormSet = inlineformset_factory(
    Propiedades,
    PropiedadesImagenes,
    form=PropiedadesImagenesForm,
    extra=3,  # Número de formularios adicionales a mostrar inicialmente
    can_delete=True
)
