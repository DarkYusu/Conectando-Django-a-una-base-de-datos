from django.db import models

class Usuarios(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    rut = models.CharField(unique=True, max_length=12)
    direccion = models.CharField(max_length=255)
    telefono_personal = models.CharField(max_length=20, blank=True, null=True)
    correo_electronico = models.CharField(unique=True, max_length=255)
    tipo_usuario = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Auto set to current timestamp

    # Relación Many-to-Many con Propiedades para marcar favoritas
    propiedades_favoritas = models.ManyToManyField('Propiedades', through='UsuariosPropiedadesFavoritas', related_name='usuarios_favoritos')

    class Meta:
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
    comuna = models.CharField(max_length=255)
    tipo_inmueble = models.CharField(max_length=20)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    arrendador = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='propiedades_publicadas')

    # Relación Many-to-Many con Comunas
    comunas = models.ManyToManyField('Comunas', through='PropiedadesComunas', related_name='propiedades')

    class Meta:
        db_table = 'propiedades'


class Arrendamientos(models.Model):
    arrendatario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='arrendamientos')
    propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE, related_name='arrendamientos')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)  # Auto set to current timestamp
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')], default='pendiente')

    class Meta:
        db_table = 'arrendamientos'


class Comunas(models.Model):
    nombre = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'comunas'


class PropiedadesComunas(models.Model):
    propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comunas, on_delete=models.CASCADE)

    class Meta:
        db_table = 'propiedades_comunas'
        unique_together = ('propiedad', 'comuna')  # Ensure a property is not linked to the same comuna more than once


class UsuariosPropiedadesFavoritas(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)  # Auto set to current timestamp

    class Meta:
        db_table = 'usuarios_propiedades_favoritas'
        unique_together = ('usuario', 'propiedad')  # Ensure a user can't favorite the same property more than once
