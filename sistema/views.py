from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from sistema.form import PerfilForm, EstudianteForm, DocenteForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def signup(request):
    form_perfil = PerfilForm(prefix='perfil')
    if request.method == 'GET':
        return render(request, 'registrar.html', {
            'form': form_perfil
        })
    else:
        form_perfil = PerfilForm(request.POST, prefix='perfil')
        if form_perfil.is_valid():
            try:
                user = User.objects.create_user(username=request.POST['perfil-dni'], password=request.POST['perfil-dni'])
                user.save()

                perfil_instance = form_perfil.save(commit=False)
                perfil_instance.user = user
                perfil_instance.save()

                # revisar que no se puede guardar el tamaño del cuil

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

                #messages.success(request, 'Se ha agregado al estudiante correctamente.')
                return redirect(request, 'registrar.html', {
                    'error': 'Se ha agregado al estudiante correctamente.'
                })
                #login(request, user)
                #return redirect('inicio')
            except:
                return render(request, 'registrar.html', {
                    'form': form_perfil,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'registrar.html', {
                'form': form_perfil,
                'error': 'algo ha pasao compadre'
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


def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
