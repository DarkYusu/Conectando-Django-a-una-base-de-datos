from .models import Usuarios, Propiedades, Arrendamientos

def registrar_usuario(data):
    """ Registra un nuevo usuario en la base de datos """
    usuario = Usuarios.objects.create(**data)
    return usuario

def publicar_propiedad(data, arrendador):
    """ Publica una nueva propiedad para un arrendador específico """
    propiedad = Propiedades.objects.create(**data, arrendador=arrendador)
    return propiedad

def listar_propiedades_por_comuna(comuna):
    """ Lista todas las propiedades en una comuna específica """
    return Propiedades.objects.filter(comuna=comuna)

def generar_solicitud_arriendo(arrendatario, propiedad):
    """ Genera una solicitud de arriendo para una propiedad específica """
    arrendamiento = Arrendamientos.objects.create(arrendatario=arrendatario, propiedad=propiedad)
    return arrendamiento

def aceptar_arrendatario(arrendamiento):
    """ Acepta una solicitud de arriendo """
    arrendamiento.estado = 'aceptado'
    arrendamiento.save()
    return arrendamiento
