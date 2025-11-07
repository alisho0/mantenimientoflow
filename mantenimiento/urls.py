from django.urls import path
from . import views

urlpatterns = [
    path('', views.orden_list, name='orden_list'),
    path('nueva/', views.crear_orden, name='crear_orden'),
    path('consumo/', views.registrar_consumo, name='registrar_consumo'),
    path('asignar/<int:id>/', views.asignar_orden, name='asignar_orden'),
    path('eliminar/<int:id>/', views.eliminar_orden, name='eliminar_orden'),
    path('suministros/', views.listar_suministros, name='listar_suministros'),
    path('suministros/nuevo/', views.crear_suministro, name='crear_suministro'),
    path('suministros/editar/<int:id>/', views.editar_suministro, name='editar_suministro'),
    path('suministros/eliminar/<int:id>/', views.eliminar_suministro, name='eliminar_suministro'),
]