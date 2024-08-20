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
from django.urls import path
from arriendahogar_aplicacion.views import registrar_usuario_view,listar_propiedades_view,publicar_propiedad_view,generar_solicitud_arriendo_view, aceptar_arrendatario_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrar_usuario/', registrar_usuario_view, name='registrar_usuario'),
    path('listar_propiedades/', listar_propiedades_view, name='listar_propiedades'),
    path('publicar_propiedad/', publicar_propiedad_view, name='publicar_propiedad'),
    path('generar_solicitud_arriendo/<int:propiedad_id>/', generar_solicitud_arriendo_view, name='generar_solicitud_arriendo'),
    path('aceptar_arrendatario/<int:arrendamiento_id>/', aceptar_arrendatario_view, name='aceptar_arrendatario'),
]
