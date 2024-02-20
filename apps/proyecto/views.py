from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from apps.movimiento.form import MovimientoForm
from apps.movimiento.models import Movimiento
from apps.proyecto.form import ProyectoForm, ProyectoEstudianteForm, ProyectoDocenteForm
from apps.proyecto.models import Proyecto


# Create your views here.

@login_required
def proyecto_lista(request):
    movimientos = Movimiento.objects.all().order_by('-id')
    return render(request, 'lista.html', {
        'movimientos': movimientos,
    })


@login_required
def proyecto_nuevo(request):
    if request.method == 'POST':
        print(request.POST)
        form_proyecto = ProyectoForm(request.POST, request.FILES, prefix='')

        if form_proyecto.is_valid():
            proyecto_instance = form_proyecto.save()

            form_estudiante = ProyectoEstudianteForm(request.POST)
            estudiante_instance = form_estudiante.save(commit=False)
            estudiante_instance.proyecto = proyecto_instance
            estudiante_instance.save()

            form_docente = ProyectoDocenteForm(request.POST, prefix='director')
            docente_instance = form_docente.save(commit=False)
            docente_instance.proyecto = proyecto_instance
            docente_instance.cargo = 'director'
            docente_instance.save()

            form_docente = ProyectoDocenteForm(request.POST, prefix='codirector')
            docente_instance = form_docente.save(commit=False)
            docente_instance.proyecto = proyecto_instance
            docente_instance.cargo = 'co_director'
            docente_instance.save()

            form_docente = ProyectoDocenteForm(request.POST, prefix='asesor')
            docente_instance = form_docente.save(commit=False)
            docente_instance.proyecto = proyecto_instance
            docente_instance.cargo = 'asesor'
            docente_instance.save()

            form_mov = MovimientoForm(request.POST, prefix='mov')
            print(form_mov)
            movimiento_instance = form_mov.save(commit=False)
            movimiento_instance.proyecto = proyecto_instance
            movimiento_instance.etapa = 'presentacion'
            movimiento_instance.estado = 'pendiente'
            print(movimiento_instance)
            movimiento_instance.save()

            messages.success(request, 'Se ha registrado el proyecto correctamente.')
            return redirect(reverse('proyecto:lista'))
        else:
            return render(request, 'nuevo.html', {
                'error': 'UPS! Algo no resultó como esperabamos'
            })
    else:
        form_proyecto = ProyectoForm(prefix='')
        form_estud = ProyectoEstudianteForm(prefix='')
        form_director = ProyectoDocenteForm(prefix='director')
        form_codirector = ProyectoDocenteForm(prefix='codirector')
        form_asesor = ProyectoDocenteForm(prefix='asesor')
        form_movimiento = MovimientoForm(prefix='mov')

        return render(request, 'nuevo.html', {
            'form': form_proyecto,
            'form_estud': form_estud,
            'form_director': form_director,
            'form_codirector': form_codirector,
            'form_asesor': form_asesor,
            'form_mov': form_movimiento,
        })


def proyecto_ver(request, proy_id):
    proyecto = get_object_or_404(Proyecto, pk=proy_id)
    print(proyecto)
    return render(request, 'ver.html', {
        'proyecto': proyecto
    })
