from django.urls import path
from .views import inicio, login_verify, temas, ejercicios, ejercicioResolver, agregar_respuesta, ejercicioAprender

urlpatterns = [
    path('login/', inicio),
    path('login/verify/', login_verify),
    path('temas/', temas,  name='temas'),
    path('ejercicios/<int:id>/', ejercicios, name='ejercicios'),
    path('ejercicio_resolver/<int:id>/', ejercicioResolver, name='ejercicio_resolver'),
    path('agregar_respuesta/', agregar_respuesta),
    path('ejercicio_aprender/<int:id>/', ejercicioAprender, name='ejercicio_aprender'),
]