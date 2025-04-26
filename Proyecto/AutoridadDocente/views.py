from django.shortcuts import render

def index(request):
    return render(request, 'base_docente.html')

def home_docente(request):
    return render(request, 'home_docente.html')



def ensayos_view(request):
    return render(request, 'ensayos_docente.html')

def cuenta_view(request):
    return render(request, 'cuenta_docente.html')