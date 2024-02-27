from django.urls import path
from .views import proyecto_lista, proyecto_nuevo, proyecto_ver, proyecto_addEstudiante, proyecto_delEstudiante, \
    proyecto_addDocente, proyecto_delDocente, proyecto_addTribunal, proyecto_reportes, archivo_proy, borrador_proy

app_name = 'proyecto'
urlpatterns = [
    path('lista', proyecto_lista, name='lista'),
    path('nuevo', proyecto_nuevo, name='nuevo'),
    path('ver/<int:proy_id>', proyecto_ver, name='ver'),
    path('agregarEstudiante/', proyecto_addEstudiante, name='addEstudiante'),
    path('quitarEstudiante/', proyecto_delEstudiante, name='delEstudiante'),
    path('agregarDocente/', proyecto_addDocente, name='addDocente'),
    path('quitarDocente/', proyecto_delDocente, name='delDocente'),
    path('agregarTribunal/', proyecto_addTribunal, name='addTribunal'),
    path('reportes/', proyecto_reportes, name='reportes'),
    path('archivo_proy/<int:proy_id>', archivo_proy, name='archivo_proy'),
    path('borrador_proy/<int:proy_id>', borrador_proy, name='borrador_proy'),
]
