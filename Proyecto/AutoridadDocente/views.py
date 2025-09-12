from django.shortcuts import render, redirect, get_object_or_404
from LoginRegister.models import Ensayo
from .models import Ensayo, Pregunta, Tema, Tag
from .forms import EnsayoForm, PreguntaForm, TemaForm, TagForm
from AutoridadDocente.models import RespuestaEnsayo
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request, 'base_docente.html')

def home_docente(request):
    return render(request, 'home_docente.html')



def ensayos_view(request):
    ensayos = Ensayo.objects.all()
    return render(request, 'ensayos_docente.html', {'ensayos': ensayos})

def cuentadoc_view(request):
    return render(request, 'cuenta_docente.html')

def listar_ensayos(request):
    ensayos = Ensayo.objects.all()
    return render(request, 'ensayos/listar.html', {'ensayos': ensayos})

def crear_tema(request):
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_preguntas')  # redirige a un nombre de URL que sí existe
    else:
        form = TemaForm()
    return render(request, 'crear_tema.html', {'form': form})

def crear_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_preguntas')
    else:
        form = TagForm()
    return render(request, 'crear_tag.html', {'form': form})

def crear_ensayo(request):
    if request.method == 'POST':
        form = EnsayoForm(request.POST)
        if form.is_valid():
            ensayo = form.save(commit=False)
            ensayo.save()
            
            # Manejar nuevo tema
            nuevo_tema_nombre = form.cleaned_data.get('nuevo_tema')
            if nuevo_tema_nombre:
                nuevo_tema, created = Tema.objects.get_or_create(nombre=nuevo_tema_nombre)
                ensayo.temas.add(nuevo_tema)
            
            form.save_m2m()  # Para guardar relaciones many-to-many
            return redirect('listar_ensayos')
    else:
        form = EnsayoForm()
    return render(request, 'ensayos/formulario.html', {'form': form})

def editar_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(Ensayo, id=ensayo_id)
    if request.method == 'POST':
        form = EnsayoForm(request.POST, instance=ensayo)
        if form.is_valid():
            ensayo = form.save(commit=False)
            ensayo.save()
            
            nuevo_tema_nombre = form.cleaned_data.get('nuevo_tema')
            if nuevo_tema_nombre:
                nuevo_tema, created = Tema.objects.get_or_create(nombre=nuevo_tema_nombre)
                ensayo.temas.add(nuevo_tema)
            
            form.save_m2m()
            return redirect('listar_ensayos')
    else:
        form = EnsayoForm(instance=ensayo)
    return render(request, 'ensayos/formulario.html', {'form': form})

def eliminar_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(Ensayo, id=ensayo_id)
    ensayo.delete()
    return redirect('listar_ensayos')

def listar_preguntas(request):
    solo_libres = request.GET.get('libres') == '1'
    preguntas = Pregunta.objects.all().prefetch_related('temas')
    if solo_libres and hasattr(Pregunta, 'is_free'):
        preguntas = preguntas.filter(is_free=True)

    context = {
        'preguntas': preguntas,
        'solo_libres': solo_libres,
    }
    return render(request, 'preguntas/listar.html', context)

def crear_pregunta(request):
    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_preguntas')
    else:
        form = PreguntaForm()
    return render(request, 'preguntas/formulario.html', {'form': form})

def editar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    if request.method == 'POST':
        form = PreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            return redirect('listar_preguntas')
    else:
        form = PreguntaForm(instance=pregunta)
    return render(request, 'preguntas/formulario.html', {'form': form})

def eliminar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    pregunta.delete()
    return redirect('listar_preguntas')

@login_required
def resultados_ensayos_docente(request):
    if request.user.role != 'AutoridadDocente':
        return redirect('login')

    resultados = RespuestaEnsayo.objects.select_related('estudiante', 'ensayo').order_by('-fecha_respuesta')
    return render(request, 'resultados/resultados_docente.html', {'resultados': resultados})