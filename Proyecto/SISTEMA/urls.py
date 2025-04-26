from django.contrib import admin
from django.urls import path, include
from LoginRegister import views as LoginRegister_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginRegister_views.login, name='home'), 
    path('login/', LoginRegister_views.login, name='login'),
    path('register/', LoginRegister_views.register, name='register'),
    path('estudiante/', include('Estudiante.urls')),
    path('docente/', include('AutoridadDocente.urls')),
]