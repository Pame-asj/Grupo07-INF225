from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_estudiante, name='estudiante_index'),
    path('ensayos/', views.ensayos_view, name= 'ensayos'),
    path('cuenta/', views.cuenta_view, name='cuenta_estudiante'),
    path('aboutus/', views.aboutus_view, name= 'aboutus'),
    path('ensayos/<int:ensayo_id>/resolver/', views.resolver_ensayo, name='resolver_ensayo'),
    path('ensayos/resultados/<int:resultado_id>/', views.ver_resultado, name='ver_resultado'),
    path('resultados/', views.mis_resultados_view, name='mis_resultados'),
    path('resultados/mis_resultados/<int:resultado_id>/', views.detalle_resultado_view, name='detalle_resultado'),

]