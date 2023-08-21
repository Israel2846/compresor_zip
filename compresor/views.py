from django.shortcuts import render, HttpResponse
import zipfile
from datetime import datetime
import os
from config.settings import BASE_DIR
from django.core.mail import EmailMessage
import io

# Create your views here.
def index(request):
    mensaje = None
    if request.POST:
        # Intento de manejo de datos
        try:
            static_archivos_path = os.path.join(BASE_DIR, 'compresor', 'static', 'archivos') #Carpeta donde llegará el archivo comprimido
            os.makedirs(static_archivos_path, exist_ok=True) #Si no existe la carpeta destino, se crea.
            folder_to_compress = 'C:/Users/siste/OneDrive/Escritorio/Documentos/Excel' #Carpeta a comprimir.
            zip_file_path = os.path.join(BASE_DIR, 'compresor', 'static', 'archivos', 'archivos.zip') # Direccion del archivo comprimido.
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
            fecha_fin_str = request.POST.get('fecha_fin')
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
            # Start compresión de archivos.
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for root, _, files in os.walk(folder_to_compress):
                    for archivo in files:
                        archivo_path = os.path.join(root, archivo)
                        fecha_creacion = datetime.fromtimestamp(os.path.getmtime(archivo_path))
                        print(fecha_creacion)
                        if fecha_creacion >= fecha_inicio and fecha_creacion <= fecha_fin:
                            zipf.write(archivo_path, os.path.relpath(archivo_path, folder_to_compress))
            # End compresión de archivos.
            return render(request, 'download.html')
        # Manejo de errores en caso de haber alguno.
        except Exception as e:
            mensaje = str(e)
    return render(request, 'index.html', {'mensaje': mensaje})



def lista(request):
    if request.method == 'POST' and request.FILES.getlist('archivos'):
        archivos_seleccionados = request.FILES.getlist('archivos')
        print (archivos_seleccionados)

        # Crear un archivo .zip en memoria
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for archivo in archivos_seleccionados:
                # Agregar cada archivo al archivo .zip
                nombre_archivo = archivo.name
                contenido_archivo = archivo.read()
                zipf.writestr(nombre_archivo, contenido_archivo)

        # Configurar la respuesta HTTP
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=archivos_comprimidos.zip'

        return response
    return render(request, 'lista.html')