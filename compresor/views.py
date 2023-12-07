import os
import zipfile
from django.http import FileResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *


def login_user(request):
    return render(request, 'login.html')


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
            return redirect('list_files')
        # Retorna un mensaje de que las contraseñas no coinciden
        return HttpResponse('Las contraseñas no coinciden')
    # Retorna la vista con el formulario para llenar
    return render(request, 'create_user.html', {'formulario': UsuarioForm})


def list_files(request):
    mensaje = None
    archivos = None
    # Si el formulario manda datos por POST
    if request.POST:
        archivos = []
        # RFC ingresado por el usuario
        rfc = request.POST.get('rfc')
        # Resultado de busqueda en BD
        facturas = Facturas.objects.filter(rfc=rfc).order_by('factura')
        # Si facturas == 0, mandar alerta de que no existen facturas
        if len(facturas) == 0:
            mensaje = "No existen facturas para este RFC"
        # Iterar sobre facturas
        for factura in facturas:
            # Agregar extenciones a archivos
            ruta_pdf = factura.RutaAppFact + '.pdf'
            ruta_xml = factura.RutaAppFact + '.xml'
            # Intento para agregar archivos a lista
            try:
                # Si la ruta completa pertenece a un archivo agragarlo a lista
                if os.path.isfile(ruta_pdf):
                    # Agregar factura a arreglo
                    archivos.append(factura)
                # Si la ruta no pertenece a un archivo, mandar alerta
                else:
                    mensaje = f"El archivo '{factura}' no existe en la ruta '{ruta_pdf}'"
                # Manejo de errores
            except OSError as e:
                mensaje = f"No se pudieron listar los archivos en la ruta '{ruta_pdf}': {str(e)}"
    # Retorna template, y si tiene archivos los manda también
    return render(request, 'lista.html', {'files': archivos, 'mensaje': mensaje})


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
