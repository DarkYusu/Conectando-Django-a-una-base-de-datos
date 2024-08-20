from django.contrib import admin
from .models import Usuarios, Propiedades, Arrendamientos, Comunas, Regiones, PropiedadesComunas

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'correo_electronico', 'tipo_usuario', 'fecha_registro')
    search_fields = ('nombres', 'apellidos', 'rut', 'correo_electronico')

@admin.register(Propiedades)
class PropiedadesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'cantidad_estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'direccion', 'tipo_inmueble', 'precio_mensual', 'arrendador', 'comuna')
    search_fields = ('nombre', 'descripcion', 'direccion', 'tipo_inmueble')
    list_filter = ('arrendador', 'comuna')

@admin.register(Arrendamientos)
class ArrendamientosAdmin(admin.ModelAdmin):
    list_display = ('arrendatario', 'propiedad', 'fecha_solicitud', 'estado')
    search_fields = ('arrendatario__nombres', 'propiedad__nombre', 'estado')
    list_filter = ('estado',)

@admin.register(Comunas)
class ComunasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region')
    search_fields = ('nombre', 'region__nombre')

@admin.register(Regiones)
class RegionesAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(PropiedadesComunas)
class PropiedadesComunasAdmin(admin.ModelAdmin):
    list_display = ('propiedad', 'comuna')
    search_fields = ('propiedad__nombre', 'comuna__nombre')
