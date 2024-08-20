from django.db import models

# Create your models here.

class Usuarios(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    rut = models.CharField(unique=True, max_length=12)
    direccion = models.CharField(max_length=255)
    telefono_personal = models.CharField(max_length=20, blank=True, null=True)
    correo_electronico = models.CharField(unique=True, max_length=255)
    tipo_usuario = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class Propiedades(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    m2_construidos = models.FloatField()
    m2_totales = models.FloatField()
    cantidad_estacionamientos = models.IntegerField()
    cantidad_habitaciones = models.IntegerField()
    cantidad_banos = models.IntegerField()
    direccion = models.CharField(max_length=255)
    tipo_inmueble = models.CharField(max_length=20)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    arrendador = models.ForeignKey(Usuarios, models.DO_NOTHING)
    comuna = models.ForeignKey('Comunas', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'propiedades'


class Arrendamientos(models.Model):
    arrendatario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    propiedad = models.ForeignKey(Propiedades, models.DO_NOTHING)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arrendamientos'


class Comunas(models.Model):
    nombre = models.CharField(unique=True, max_length=255)
    region = models.ForeignKey('Regiones', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comunas'


class Regiones(models.Model):
    nombre = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'regiones'


class PropiedadesComunas(models.Model):
    propiedad = models.ForeignKey(Propiedades, models.DO_NOTHING)
    comuna = models.ForeignKey(Comunas, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'propiedades_comunas'
