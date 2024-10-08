# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Propiedades(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    m2_construidos = models.IntegerField()
    m2_totales = models.IntegerField()
    cantidad_estacionamientos = models.IntegerField()
    cantidad_habitaciones = models.IntegerField()
    cantidad_banos = models.IntegerField()
    direccion = models.CharField(max_length=255)
    tipo_inmueble = models.CharField(max_length=20)
    precio_mensual = models.IntegerField()
    arrendador = models.ForeignKey('Usuarios', models.DO_NOTHING)
    comuna = models.ForeignKey('Comunas', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'propiedades'


class PropiedadesImagenes(models.Model):
    pi_id = models.AutoField(primary_key=True)
    propiedad = models.ForeignKey(Propiedades, models.DO_NOTHING)
    pi_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'propiedades_imagenes'
