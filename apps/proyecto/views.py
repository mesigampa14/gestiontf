from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from apps.proyecto.form import ProyectoForm
from apps.proyecto.models import Proyecto


# Create your views here.

@login_required
def proyecto_lista(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'lista.html', {
        'proyectos': proyectos
    })


@login_required
def proyecto_nuevo(request):
    if request.method == 'POST':
        form_proyecto = ProyectoForm(request.POST, request.FILES, prefix='')

        if form_proyecto.is_valid():
            form_proyecto.save()

            messages.success(request, 'Se ha registrado el proyecto correctamente.')
            return redirect(reverse('proyecto:lista'))
        else:
            return render(request, 'nuevo.html', {
                'error': 'UPS! Algo no resultó como esperabamos'
            })
    else:
        form_proyecto = ProyectoForm(prefix='')

        return render(request, 'nuevo.html', {
            'form': form_proyecto,
        })


def proyecto_ver(request, proy_id):
    proyecto = get_object_or_404(Proyecto, pk=proy_id)
    return render(request, 'ver.html', {
        'proyecto': proyecto
    })
