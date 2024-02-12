from django.urls import path
from .views import proyecto_lista, proyecto_nuevo, proyecto_ver

app_name = 'proyecto'
urlpatterns = [
    path('lista', proyecto_lista, name='lista'),
    path('nuevo', proyecto_nuevo, name='nuevo'),
    path('ver/<int:proy_id>', proyecto_ver, name='ver'),
]
