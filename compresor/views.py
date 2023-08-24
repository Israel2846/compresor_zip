import os
import zipfile
from django.http import FileResponse
from django.shortcuts import render, HttpResponse

def list_files(request):
    files = None
    mensaje = None
    # Si el formulario manda datos por POST
    if request.POST:
        # RFC ingresado por el usuario
        rfc = request.POST.get('rfc')
        # Ruta de la carpeta de documentos
        folder_path = "C:/Users/siste/OneDrive/Escritorio/Excel"
        # Obtener una lista de archivos en la carpeta
        all_files = os.listdir(folder_path)
        # Filtrar solo los archivos que tengan el nombre del campo RFC
        files = [file for file in all_files if file.startswith(rfc)]
        # Si no se encuentran archivos, manda mensaje de error
        if len(files) == 0:
            mensaje = "No se encontraron facturas para este RFC"
        
    return render(request, 'lista.html', {'files': files, 'mensaje' : mensaje})

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
                file_path = os.path.join("C:/Users/siste/OneDrive/Escritorio/Excel", file)
                zipf.write(file_path, os.path.basename(file_path))

        # Respuesta de descarga de los archivos
        response = FileResponse(open(zip_filename, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    # Manejo de errores
    except Exception as e:
        response = HttpResponse(f'Error!!! {str(e)}')
    # Retornamos la respuesta
    return response