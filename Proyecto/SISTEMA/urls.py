from django.contrib import admin
from django.urls import path, include
from LoginRegister import views as LoginRegister_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginRegister_views.login_view, name='home'),
    path('', include('LoginRegister.urls')), 
    path('login/', LoginRegister_views.login_view, name='login'),
    path('register/', LoginRegister_views.register_view, name='register'),
    path('estudiante/', include('Estudiante.urls')),
    path('docente/', include('AutoridadDocente.urls')),
]