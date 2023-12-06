import os
import zipfile
from django.http import FileResponse
from django.shortcuts import render, HttpResponse
from .models import *


def list_files(request):
    mensaje = None
    archivos = None
    # Si el formulario manda datos por POST
    if request.POST:
        archivos = []
        # RFC ingresado por el usuario
        rfc = request.POST.get('rfc')
        # Resultado de busqueda en BD
        facturas = Facturas.objects.filter(rfc=rfc)
        # Si facturas == 0, mandar alerta de que no existen facturas
        if len(facturas) == 0:
            mensaje = "No existen facturas para este RFC"
        # Iterar sobre facturas
        for factura in facturas:
            # Agregar extenciones a archivos
            ruta_pdf = factura.RutaAppFact + '.pdf'
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
                file_path = os.path.join(
                    r'E:\AIFA\JAI040322QI\202311\01', file)
                zipf.write(file_path, os.path.basename(file_path))
        # Respuesta de descarga de los archivos
        response = FileResponse(open(zip_filename, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    # Manejo de errores
    except Exception as e:
        response = HttpResponse(f'Error!!! {str(e)}')
    # Retornamos la respuesta
    return response
