from django.contrib import admin
from .models import Usuarios, Propiedades, Arrendamientos, Comunas, PropiedadesComunas, UsuariosPropiedadesFavoritas

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'rut', 'correo_electronico', 'tipo_usuario', 'fecha_registro')

@admin.register(Propiedades)
class PropiedadesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'comuna', 'tipo_inmueble', 'precio_mensual', 'arrendador')

@admin.register(Arrendamientos)
class ArrendamientosAdmin(admin.ModelAdmin):
    list_display = ('arrendatario', 'propiedad', 'fecha_solicitud', 'estado')

@admin.register(Comunas)
class ComunasAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

# Opcionalmente, también puedes registrar las tablas intermedias
@admin.register(PropiedadesComunas)
class PropiedadesComunasAdmin(admin.ModelAdmin):
    list_display = ('propiedad', 'comuna')

@admin.register(UsuariosPropiedadesFavoritas)
class UsuariosPropiedadesFavoritasAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'propiedad', 'fecha_agregado')
