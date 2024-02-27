"""
URL configuration for laboratorio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from apps.sistema import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='inicio'),
    path('usuarios/', views.usuario_lista, name='usuariosLista'),
    path('registrar/', views.signup, name='registrar'),
    path('login/', views.signin, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('buscarEstudiante/', views.buscarEstudiante, name='buscarEstudiante'),
    path('buscarDocente/', views.buscarDocente, name='buscarDocente'),
    path('proyecto/', include('apps.proyecto.urls', namespace='proyecto')),
    path('tribunal/', include('apps.tribunal.urls', namespace='tribunal')),
    path('movimiento/', include('apps.movimiento.urls', namespace='movimiento')),
]
