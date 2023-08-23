import os
import zipfile
from django.http import FileResponse
from django.shortcuts import render

def list_files(request):
    # Ruta de la carpeta de documentos
    folder_path = "C:/Users/siste/OneDrive/Escritorio/Excel"
    
    # Obtener una lista de archivos en la carpeta
    files = os.listdir(folder_path)
    
    return render(request, 'lista.html', {'files': files})

def compress_files(request):
    # Archivos recibidos del formulario
    selected_files = request.POST.getlist('selected_files')
    # Nombre del archivo como se guardará
    zip_filename = "compressed_files.zip"

    # Proceso de compresión de archivos
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in selected_files:
            file_path = os.path.join("C:/Users/siste/OneDrive/Escritorio/Excel", file)
            zipf.write(file_path, os.path.basename(file_path))

    # Respuesta de descarga de los archivos
    response = FileResponse(open(zip_filename, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    return response