from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import OrdenDeTrabajo, Suministro
# ¡IMPORTANTE! Asegúrate de que los formularios estén importados
from .forms import OrdenDeTrabajoForm, ConsumoSuministroForm, AsignacionYEstadoForm

@login_required
def orden_list(request):
    user = request.user
    if user.groups.filter(name='Operario').exists():
        ordenes = OrdenDeTrabajo.objects.filter(creador=user) | OrdenDeTrabajo.objects.filter(operario_asignado=user)
    else:
        ordenes = OrdenDeTrabajo.objects.all()

    # Guardar en sesión la última orden visualizada
    ultima = request.session.get('ultima_orden')
    return render(request, 'orden_list.html', {'ordenes': ordenes, 'ultima_orden': ultima})

@login_required
@permission_required('mantenimiento.add_ordendetrabajo', raise_exception=True)
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenDeTrabajoForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.creador = request.user
            orden.save()
            request.session['ultima_orden'] = orden.id
            messages.success(request, "Orden creada exitosamente.")
            return redirect('orden_list')
        else:
            messages.error(request, "Error al crear la orden.")
    else:
        form = OrdenDeTrabajoForm()
    return render(request, 'orden_form.html', {'form': form})

@login_required
@permission_required('mantenimiento.add_consumosuministro', raise_exception=True)
def registrar_consumo(request):
    if request.method == 'POST':
        form = ConsumoSuministroForm(request.POST, user=request.user)
        if form.is_valid():
            consumo = form.save()
            suministro = consumo.suministro
            suministro.stock -= consumo.cantidad_usada
            suministro.save()
            messages.success(request, "Consumo registrado correctamente.")
            return redirect('orden_list')
        else:
            messages.error(request, "Error en el registro del consumo.")
    else:
        form = ConsumoSuministroForm(user=request.user)
    return render(request, 'consumo_form.html', {'form': form})

@login_required
@permission_required('mantenimiento.change_ordendetrabajo', raise_exception=True)
def asignar_orden(request, id):
    orden = get_object_or_404(OrdenDeTrabajo, id=id)
    if request.method == 'POST':
        form = AsignacionYEstadoForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            messages.success(request, "Orden actualizada correctamente.")
            return redirect('orden_list')
        else:
            messages.error(request, "Error al actualizar la orden.")
    else:
        form = AsignacionYEstadoForm(instance=orden)
    return render(request, 'asignacion_form.html', {'form': form, 'orden': orden})