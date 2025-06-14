from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
#from LoginRegister.models import Ensayo
from AutoridadDocente.models import Ensayo, RespuestaEnsayo, RespuestaPregunta, Pregunta

def index(request):
    return render(request, 'base_estudiante.html')


def home_estudiante(request):
    return render(request, 'home_estudiante.html')


@login_required
def ensayos_view(request):
    estudiante = request.user
    ensayos = Ensayo.objects.filter(nivel=estudiante.nivel,colegio=estudiante.colegio)

    return render(request, 'ensayos.html', {'ensayos': ensayos})

def cuenta_view(request):
    return render(request, 'cuenta.html')

def aboutus_view(request):
    return render(request, 'aboutus.html')

@login_required
def resolver_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(Ensayo, id=ensayo_id)
    
    if request.method == 'POST':
        respuestas = []
        correctas = 0
        total = ensayo.preguntas.count()
        
        resultado = RespuestaEnsayo.objects.create(estudiante=request.user, ensayo=ensayo)

        for pregunta in ensayo.preguntas.all():
            respuesta = request.POST.get(f'pregunta_{pregunta.id}')
            rp = RespuestaPregunta.objects.create(
                respuesta_ensayo=resultado,
                pregunta=pregunta,
                alternativa_elegida=respuesta
            )
            if rp.es_correcta():
                correctas += 1

        resultado.puntaje = (correctas / total) * 100
        resultado.save()
        return redirect('ver_resultado', resultado.id)

    return render(request, 'resolver_ensayo.html', {'ensayo': ensayo})

@login_required
def ver_resultado(request, resultado_id):
    resultado = get_object_or_404(RespuestaEnsayo, id=resultado_id, estudiante=request.user)
    return render(request, 'ver_resultado.html', {'resultado': resultado})

@login_required
def mis_resultados_view(request):
    estudiante = request.user
    resultados = RespuestaEnsayo.objects.filter(estudiante=estudiante).select_related('ensayo').order_by('-fecha_respuesta')
    return render(request, 'resultados/mis_resultados.html', {'resultados': resultados})

@login_required
def detalle_resultado_view(request, resultado_id):
    resultado = get_object_or_404(RespuestaEnsayo, id=resultado_id, estudiante=request.user)
    respuestas = RespuestaPregunta.objects.filter(respuesta_ensayo=resultado).select_related('pregunta')

    detalle = []
    for r in respuestas:
        opciones = r.pregunta.opciones
        detalle.append({
            'pregunta': r.pregunta.enunciado,
            'respuesta_estudiante_letra': r.alternativa_elegida,
            'respuesta_estudiante_texto': opciones.get(r.alternativa_elegida, '') if r.alternativa_elegida else None,
            'respuesta_correcta_letra': r.pregunta.respuesta_correcta,
            'respuesta_correcta_texto': opciones.get(r.pregunta.respuesta_correcta, ''),
            'es_correcta': r.es_correcta(),
        })

    return render(request, 'resultados/detalle_resultado.html', {
        'resultado': resultado,
        'detalle': detalle,
    })

