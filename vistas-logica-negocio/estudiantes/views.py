from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from .utils import obtener_temas_por_unidad
from .models import Tema, Ejercicio, Intento, Aprender

def inicio(request):
    return render(request, 'estudiantes/login.html')




@csrf_exempt 
def login_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'redirect_url': '/temas/'   # cambia a donde quieras
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Usuario o Contraseña incorrectas'
            })

    return JsonResponse({'success': False})


def temas(request):
    unidades_ordenadas = obtener_temas_por_unidad()

    return render(request, 'estudiantes/temas.html', {
        'unidades': unidades_ordenadas
    })



def ejercicios(request, id):
    unidades_ordenadas = obtener_temas_por_unidad()
    tema = Tema.objects.get(id=id)

    ejercicios = Ejercicio.objects.filter(tema=tema)\
        .prefetch_related('intentos')\
        .annotate(total_intentos=Count('intentos'))

    return render(request, 'estudiantes/ejercicios.html', {
        'unidades': unidades_ordenadas,
        'temaPrincipal': tema,
        'ejerciciosEnviados': ejercicios
    })


def ejercicioAprender(request, id):
    unidades_ordenadas = obtener_temas_por_unidad()
    
    ejercicio = Ejercicio.objects.get(id=id)
    tema = ejercicio.tema

    aprender = Aprender.objects.get(ejercicio__id=id)

    return render(request, 'estudiantes/ejercicio_aprender.html', {
        'unidades': unidades_ordenadas,
        'temaPrincipal': tema,
        'aprenderEnviado': aprender,
        'ejercicioEnviado': ejercicio
    })

def ejercicioResolver(request, id):
    unidades_ordenadas = obtener_temas_por_unidad()

    ejercicioAux = Ejercicio.objects.get(id=id)
    tema = ejercicioAux.tema

    ejercicio = Ejercicio.objects\
        .prefetch_related('intentos')\
        .annotate(total_intentos=Count('intentos'))\
        .get(id=id)

    return render(request, 'estudiantes/ejercicio_resolver.html', {
        'unidades': unidades_ordenadas,
        'temaPrincipal': tema,
        'ejercicioEnviado': ejercicio
    })


@csrf_exempt
def agregar_respuesta(request):
    if request.method == 'POST':
        respuesta = request.POST.get('valor')
        id = request.POST.get('id')

        user = request.user 
        ejercicio = Ejercicio.objects.get(id=id)

        if respuesta == ejercicio.solucion_esperada_ejercicio:
            Intento.objects.create(
                usuario=user,
                ejercicio=ejercicio,
                respuesta=respuesta,
                resultado="1"
            )
            return JsonResponse({
                'success': True,
                'correcto': "correcto",
                'redirect_url': '/ejercicio_resolver/'   # cambia a donde quieras
            })
        else:
            Intento.objects.create(
                usuario=user,
                ejercicio=ejercicio,
                respuesta=respuesta,
                resultado="0"
            )
            return JsonResponse({
                'success': True,
                'redirect_url': '/ejercicio_resolver/'   # cambia a donde quieras
            })

    return JsonResponse({'success': False})

