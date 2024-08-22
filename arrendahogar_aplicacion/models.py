from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
        
class Usuarios(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    rut = models.CharField(unique=True, max_length=12)
    direccion = models.CharField(max_length=255)
    telefono_personal = models.CharField(max_length=20, blank=True, null=True)
    correo_electronico = models.CharField(unique=True, max_length=255)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tu = models.ForeignKey('TipoUsuario', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class TipoUsuario(models.Model):
    tu_id = models.AutoField(primary_key=True)
    tu_nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_usuario'


class Regiones(models.Model):
    nombre = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'regiones'


class PropiedadesComunas(models.Model):
    propiedad = models.ForeignKey('Propiedades', models.DO_NOTHING)
    comuna = models.ForeignKey('Comunas', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'propiedades_comunas'


class Propiedades(models.Model):
    TIPO_INMUEBLE_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('oficina', 'Oficina'),
    ]
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    m2_construidos = models.IntegerField()
    m2_totales = models.IntegerField()
    cantidad_estacionamientos = models.IntegerField()
    cantidad_habitaciones = models.IntegerField()
    cantidad_banos = models.IntegerField()
    direccion = models.CharField(max_length=255)
    tipo_inmueble = models.CharField(max_length=20, choices=TIPO_INMUEBLE_CHOICES)
    precio_mensual = models.IntegerField()
    arrendador = models.ForeignKey(Usuarios, models.DO_NOTHING)
    comuna = models.ForeignKey('Comunas', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'propiedades'



class Comunas(models.Model):
    nombre = models.CharField(unique=True, max_length=255)
    region = models.ForeignKey(Regiones, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comunas'
        
    def __str__(self):
        return self.nombre


class Arrendamientos(models.Model):
    arrendatario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    propiedad = models.ForeignKey(Propiedades, models.DO_NOTHING)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arrendamientos'
