from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import OuterRef, Subquery, Max

from apps.movimiento.form import MovimientoForm, MovPresForm
from apps.movimiento.models import Movimiento
from apps.proyecto.form import ProyectoForm, ProyectoEstudianteForm, ProyectoDocenteForm
from apps.proyecto.models import Proyecto, ProyectoEstudiante, ProyectoDocente
from apps.sistema.models import Estudiante


# Create your views here.

@login_required
def proyecto_lista(request):
    movimientos = Movimiento.objects.values('proyecto').annotate(ultima_fecha=Max('fecha_hora')).distinct()
    movimientos_completos = Movimiento.objects.filter(
        proyecto__in=[movimiento['proyecto'] for movimiento in movimientos],
        fecha_hora__in=[movimiento['ultima_fecha'] for movimiento in movimientos]
    )
    return render(request, 'lista.html', {
        'proyectos': movimientos_completos,
    })

@login_required
def proyecto_lista_bad(request):
    ultimos_movimientos = Movimiento.objects.filter(
        proyecto=OuterRef('pk')
    ).order_by('-fecha_hora').values('fecha_hora')[:1]

    proyectos_con_ultimo_movimiento = Proyecto.objects.annotate(
        ultimo_movimiento_fecha=Subquery(ultimos_movimientos)
    )

    # Iterar sobre los proyectos y mostrar el último movimiento de cada uno
    for proyecto in proyectos_con_ultimo_movimiento:
        ultimo_movimiento = Movimiento.objects.filter(
            proyecto=proyecto,
            fecha_hora=proyecto.ultimo_movimiento_fecha
        ).first()
        print(f"Proyecto: {proyecto.titulo}, Último movimiento: {ultimo_movimiento}")

    return render(request, 'lista.html', {
                      'proyectos': proyectos_con_ultimo_movimiento,
                      })
    #proyectos = Proyecto.objects.annotate(ultima_fecha_hora=Max('movimiento__fecha_hora')).filter(movimiento__fecha_hora=F('ultima_fecha_hora'))
    #print(proyectos)
    #for proyecto in proyectos:
        #ultimo_movimiento = Movimiento.objects.filter(
            #proyecto=proyecto,
            #fecha_hora=proyecto.ultima_fecha_hora
        #).first()
        #print(f"Proyecto: {proyecto.titulo}, Último movimiento: {ultimo_movimiento.fecha_hora}")
    #return render(request, 'lista.html', {
        #'proyectos': proyectos,
    #})


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

            form_mov = MovimientoForm(request.POST, prefix='mov')
            movimiento_instance = form_mov.save(commit=False)
            movimiento_instance.proyecto = proyecto_instance
            movimiento_instance.etapa = 'presentacion'
            movimiento_instance.estado = 'pendiente'
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
    movimientos = Movimiento.objects.filter(proyecto_id=proy_id).order_by('-id')
    band = True
    actual = {}
    for mov in movimientos:
        if band:
            actual = {
                'get_etapa_display': mov.get_etapa_display,
                'get_estado_display': mov.get_estado_display,
                'etapa': mov.etapa,
                'estado': mov.estado,
            }
            band = False

    proy_estu = ProyectoEstudiante.objects.filter(proyecto_id=proy_id)
    estudiantes = Estudiante.objects.all()
    proy_docen = ProyectoDocente.objects.all()
    form_movimiento = MovPresForm(prefix='mov')
    return render(request, 'ver.html', {
        'proyecto': proyecto,
        'movimientos': movimientos,
        'proy_estu': proy_estu,
        'estudiantes': estudiantes,
        'proy_docen': proy_docen,
        'form': form_movimiento,
        'actual': actual,
    })


