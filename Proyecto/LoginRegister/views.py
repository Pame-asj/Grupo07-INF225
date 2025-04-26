from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(username=username, password=password)
            if user.role == 'Estudiante':
                return redirect('estudiante_index')  
            elif user.role == 'AutoridadDocente':
                return redirect('docente_index') 
        except User.DoesNotExist:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return render(request, 'login.html')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        nivel = request.POST.get('nivel')

        # Validación de datos únicos
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return render(request, 'register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está registrado.')
            return render(request, 'register.html')

        # Crear y guardar el usuario
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            username=username,
            password=password,
            role=role,
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
