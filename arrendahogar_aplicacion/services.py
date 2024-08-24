from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Usuarios, Propiedades
from .forms import PropiedadesForm, PropiedadesImagenesFormSet, PerfilUsuarioForm

def obtener_usuario_actual(user):
    return Usuarios.objects.filter(user_id=user.id).first()

def obtener_propiedades():
    return Propiedades.objects.all()

def obtener_propiedad_por_id(propiedad_id):
    return get_object_or_404(Propiedades, id=propiedad_id)

def autenticar_usuario(username, password):
    user = authenticate(username=username, password=password)
    return user

def registrar_usuario(post_data):
    form = UserCreationForm(post_data)
    if form.is_valid():
        form.save()
        return True
    return False

def obtener_usuario_para_perfil(user):
    return Usuarios.objects.filter(user_id=user.id).first()

def guardar_perfil_usuario(usuario, post_data):
    form = PerfilUsuarioForm(post_data, instance=usuario)
    if form.is_valid():
        form.save()
        return True
    return False

def obtener_propiedades_por_arrendador(usuario):
    return Propiedades.objects.filter(arrendador=usuario)

def guardar_propiedad_y_imagenes(post_data, files, usuario):
    propiedad_form = PropiedadesForm(post_data)
    imagenes_formset = PropiedadesImagenesFormSet(post_data, files)
    
    if propiedad_form.is_valid() and imagenes_formset.is_valid():
        propiedad = propiedad_form.save(commit=False)
        propiedad.arrendador = usuario
        propiedad.save()

        # Guardar las imágenes asociadas a la propiedad
        for form in imagenes_formset.forms:
            if form.cleaned_data.get('pi_url'):
                imagen = form.save(commit=False)
                imagen.propiedad = propiedad
                imagen.save()

        return propiedad
    return None

def actualizar_propiedad(propiedad, post_data, files):
    form = PropiedadesForm(post_data, instance=propiedad)
    formset = PropiedadesImagenesFormSet(post_data, files, instance=propiedad)
    
    if form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        return True
    return False

def eliminar_propiedad(propiedad):
    propiedad.delete()
