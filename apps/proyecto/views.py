from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from apps.proyecto.form import ProyectoForm, ProyectoEstudianteForm, ProyectoDocenteForm
from apps.proyecto.models import Proyecto


# Create your views here.

@login_required
def proyecto_lista(request):
    proyectos = Proyecto.objects.all().order_by('-id')
    return render(request, 'lista.html', {
        'proyectos': proyectos
    })


@login_required
def proyecto_nuevo(request):
    if request.method == 'POST':
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

        return render(request, 'nuevo.html', {
            'form': form_proyecto,
            'form_estud': form_estud,
            'form_director': form_director,
            'form_codirector': form_codirector,
            'form_asesor': form_asesor,
        })


def proyecto_ver(request, proy_id):
    proyecto = get_object_or_404(Proyecto, pk=proy_id)
    return render(request, 'ver.html', {
        'proyecto': proyecto
    })
