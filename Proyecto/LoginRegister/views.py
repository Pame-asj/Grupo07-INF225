from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'Estudiante':
            return redirect('estudiante_index')
        elif request.user.role == 'AutoridadDocente':
            return redirect('docente_index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  
            if user.role == 'Estudiante':
                return redirect('estudiante_index')
            elif user.role == 'AutoridadDocente':
                return redirect('docente_index')
        else:
            messages.error(request, 'Credenciales incorrectas.')
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        nivel = request.POST.get('nivel')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return render(request, 'register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está registrado.')
            return render(request, 'register.html')

        # Crear y guardar el usuario
        user = User.objects.create_user(
            full_name=full_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            username=username,
            password=password,
            role=role,
            #colegio = colegio,
            nivel=nivel,
        )
        user.save()
        messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'register.html')

def estudiante_index(request):
    return render(request, 'estudiante_index.html')

def docente_view(request):
    return render(request, 'docente.html')

def logout_view(request):
    logout(request)
    return redirect('login')  #Redirige al login luego de cerrar sesión
