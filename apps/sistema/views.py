from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse

from apps.proyecto.models import Proyecto
from apps.sistema.form import PerfilForm, EstudianteForm, DocenteForm
from apps.sistema.models import Estudiante, Docente, Perfil


# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
@permission_required('auth.add_user')
def signup(request):
    if request.method == 'POST':
        form_perfil = PerfilForm(request.POST, prefix='perfil')
        if form_perfil.is_valid():
            try:
                user = User.objects.create_user(username=request.POST['perfil-dni'], password=request.POST['perfil-dni'])
                user.save()

                perfil_instance = form_perfil.save(commit=False)
                perfil_instance.user = user
                perfil_instance.save()

                if request.POST['perfil-tipo_usuario'] == 'estudiante':
                    form_estudiante = EstudianteForm(request.POST, prefix='perfil')

                    estudiante_instance = form_estudiante.save(commit=False)
                    estudiante_instance.user = perfil_instance
                    estudiante_instance.save()

                    grupo_estudiantes, creado = Group.objects.get_or_create(name='Estudiantes')
                    user.groups.add(grupo_estudiantes)

                if request.POST['perfil-tipo_usuario'] == 'docente':
                    form_docente = DocenteForm(request.POST, prefix='perfil')

                    docente_instance = form_docente.save(commit=False)
                    docente_instance.user = perfil_instance
                    docente_instance.save()

                    grupo_docentes, creado = Group.objects.get_or_create(name='Docentes')
                    user.groups.add(grupo_docentes)

                if request.POST['perfil-tipo_usuario'] == 'comision':
                    grupo_comision, creado = Group.objects.get_or_create(name='Comisión')
                    user.groups.add(grupo_comision)

                messages.success(request, 'Se ha registrado el usuario correctamente.')
                return redirect(reverse('registrarme'))

            except:
                return render(request, 'registrar.html', {
                    'form': form_perfil,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'registrar.html', {
                'form': form_perfil,
                'error': 'Ingrese los datos correctamente'
            })
    else:
        form_perfil = PerfilForm(prefix='perfil')
        return render(request, 'registrar.html', {
            'form': form_perfil
        })


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('inicio')


@login_required
def usuario_lista(request):
    vista = ''
    perteneceTribunal = False # para saber si es un docente y pertenece al tribunal | etapa: evaluacion_tribunal
    perteneceProyecto = False # para saber si es un docente y pertenece al proyecto | etapa: borrador
    usuario = request.user
    tipo_usuario = ''

    if hasattr(usuario, 'perfil'):
        perfil = usuario.perfil
        tipo_usuario = perfil.tipo_usuario
    else:
        tipo_usuario = 'superadmin'

    if tipo_usuario=='superadmin' or tipo_usuario=='comision':
        usuarios = Perfil.objects.all()
        return render(request, 'usuariosLista.html', {
            'usuarios': usuarios,
        })
    else:
        if request.method == 'POST':
            print(request.POST)
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                print('es valido')
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'La contraseña fue cambiada con éxito.')
                return redirect('usuarios:lista')
            else:
                print('no valido')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'cambiar_contraseña.html', {'form': form})



@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


@login_required
def buscarEstudiante(request):
    proyecto = get_object_or_404(Proyecto, pk=request.GET['proyecto'])
    if 'q' in request.GET:
        query = request.GET ['q']
        estudiantes = Estudiante.objects.filter(
            Q(matricula__icontains=query) |
            Q(user__dni__icontains=query) |
            Q(user__nombre__icontains=query) |
            Q(user__apellido__icontains=query)
        )
    else:
        estudiantes = Estudiante.objects.all()
    return render(request, 'buscarEstudiantes.html', {
        'estudiantes': estudiantes,
        'proyecto': proyecto
    })


@login_required
def buscarDocente(request):
    proyecto = get_object_or_404(Proyecto, pk=request.GET['proyectoDocente'])
    if 'q' in request.GET:
        query = request.GET ['q']
        docentes = Docente.objects.filter(
            Q(cuil__icontains=query) |
            Q(user__dni__icontains=query) |
            Q(user__nombre__icontains=query) |
            Q(user__apellido__icontains=query)
        )
    else:
        docentes = Docente.objects.all()
    return render(request, 'buscarDocentes.html', {
        'docentes': docentes,
        'proyectoDocente': proyecto,
    })
