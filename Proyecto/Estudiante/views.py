from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from LoginRegister.models import Ensayo

def index(request):
    return render(request, 'base_estudiante.html')


def home_estudiante(request):
    return render(request, 'home_estudiante.html')


@login_required
def ensayos_view(request):
    estudiante = request.user
    ensayos = Ensayo.objects.filter(nivel=estudiante.nivel)

    return render(request, 'ensayos.html', {'ensayos': ensayos})

def cuenta_view(request):
    return render(request, 'cuenta.html')

def aboutus_view(request):
    return render(request, 'aboutus.html')