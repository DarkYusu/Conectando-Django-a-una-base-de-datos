from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Usuarios

def home(request):
    return render(request, 'home.html')

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
    user = request.user
    return render(request, 'profile.html', {'user': user})

# Vista para logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
