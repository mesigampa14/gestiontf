from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import OuterRef, Subquery, Max
from django.utils import timezone
from django.contrib.auth.models import User

from apps.movimiento.form import MovimientoForm, MovPresForm
from apps.movimiento.models import Movimiento
from apps.proyecto.form import ProyectoForm, ProyectoEstudianteForm, ProyectoDocenteForm
from apps.proyecto.models import Proyecto, ProyectoEstudiante, ProyectoDocente
from apps.sistema.models import Estudiante, Docente, Perfil


# Create your views here.

@login_required
def proyecto_lista(request):
    proyectos = Proyecto.objects.all().order_by('-id')
    return render(request, 'proyectosLista.html', {
        'proyectos': proyectos,
    })

#@login_required
#def proyecto_lista(request):
    #movimientos = Movimiento.objects.values('proyecto').annotate(ultima_fecha=Max('fecha_hora')).distinct()
    #movimientos_completos = Movimiento.objects.filter(
        #proyecto__in=[movimiento['proyecto'] for movimiento in movimientos],
        #fecha_hora__in=[movimiento['ultima_fecha'] for movimiento in movimientos]
    #).order_by('-fecha_hora')
    #return render(request, 'proyectosLista.html', {
        #'proyectos': movimientos_completos,
    #})

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

    return render(request, 'proyectosLista.html', {
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
    #return render(request, 'proyectosLista.html', {
        #'proyectos': proyectos,
    #})


@login_required
@permission_required('prooyecto.add_proyecto')
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
            band = False

    proy_estu = ProyectoEstudiante.objects.filter(proyecto_id=proy_id)
    estudiantes = Estudiante.objects.all()
    proy_docen = ProyectoDocente.objects.filter(proyecto_id=proy_id)
    form_movimiento = MovPresForm(prefix='mov')

    usuario = request.user
    tipo_usuario = ''

    if hasattr(usuario, 'perfil'):
        perfil = usuario.perfil
        tipo_usuario = perfil.tipo_usuario
    else:
        tipo_usuario = 'superadmin'

    return render(request, 'ver.html', {
        'proyecto': proyecto,
        'movimientos': movimientos,
        'proy_estu': proy_estu,
        'estudiantes': estudiantes,
        'proy_docen': proy_docen,
        'form': form_movimiento,
        'actual': actual,
        'tipo_usuario': tipo_usuario
    })


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


def proyecto_addDocente(request):
    if request.method == 'POST':
        relacion = ProyectoDocente.objects.filter(proyecto=request.POST['proyecto'], docente=request.POST['docente'], activo=True)
        #ver tambien de no dejar guardar con el mismo cargo de otro docente

        if relacion:
            messages.warning(request, 'El docente seleccionado ya se encuentra vinculado al proyecto.')
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


def proyecto_delDocente(request):
    if request.method == 'POST':
        print(request.POST)
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


