from django.urls import path
from .views import cambio_estado, archivo_mov

app_name = 'movimiento'
urlpatterns = [
    path('cambio_estado/<int:proy_id>', cambio_estado, name='cambio_estado'),
    path('archivo_mov/<int:mov_id>', archivo_mov, name='archivo_mov'),
]