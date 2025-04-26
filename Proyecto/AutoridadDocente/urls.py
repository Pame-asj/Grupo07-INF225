from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_docente, name='docente_index'),
    path('cuenta_docente/', views.cuenta_view, name= 'cuenta_docente'),
    path('ensayos_docente/', views.ensayos_view, name= 'ensayos_docente'),
]