from django.contrib import admin
from django.urls import path, include  # Asegúrate de que 'include' esté aquí
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Esta es la línea clave que faltaba:
    path('', include('mantenimiento.urls')), 
]