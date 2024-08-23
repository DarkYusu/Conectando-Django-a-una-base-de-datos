from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Usuarios, Propiedades,AuthUser
from django.core.exceptions import ObjectDoesNotExist
from .forms import PropiedadesForm, PropiedadesImagenesFormSet,PerfilUsuarioForm

def home(request):
    usuario =Usuarios.objects.filter(user_id=request.user.id).first()
    return render(request, 'home.html', {"usuario":usuario})

def bas(request):
    usuario =Usuarios.objects.filter(user_id=request.user.id).first()
    return render(request, 'base.html', {"usuario":usuario})

# Vista para login de usuarios
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirige a la vista de perfil
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'login.html')

# Vista para registro de usuarios
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Vista de perfil de usuario
@login_required
def profile(request):
    usuario =Usuarios.objects.filter(user_id=request.user.id).first()
    user = request.user
    return render(request, 'profile.html', {'user': user, 'usuario':usuario})

# Vista para logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def editar_perfil(request):
    usuario = Usuarios.objects.get(user=request.user)

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario')
    else:
        form = PerfilUsuarioForm(instance=usuario)

    return render(request, 'editar_perfil.html', {'form': form, 'usuario':usuario})

@login_required
def propiedades_list(request):
    usuario =Usuarios.objects.filter(user_id=request.user.id).first()
    propiedades = Propiedades.objects.all()
    return render(request, 'propiedades_list.html', {'propiedades': propiedades,'usuario':usuario})

def detalle_propiedad(request, propiedad_id):
    usuario =Usuarios.objects.filter(user_id=request.user.id).first()
    propiedad = get_object_or_404(Propiedades, id=propiedad_id)
    return render(request, 'detalle_propiedad.html', {'propiedad': propiedad, 'usuario':usuario})

@login_required
def propiedades_arrendador(request):
    usuario = request.user.usuarios_set.first()  # Asumiendo que un usuario tiene un objeto Usuarios
    if usuario.tu.tu_id == 2:  # Verifica si es un arrendador
        usuario = Usuarios.objects.filter(user_id=request.user.id).first()
        propiedades = Propiedades.objects.filter(arrendador=usuario)
        return render(request, 'propiedades_arrendador.html', {'propiedades': propiedades,"usuario":usuario})
    else:
        return redirect('home')  # Redirige si no es un arrendador
    
from django.forms import ModelForm

class PropiedadForm(ModelForm):
    class Meta:
        model = Propiedades
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'cantidad_estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'direccion', 'tipo_inmueble', 'precio_mensual', 'comuna']

@login_required
def crear_propiedad(request):
    usuario = Usuarios.objects.get(user=request.user)
    
    if request.method == 'POST':
        propiedad_form = PropiedadesForm(request.POST)
        imagenes_formset = PropiedadesImagenesFormSet(request.POST, request.FILES)

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

            return redirect('propiedades_arrendador')
    else:
        propiedad_form = PropiedadesForm()
        imagenes_formset = PropiedadesImagenesFormSet()

    return render(request, 'crear_propiedad.html', {
        'propiedad_form': propiedad_form,
        'imagenes_formset': imagenes_formset,'usuario':usuario
    })

@login_required
def editar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedades, pk=pk)
    
    if request.method == 'POST':
        form = PropiedadesForm(request.POST, instance=propiedad)
        formset = PropiedadesImagenesFormSet(request.POST, request.FILES, instance=propiedad)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('detalle_propiedad', pk=propiedad.pk)
    else:
        form = PropiedadesForm(instance=propiedad)
        formset = PropiedadesImagenesFormSet(instance=propiedad)
    
    return render(request, 'editar_propiedad.html', {
        'form': form,
        'formset': formset,
        'propiedad': propiedad
    })

@login_required
def eliminar_propiedad(request, propiedad_id):
    usuario = request.user.usuarios_set.first()
    propiedad = get_object_or_404(Propiedades, id=propiedad_id, arrendador=usuario)
    if request.method == 'POST':
        propiedad.delete()
        return redirect('propiedades_arrendador')
    return render(request, 'eliminar_propiedad.html', {'propiedad': propiedad})

@login_required
def mis_propiedades(request):
    # Obtén el usuario autenticado
    auth_user = request.user

    # Encuentra el perfil del usuario en el modelo Usuarios
    try:
        usuario = Usuarios.objects.get(user=auth_user)

    except Usuarios.DoesNotExist:
        usuario = None

    # Si se encontró el perfil, obtiene las propiedades asociadas
    if usuario:
        propiedades = Propiedades.objects.filter(arrendador=usuario)
    else:
        propiedades = []

    return render(request, 'mis_propiedades.html', {'propiedades': propiedades})
