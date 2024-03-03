from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models.functions import ExtractYear
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q, Count, F
from django.utils import timezone
from datetime import datetime

from apps.movimiento.form import MovimientoForm, MovPresForm
from apps.movimiento.models import Movimiento
from apps.proyecto.form import ProyectoForm, ProyectoEstudianteForm, ProyectoDocenteForm
from apps.proyecto.models import Proyecto, ProyectoEstudiante, ProyectoDocente
from apps.sistema.models import Estudiante, Docente
from apps.sistema.views import usuario_tipo
from apps.tribunal.models import Tribunal


# Create your views here.

@login_required
def proyecto_lista(request):
    usuario = request.user

    if hasattr(usuario, 'perfil'):
        perfil = usuario.perfil
        tipo_usuario = perfil.tipo_usuario
        if tipo_usuario == 'docente':
            proyectos = Proyecto.objects.filter(
                proyectodocente__docente__user__dni=perfil.dni,
                proyectoestudiante__activo=True
            ).order_by('-id')
        if tipo_usuario == 'estudiante':
            proyectos = Proyecto.objects.filter(
                proyectoestudiante__estudiante__user__dni=perfil.dni,
                proyectoestudiante__activo=True
            ).order_by('-id')
        if tipo_usuario == 'comision':
            proyectos = Proyecto.objects.all().order_by('-id')
    else:
        proyectos = Proyecto.objects.all().order_by('-id')

    if request.method == 'POST':
        buscar = request.POST.get('buscar', '')
        estado = request.POST.get('estado', '')
        fecha_inicio = request.POST.get('fecha_inicio', '')
        fecha_fin = request.POST.get('fecha_fin', '')

        if buscar:
            proyectos = proyectos.filter(titulo__icontains=buscar)

        if estado:
            proyectos = proyectos.filter(estado=estado)

        if fecha_inicio:
            proyectos = proyectos.filter(presentacion__gte=fecha_inicio)

        if fecha_fin:
            proyectos = proyectos.filter(presentacion__lte=fecha_fin)

    return render(request, 'proyectosLista.html', {
        'proyectos': proyectos,
    })

@login_required
def proyecto_reportes(request):
    año_actual = datetime.now().year

    # Consulta para contar proyectos iniciados por año
    proyectos_iniciados_por_año = Proyecto.objects.annotate(
        año_inicio=ExtractYear('presentacion')
    ).filter(
        año_inicio__lte=año_actual
    ).values('año_inicio').annotate(
        total_iniciados=Count('id')
    )

    # Consulta para contar proyectos terminados por año
    proyectos_terminados_por_año = Proyecto.objects.annotate(
        año_inicio=ExtractYear('presentacion'),
        año_fin=ExtractYear('defensa_fecha')
    ).filter(
        Q(año_fin__lte=año_actual) | Q(defensa_fecha=None)
    ).values('año_fin').annotate(
        total_terminados=Count('id')
    )

    # Consulta para contar proyectos iniciados y terminados en el mismo año
    proyectos_iniciados_y_terminados_mismo_año = Proyecto.objects.annotate(
        año_inicio=ExtractYear('presentacion'),
        año_fin=ExtractYear('defensa_fecha')
    ).filter(
        año_inicio=F('año_fin'),
        defensa_fecha__isnull=False
    ).values('año_inicio').annotate(
        total_iniciados_y_terminados=Count('id')
    )

    return render(request, 'proyectosReportes.html', {
        'reportes_iniciados': proyectos_iniciados_por_año,
        'reportes_finalizados': proyectos_terminados_por_año,
        'reportes_anual': proyectos_iniciados_y_terminados_mismo_año,
    })

@login_required
@permission_required('proyecto.add_proyecto')
def proyecto_nuevo(request):
    if request.method == 'POST':
        form_proyecto = ProyectoForm(request.POST, request.FILES, prefix='')

        if form_proyecto.is_valid():
            #proyecto_instance = form_proyecto.save()
            proyecto_instance = form_proyecto.save(commit=False)
            proyecto_instance.etapa = 'evaluacion_comision'
            proyecto_instance.estado = 'pendiente'
            proyecto_instance.save()

            form_mov = MovimientoForm(request.POST, prefix='mov')
            movimiento_instance = form_mov.save(commit=False)
            movimiento_instance.proyecto = proyecto_instance
            movimiento_instance.etapa = 'evaluacion_comision'
            movimiento_instance.estado = 'pendiente'
            movimiento_instance.save()

            messages.success(request, 'Se ha registrado el proyecto correctamente.')
            return redirect(reverse('proyecto:lista'))
        else:
            return render(request, 'nuevo.html', {
                'error': 'UPS! Algo no resultó como esperabamos',
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


@login_required
def proyecto_ver(request, proy_id):
    vista = ''
    perteneceTribunal = False # para saber si es un docente y pertenece al tribunal | etapa: evaluacion_tribunal
    perteneceProyecto = False # para saber si es un docente y pertenece al proyecto | etapa: borrador
    proyecto = get_object_or_404(Proyecto, pk=proy_id)
    usuario = request.user
    tipo_usuario = ''

    if hasattr(usuario, 'perfil'):
        perfil = usuario.perfil
        tipo_usuario = perfil.tipo_usuario
        if tipo_usuario == 'docente':
            tribunal_sel = Tribunal.objects.filter(
                Q(pk=proyecto.tribunal.id) &
                (Q(presidente__user__dni=perfil.dni)|
                Q(vocalTitular1__user__dni=perfil.dni)|
                Q(vocalTitular2__user__dni=perfil.dni)|
                Q(vocalSuplente1__user__dni=perfil.dni)|
                Q(vocalSuplente2__user__dni=perfil.dni))
            )

            if tribunal_sel:
                perteneceTribunal = True


            docente_sel = ProyectoDocente.objects.filter(
                docente__user__dni=perfil.dni, cargo='director'
            )
            if docente_sel:
                perteneceProyecto = True

    else:
        tipo_usuario = 'superadmin'

    movimientos = Movimiento.objects.filter(proyecto_id=proy_id).order_by('-id')
    band = True
    actual = {}
    for mov in movimientos:
        if band:
            color = ''
            if mov.estado == 'pendiente':
                color = 'primary'
            if mov.estado == 'observado':
                color = 'warning'
            if mov.estado == 'aceptado':
                color = 'success'
            if mov.estado == 'rechazado':
                color = 'danger'
            actual = {
                'get_etapa_display': mov.get_etapa_display,
                'get_estado_display': mov.get_estado_display,
                'etapa': mov.etapa,
                'estado': mov.estado,
                'color': color
            }
            if (tipo_usuario=='superadmin' or tipo_usuario=='comision') and mov.etapa=='evaluacion_comision' and (mov.estado=='pendiente' or mov.estado=='observado'):
                vista = 'comision'

            if (tipo_usuario=='superadmin' or tipo_usuario=='docente') and perteneceTribunal and mov.etapa=='evaluacion_tribunal' and (mov.estado=='pendiente' or mov.estado=='observado'):
                vista = 'tribunal'

            if (tipo_usuario=='superadmin' or tipo_usuario=='docente') and perteneceProyecto and mov.etapa=='borrador' and (mov.estado=='pendiente' or mov.estado=='observado'):
                vista = 'borrador'

            if (tipo_usuario=='superadmin' or tipo_usuario=='docente') and perteneceTribunal and mov.etapa=='evaluacion_borrador' and (mov.estado=='pendiente' or mov.estado=='observado'):
                vista = 'tribunal'

            if (tipo_usuario=='superadmin' or tipo_usuario=='comision') and mov.etapa=='defensa' and (mov.estado=='pendiente' or mov.estado=='observado'):
                vista = 'defensa'

            band = False

    proy_estu = ProyectoEstudiante.objects.filter(proyecto_id=proy_id)
    proy_docen = ProyectoDocente.objects.filter(proyecto_id=proy_id)
    form_movimiento = MovPresForm(prefix='mov')

    return render(request, 'ver.html', {
        'proyecto': proyecto,
        'movimientos': movimientos,
        'proy_estu': proy_estu,
        'proy_docen': proy_docen,
        'form': form_movimiento,
        'actual': actual,
        'tipo_usuario': tipo_usuario,
        'vista': vista,
    })


@login_required
def proyecto_addEstudiante(request):
    if request.method == 'POST':
        relacion = ProyectoEstudiante.objects.filter(proyecto=request.POST['proyecto'], estudiante=request.POST['estudiante'], activo=True)

        if relacion:
            messages.warning(request, 'El estudiante seleccionado ya se encuentra vinculado al proyecto.')
            return redirect(reverse('proyecto:ver', kwargs={'proy_id': request.POST['proyecto']}))
        else:
            proyecto = get_object_or_404(Proyecto, pk=request.POST['proyecto'])
            estudiante = get_object_or_404(Estudiante, pk=request.POST['estudiante'])

            form_estudiante = ProyectoEstudianteForm(request.POST)
            instance = form_estudiante.save(commit=False)
            instance.proyecto = proyecto
            instance.estudiante = estudiante
            instance.save()

            messages.success(request, 'Se ha vinculado el estudiante al proyecto correctamente.')
            return redirect(reverse('proyecto:ver', kwargs={'proy_id': proyecto.pk}))

    else:
        messages.error(request, 'Se ha producido un error.')
        return redirect(reverse('proyecto:lista'))


@login_required
def proyecto_delEstudiante(request):
    if request.method == 'POST':
        relacion = get_object_or_404(ProyectoEstudiante, proyecto=request.POST['proyecto'], estudiante=request.POST['estudiante'], activo=True)

        if relacion:
            hora_actual = timezone.now()
            relacion.activo = False
            relacion.fecha_baja = hora_actual
            relacion.save()

            messages.success(request, 'Se ha desvinculado el estudiante al proyecto correctamente.')
            return redirect(reverse('proyecto:ver', kwargs={'proy_id': request.POST['proyecto']}))
        else:
            messages.warning(request, 'El estudiante seleccionado no se encuentra vinculado al proyecto.')
            return redirect(reverse('proyecto:ver', kwargs={'proy_id': request.POST['proyecto']}))
    else:
        messages.error(request, 'Se ha producido un error.')
        return redirect(reverse('proyecto:lista'))


@login_required
def proyecto_addDocente(request):
    if request.method == 'POST':
        relacion = ProyectoDocente.objects.filter(proyecto=request.POST['proyecto'], docente=request.POST['docente'], activo=True)
        relacion = ProyectoDocente.objects.filter(
            Q(proyecto=request.POST['proyecto'], docente=request.POST['docente'], activo=True) |
            Q(proyecto=request.POST['proyecto'], cargo=request.POST['cargo'], activo=True)
        )

        if relacion:
            messages.warning(request, 'No es posible vincular el docente con ese cargo al proyecto.')
            return redirect(reverse('proyecto:ver', kwargs={'proy_id': request.POST['proyecto']}))
        else:
            proyecto = get_object_or_404(Proyecto, pk=request.POST['proyecto'])
            docente = get_object_or_404(Docente, pk=request.POST['docente'])

            form_docente = ProyectoDocenteForm(request.POST)
            instance = form_docente.save(commit=False)
            instance.proyecto = proyecto
            instance.docente = docente
            instance.cargo = request.POST['cargo']
            instance.save()

            messages.success(request, 'Se ha vinculado el docente al proyecto correctamente.')
            return redirect(reverse('proyecto:ver', kwargs={'proy_id': proyecto.pk}))
    else:
        messages.error(request, 'Se ha producido un error.')
        return redirect(reverse('proyecto:lista'))


@login_required
def proyecto_delDocente(request):
    if request.method == 'POST':
        relacion = get_object_or_404(ProyectoDocente, proyecto=request.POST['proyecto'], docente=request.POST['docente'], activo=True)

        if relacion:
            hora_actual = timezone.now()
            relacion.activo = False
            relacion.fecha_baja = hora_actual
            relacion.save()

            messages.success(request, 'Se ha desvinculado el docente del proyecto correctamente.')
            return redirect(reverse('proyecto:ver', kwargs={'proy_id': request.POST['proyecto']}))
        else:
            messages.warning(request, 'El docente seleccionado no se encuentra vinculado al proyecto.')
            return redirect(reverse('proyecto:ver', kwargs={'proy_id': request.POST['proyecto']}))
    else:
        messages.error(request, 'Se ha producido un error.')
        return redirect(reverse('proyecto:lista'))


@login_required
def proyecto_addTribunal(request):
    if request.method == 'POST':
        proyecto = get_object_or_404(Proyecto, pk=request.POST['proyecto'])
        tribunal = get_object_or_404(Tribunal, pk=request.POST['tribunal'])

        proyecto.tribunal = tribunal
        proyecto.save()

        messages.success(request, 'Se ha vinculado el tribunal al proyecto correctamente.')
        return redirect(reverse('proyecto:ver', kwargs={'proy_id': proyecto.pk}))

    else:
        messages.error(request, 'Se ha producido un error.')
        return redirect(reverse('proyecto:lista'))

@login_required
def archivo_proy(request, proy_id):
    proyecto = Proyecto.objects.get(pk=proy_id)
    response = HttpResponse (proyecto.archivos, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{proyecto.archivos.name}"'
    return response

@login_required
def borrador_proy(request, proy_id):
    proyecto = Proyecto.objects.get(pk=proy_id)
    response = HttpResponse (proyecto.borrador, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{proyecto.borrador.name}"'
    return response
