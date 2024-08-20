from django import forms
from .models import Usuarios, Propiedades, Arrendamientos

class UsuarioForm(forms.ModelForm):
    TIPO_USUARIO_CHOICES = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]

    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, label="Tipo de Usuario")

    class Meta:
        model = Usuarios
        fields = ['nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'correo_electronico', 'tipo_usuario']


class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedades
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'cantidad_estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'direccion', 'comuna', 'tipo_inmueble', 'precio_mensual']
        exclude = ['arrendador']  # Excluir el campo arrendador para que no sea manipulable

class ArrendamientoForm(forms.ModelForm):
    class Meta:
        model = Arrendamientos
        fields = ['propiedad', 'estado']
