from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm, PropiedadForm, ArrendamientoForm
from .models import Propiedades, Arrendamientos
from .services import registrar_usuario, publicar_propiedad, listar_propiedades_por_comuna, generar_solicitud_arriendo, aceptar_arrendatario
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def registrar_usuario_view(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            registrar_usuario(form.cleaned_data)
            return redirect('home')
    else:
        form = UsuarioForm()
    return render(request, 'registrar_usuario.html', {'form': form})

def listar_propiedades_view(request):
    comuna = request.GET.get('comuna')
    propiedades = listar_propiedades_por_comuna(comuna) if comuna else Propiedades.objects.all()
    return render(request, 'listar_propiedades.html', {'propiedades': propiedades})

@login_required
def publicar_propiedad_view(request):
    # Verificar si el usuario es un arrendador
    if request.user.tipo_usuario != 'arrendador':
        messages.error(request, 'Solo los arrendadores pueden publicar propiedades.')
        return redirect('home')

    if request.method == 'POST':
        form = PropiedadForm(request.POST)
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.arrendador = request.user  # Asignar el usuario como arrendador
            propiedad.save()
            messages.success(request, 'Propiedad publicada con éxito.')
            return redirect('listar_propiedades')
    else:
        form = PropiedadForm()

    return render(request, 'arriendahogar_aplicacion/publicar_propiedad.html', {'form': form})


def generar_solicitud_arriendo_view(request, propiedad_id):
    propiedad = get_object_or_404(Propiedades, id=propiedad_id)
    if request.method == 'POST':
        form = ArrendamientoForm(request.POST)
        if form.is_valid():
            generar_solicitud_arriendo(request.user, propiedad)
            return redirect('listar_propiedades')
    else:
        form = ArrendamientoForm()
    return render(request, 'generar_solicitud_arriendo.html', {'form': form, 'propiedad': propiedad})

def aceptar_arrendatario_view(request, arrendamiento_id):
    arrendamiento = get_object_or_404(Arrendamientos, id=arrendamiento_id)
    aceptar_arrendatario(arrendamiento)
    return redirect('listar_propiedades')
