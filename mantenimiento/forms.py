from django import forms
from django.core.exceptions import ValidationError
from .models import OrdenDeTrabajo, ConsumoSuministro
from django.contrib.auth.models import User
import datetime

class OrdenDeTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenDeTrabajo
        fields = ['titulo', 'descripcion_falla', 'prioridad']

    def clean_descripcion_falla(self):
        desc = self.cleaned_data['descripcion_falla']
        if len(desc) < 20:
            raise ValidationError("La descripción debe tener al menos 20 caracteres.")
        return desc

    def clean(self):
        cleaned_data = super().clean()
        prioridad = cleaned_data.get('prioridad')
        descripcion = cleaned_data.get('descripcion_falla', '').lower()
        if prioridad == 'Alta' and not any(p in descripcion for p in ['detenido', 'bloqueado', 'fuego']):
            raise ValidationError("Una orden de prioridad Alta debe contener una palabra de urgencia ('detenido', 'bloqueado', 'fuego').")
        return cleaned_data

class ConsumoSuministroForm(forms.ModelForm):
    class Meta:
        model = ConsumoSuministro
        fields = ['orden_de_trabajo', 'suministro', 'cantidad_usada']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['orden_de_trabajo'].queryset = OrdenDeTrabajo.objects.filter(
                operario_asignado=user, estado__in=['Pendiente', 'En Progreso']
            )

    def clean(self):
        cleaned_data = super().clean()
        suministro = cleaned_data.get('suministro')
        cantidad = cleaned_data.get('cantidad_usada')
        orden = cleaned_data.get('orden_de_trabajo')

        if suministro and cantidad:
            if cantidad > suministro.stock:
                raise ValidationError("La cantidad usada no puede superar el stock disponible.")

        if orden and orden.fecha_creacion > datetime.date.today():
            raise ValidationError("La fecha debe ser posterior a la de creación de la orden.")
        return cleaned_data

class AsignacionYEstadoForm(forms.ModelForm):
    class Meta:
        model = OrdenDeTrabajo
        fields = ['operario_asignado', 'estado', 'fecha_cierre_real']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['operario_asignado'].queryset = User.objects.filter(groups__name='Operario')

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        fecha_cierre = cleaned_data.get('fecha_cierre_real')

        if estado == 'Cerrada':
            if not fecha_cierre:
                raise ValidationError("Debe ingresar una fecha de cierre para cerrar la orden.")
            if fecha_cierre < self.instance.fecha_creacion:
                raise ValidationError("La fecha de cierre debe ser posterior a la creación.")
        return cleaned_data