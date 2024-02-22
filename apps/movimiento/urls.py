from django.urls import path
from .views import cambio_estado

app_name = 'movimiento'
urlpatterns = [
    path('cambio_estado/<int:proy_id>', cambio_estado, name='cambio_estado'),
]