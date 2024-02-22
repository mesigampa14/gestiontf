from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

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

                if request.POST['perfil-tipo_usuario'] == 'docente':
                    form_docente = DocenteForm(request.POST, prefix='perfil')

                    docente_instance = form_docente.save(commit=False)
                    docente_instance.user = perfil_instance
                    docente_instance.save()

                return render(request, 'registrar.html', {
                        'message': 'Se ha agregado al estudiante correctamente.'
                    })

            except:
                print(form_perfil)
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


def usuario_lista(request):
    usuarios = Perfil.objects.all()
    return render(request, 'usuariosLista.html', {
        'usuarios': usuarios,
    })


def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


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
