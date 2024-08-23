"""arriendahogar_proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from arrendahogar_aplicacion.views import user_login, user_logout, user_register, profile, home, propiedades_list,propiedades_arrendador,crear_propiedad,editar_propiedad, eliminar_propiedad,bas,editar_perfil,detalle_propiedad

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('profile/', profile, name='profile'),
    path('perfil/', editar_perfil, name='perfil_usuario'),
    path('logout/', user_logout, name='logout'),
    path('propiedades/', propiedades_list, name='propiedades_list'),
    path('propiedad/<int:propiedad_id>/', detalle_propiedad, name='detalle_propiedad'),
    path('mis-propiedades/', propiedades_arrendador, name='propiedades_arrendador'),
    path('crear-propiedad/', crear_propiedad, name='crear_propiedad'),
    path('editar-propiedad/<int:pk>/', editar_propiedad, name='editar_propiedad'),
    path('eliminar-propiedad/<int:propiedad_id>/', eliminar_propiedad, name='eliminar_propiedad'),
    path('base/', bas, name='base'),
]
