from django.shortcuts import render, redirect, get_object_or_404
from LoginRegister.models import Ensayo
from .models import Ensayo, Pregunta
from .forms import EnsayoForm, PreguntaForm
def index(request):
    return render(request, 'base_docente.html')

def home_docente(request):
    return render(request, 'home_docente.html')



def ensayos_view(request):
    ensayos = Ensayo.objects.all()
    return render(request, 'ensayos_docente.html', {'ensayos': ensayos})

def cuenta_view(request):
    return render(request, 'cuenta_docente.html')

def listar_ensayos(request):
    ensayos = Ensayo.objects.all()
    return render(request, 'ensayos/listar.html', {'ensayos': ensayos})

def crear_ensayo(request):
    if request.method == 'POST':
        form = EnsayoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_ensayos')
    else:
        form = EnsayoForm()
    return render(request, 'ensayos/formulario.html', {'form': form})

def editar_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(Ensayo, id=ensayo_id)
    if request.method == 'POST':
        form = EnsayoForm(request.POST, instance=ensayo)
        if form.is_valid():
            form.save()
            return redirect('listar_ensayos')
    else:
        form = EnsayoForm(instance=ensayo)
    return render(request, 'ensayos/formulario.html', {'form': form})

def eliminar_ensayo(request, ensayo_id):
    ensayo = get_object_or_404(Ensayo, id=ensayo_id)
    ensayo.delete()
    return redirect('listar_ensayos')

def listar_preguntas(request):
    preguntas = Pregunta.objects.all()
    return render(request, 'preguntas/listar.html', {'preguntas': preguntas})

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