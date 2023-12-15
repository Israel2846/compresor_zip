import os
import zipfile
from django.http import FileResponse
from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
import pyodbc


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
    # Si el formulario manda datos por POST
    if request.POST:
        # Intento de obtener los datos del formulario
        try:
            # Datos ingresados por el usuario
            rfc = request.POST['rfc']
            fecha_inicio = datetime.strptime(
                request.POST['fecha_inicio'], '%Y-%m-%d')
            fecha_fin = datetime.strptime(
                request.POST['fecha_fin'], '%Y-%m-%d')
        # Error si algún dato no se puede recuperar del formulario
        except KeyError as e:
            return HttpResponse(str(e))
        # Resultado de busqueda en BD
        archivos = Factura.objects.filter(rfc=rfc).order_by('factura')
        # Si facturas == 0, mandar alerta de que no existen facturas
        if len(archivos) == 0:
            mensaje = "No existen facturas para este RFC"
        else:
            # Filtrar las rutas que son archivos
            archivos = [factura for factura in archivos if os.path.isfile(
                factura.ruta_app_fact + '.pdf') and (
                    datetime.strptime(factura.fecha_timbrado, '%Y-%m-%dT%H:%M:%S') >= fecha_inicio and datetime.strptime(factura.fecha_timbrado, '%Y-%m-%dT%H:%M:%S') <= fecha_fin)]
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
        response['Content-Disposition'] = f'attachment; filename="{
            zip_filename}"'
    # Manejo de errores
    except Exception as e:
        response = HttpResponse(f'Error!!! {str(e)}')
    # Retornamos la respuesta
    return response


# def get_data_production(request):
    # # Configuración de la conexión a la base de datos
    # config = {
    #     'user': 'root',
    #     'password': '',
    #     'host': 'localhost',
    #     'database': 'produccion',
    #     'raise_on_warnings': True,
    # }
    # # Intentar establecer la conexión
    # try:
    #     conn = mysql.connector.connect(**config)
    #     # Crear un cursor para ejecutar consultas SQL
    #     cursor = conn.cursor()
    #     # Llamada al Stored Procedure
    #     cursor.callproc("get_data", [3])
    #     # Obtener resultados del SP
    #     results = cursor.stored_results()
    #     # Recorrido de resultados
    #     for row in results:
    #         for item in row.fetchall():
    #             # Creación de objeto Factura para cada uno de los registros
    #             factura = Factura(
    #                 almacen=item[1],
    #                 factura=item[2],
    #                 serie=item[3],
    #                 rfc=item[4],
    #                 UUID=item[5],
    #                 fecha_timbrado=item[6],
    #                 ruta_produccion=item[7],
    #                 ruta_app_fact=item[8],
    #             )
    #             # Guardado de objeto factura
    #             factura.save()
    #         return HttpResponse(status=200)
    # # Manejo de errores
    # except mysql.connector.Error as err:
    #     print(f"Error: {err}")
    # # Finalización
    # finally:
    #     # Asegurarse de cerrar la conexión al final
    #     if 'conn' in locals() and conn.is_connected():
    #         cursor.close()
    #         conn.close()
    #         print("Conexión cerrada.")
    # Configuración de la conexión a la base de datos SQL Server

def get_data_production(request):
    # Configuración de la conexión a la base de datos SQL Server
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=192.168.40.115;'
        'DATABASE=cco_facturas;'
        'UID=sa;'
        'PWD=$ql@2023;'
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Aquí puedes ejecutar tus consultas SQL, por ejemplo:
        cursor.execute("EXEC get_data @id_p=?", 3)
        results = cursor.fetchall()
        for item in results:
            # Creación de objeto Factura para cada uno de los registros
            factura = Factura(
                almacen=item[1],
                factura=item[2],
                serie=item[3],
                rfc=item[4],
                UUID=item[5],
                fecha_timbrado=item[6],
                ruta_produccion=item[7],
                ruta_app_fact=item[8],
            )

            # Guardado de objeto factura
            factura.save()
            return HttpResponse(status=200)

    except pyodbc.Error as err:
        print(f"Error de conexión: {err}")
        return HttpResponse(status=500)

    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()
            print("Conexión cerrada.")
