import os
import zipfile
from django.http import FileResponse, Http404
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from .models import *
from .forms import *


def login_user(request):
    mensaje = None
    # Si la petición viene por POST
    if request.POST:
        # Credenciales desde el formulario
        email = request.POST['email']
        password = request.POST['password']
        # Intento de autenticación
        try:
            usuario = authenticate(request, email=email, password=password)
            # Si existe el usuario
            if usuario is not None:
                # Creación de variables de sesión
                login(request, usuario)
                # Envío a página principal
                return redirect('list_files')
            # Si no existe el usuario
            else:
                mensaje = 'Credenciales incorrectas'
        # Manejo de errores
        except Exception as e:
            mensaje = str(e)
    # Retorna la vista con el formulario
    return render(request, 'usuarios/login.html', {'form': LoginForm, 'mensaje': mensaje})


def logout_user(request):
    logout(request)
    return redirect('login')


def create_user(request):
    # Si viene por metodo post
    if request.POST:
        # Si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            # Crear el usuario
            Usuario.objects.create_user(
                nombres_usuario=request.POST['nombres_usuario'],
                appat_usuario=request.POST['appat_usuario'],
                apmat_usuario=request.POST['apmat_usuario'],
                num_tel=request.POST['num_tel'],
                email=request.POST['email'],
                password=request.POST['password1']
            )
            # Retorna a la página de busqueda de rfc
            return redirect('login')
        # Retorna un mensaje de que las contraseñas no coinciden
        return HttpResponse('Las contraseñas no coinciden')
    # Retorna la vista con el formulario para llenar
    return render(request, 'usuarios/create_user.html', {'formulario': UsuarioForm})


def list_files(request):
    mensaje = None
    archivos = None
    pagina = request.GET.get('page', 1)
    # Si el formulario manda datos por POST
    if request.POST:
        # RFC ingresado por el usuario
        rfc = request.POST.get('rfc')
        # Resultado de busqueda en BD
        archivos = Facturas.objects.filter(rfc=rfc).order_by('factura')
        # Si facturas == 0, mandar alerta de que no existen facturas
        if len(archivos) == 0:
            mensaje = "No existen facturas para este RFC"
        else:
            # Filtrar las rutas que son archivos
            archivos = [factura for factura in archivos if os.path.isfile(
                factura.RutaAppFact + '.pdf')]
        # Paginación
        try:
            paginator = Paginator(archivos, 6)
            archivos = paginator.page(pagina)
        except:
            raise Http404
    # Retorna template, y si tiene archivos los manda también
    return render(request, 'facturas/lista.html', {'entity': archivos, 'mensaje': mensaje})


def compress_files(request):
    # Archivos recibidos del formulario
    selected_files = request.POST.getlist('selected_files')
    # Nombre del archivo como se guardará
    zip_filename = "compressed_files.zip"
    # Intento de procesamiento de datos
    try:
        # Proceso de compresión de archivos
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in selected_files:
                file_path = file
                zipf.write(file_path, os.path.basename(file))
        # Respuesta de descarga de los archivos
        response = FileResponse(open(zip_filename, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    # Manejo de errores
    except Exception as e:
        response = HttpResponse(f'Error!!! {str(e)}')
    # Retornamos la respuesta
    return response
