from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuarios, Propiedades
from django.contrib.auth.forms import UserCreationForm
from .forms import PropiedadesForm, PropiedadesImagenesFormSet, PerfilUsuarioForm
from .models import Propiedades, Comunas, Regiones
from .services import (
    obtener_usuario_actual, obtener_propiedades, obtener_propiedad_por_id,
    autenticar_usuario, registrar_usuario, obtener_usuario_para_perfil,
    guardar_perfil_usuario, obtener_propiedades_por_arrendador,
    guardar_propiedad_y_imagenes, actualizar_propiedad, eliminar_propiedad_servicio
)

def home(request):
    usuario = obtener_usuario_actual(request.user)
    propiedades = obtener_propiedades()
    return render(request, 'home.html', {'propiedades': propiedades, 'usuario': usuario})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = autenticar_usuario(username, password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        if registrar_usuario(request.POST):
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    usuario = obtener_usuario_para_perfil(request.user)
    user = request.user
    return render(request, 'profile.html', {'user': user, 'usuario': usuario})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def editar_perfil(request):
    usuario = Usuarios.objects.get(user=request.user)

    if request.method == 'POST':
        if guardar_perfil_usuario(usuario, request.POST):
            return redirect('profile')
    else:
        form = PerfilUsuarioForm(instance=usuario)

    return render(request, 'editar_perfil.html', {'form': form, 'usuario': usuario})

@login_required
def propiedades_list(request):
    # Obtener los IDs de regiones y comunas del GET
    usuario = Usuarios.objects.get(user=request.user)
    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    regiones = Regiones.objects.all()
    comunas = Comunas.objects.all()
    propiedades = Propiedades.objects.all()

    if region_id:
        propiedades = propiedades.filter(comuna__region_id=region_id)
    if comuna_id:
        propiedades = propiedades.filter(comuna_id=comuna_id)

    # Convertir comunas a formato JSON
    comunas_data = list(comunas.values('id', 'nombre', 'region_id'))

    context = {
        'propiedades': propiedades,
        'regiones': regiones,
        'comunas': comunas,
        'comunas_data': comunas_data,
        'usuario': usuario
    }
    return render(request, 'propiedades_list.html', context)

def detalle_propiedad(request, propiedad_id):
    usuario = obtener_usuario_actual(request.user)
    propiedad = obtener_propiedad_por_id(propiedad_id)
    return render(request, 'detalle_propiedad.html', {'propiedad': propiedad, 'usuario': usuario})

@login_required
def propiedades_arrendador(request):
    usuario = request.user.usuarios_set.first()
    if usuario.tu.tu_id == 2:
        propiedades = obtener_propiedades_por_arrendador(usuario)
        return render(request, 'propiedades_arrendador.html', {'propiedades': propiedades, "usuario": usuario})
    else:
        return redirect('home')

@login_required
def crear_propiedad(request):
    usuario = Usuarios.objects.get(user=request.user)
    
    if request.method == 'POST':
        propiedad = guardar_propiedad_y_imagenes(request.POST, request.FILES, usuario)
        if propiedad:
            return redirect('propiedades_arrendador')
    else:
        propiedad_form = PropiedadesForm()
        imagenes_formset = PropiedadesImagenesFormSet()

    return render(request, 'crear_propiedad.html', {
        'propiedad_form': propiedad_form,
        'imagenes_formset': imagenes_formset,
        'usuario': usuario
    })

@login_required
def editar_propiedad(request, pk):
    usuario = Usuarios.objects.get(user=request.user)
    propiedad = obtener_propiedad_por_id(pk)
    
    if request.method == 'POST':
        if actualizar_propiedad(propiedad, request.POST, request.FILES):
            return redirect('detalle_propiedad', propiedad_id=propiedad.id)
    else:
        form = PropiedadesForm(instance=propiedad)
        formset = PropiedadesImagenesFormSet(instance=propiedad)
    
    return render(request, 'editar_propiedad.html', {
        'form': form,
        'formset': formset,
        'propiedad': propiedad,
        'usuario':usuario
    })

@login_required
def eliminar_propiedad(request, propiedad_id):
    usuario = request.user.usuarios_set.first()  # Asegúrate de que estás obteniendo el usuario relacionado
    propiedad = get_object_or_404(Propiedades, id=propiedad_id)
    
    # Verifica que el usuario actual sea el arrendador de la propiedad
    if propiedad.arrendador == usuario:
        if request.method == 'POST':
            eliminar_propiedad_servicio(propiedad)
            return redirect('propiedades_arrendador')
    
    return render(request, 'eliminar_propiedad.html', {'propiedad': propiedad, 'usuario':usuario})

@login_required
def mis_propiedades(request):
    auth_user = request.user
    try:
        usuario = Usuarios.objects.get(user=auth_user)
    except Usuarios.DoesNotExist:
        usuario = None

    if usuario:
        propiedades = obtener_propiedades_por_arrendador(usuario)
    else:
        propiedades = []

    return render(request, 'mis_propiedades.html', {'propiedades': propiedades})
