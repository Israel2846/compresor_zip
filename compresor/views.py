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
        rutas_facturas = Facturas.objects.filter(rfc=rfc)
        # Si rutas_facturas == 0, mandar alerta de que no existen facturas
        if len(rutas_facturas) == 0:
            mensaje = "No existen facturas para este RFC"
        # Iterar sobre rutas
        for ruta_factura in rutas_facturas:
            # Agregar extenciones a archivos
            ruta_pdf = ruta_factura.RutaAppFact + '.pdf'
            ruta_xml = ruta_factura.RutaAppFact + '.xml'
            # Solo el nombre de los archivos
            nombre_archivo_pdf = os.path.basename(ruta_pdf)
            nombre_archivo_xml = os.path.basename(ruta_xml)
            # Intento para agregar archivos a lista
            try:
                # Si la ruta completa pertenece a un archivo agragarlo a lista
                if os.path.isfile(ruta_pdf):
                    archivos.append(nombre_archivo_pdf)
                    archivos.append(nombre_archivo_xml)
                # Si la ruta no pertenece a un archivo, mandar alerta
                else:
                    mensaje = f"El archivo '{nombre_archivo_pdf}' no existe en la ruta '{ruta_pdf}'"
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
