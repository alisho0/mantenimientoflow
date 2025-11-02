from django.urls import path
from . import views

urlpatterns = [
    path('', views.orden_list, name='orden_list'),
    path('nueva/', views.crear_orden, name='crear_orden'),
    path('consumo/', views.registrar_consumo, name='registrar_consumo'),
    path('asignar/<int:id>/', views.asignar_orden, name='asignar_orden'),
]