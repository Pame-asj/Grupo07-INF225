from django.shortcuts import render

def index(request):
    return render(request, 'base_estudiante.html')

def home_estudiante(request):
    return render(request, 'home_estudiante.html')



def ensayos_view(request):
    return render(request, 'ensayos.html')

def cuenta_view(request):
    return render(request, 'cuenta.html')

def aboutus_view(request):
    return render(request, 'aboutus.html')