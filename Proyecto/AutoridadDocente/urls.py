from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_docente, name='docente_index'),
    path('cuenta_docente/', views.cuentadoc_view, name= 'cuenta_docente'),
    path('ensayos_docente/', views.ensayos_view, name='ensayos_docente'),
    path('ensayos_docente/crear/', views.crear_ensayo, name='crear_ensayo'),
    path('ensayos_docente/editar/<int:ensayo_id>/', views.editar_ensayo, name='editar_ensayo'),
    path('ensayos/', views.listar_ensayos, name='listar_ensayos'),
    path('ensayos/crear/', views.crear_ensayo, name='crear_ensayo'),
    path('ensayos/editar/<int:ensayo_id>/', views.editar_ensayo, name='editar_ensayo'),
    path('ensayos/eliminar/<int:ensayo_id>/', views.eliminar_ensayo, name='eliminar_ensayo'),
    path('preguntas/', views.listar_preguntas, name='listar_preguntas'),
    path('preguntas/crear/', views.crear_pregunta, name='crear_pregunta'),
    path('preguntas/editar/<int:pregunta_id>/', views.editar_pregunta, name='editar_pregunta'),
    path('preguntas/eliminar/<int:pregunta_id>/', views.eliminar_pregunta, name='eliminar_pregunta'),
    path('resultados/', views.resultados_ensayos_docente, name='resultados_docente'),
]