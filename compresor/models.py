from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    # Función Crear Usuario
    def create_user(self, nombres_usuario, appat_usuario, apmat_usuario, num_tel, email, password=None):
        # Validación si es que no tiene email
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        # Creación del usuario
        usuario = self.model(
            nombres_usuario=nombres_usuario,
            appat_usuario=appat_usuario,
            apmat_usuario=apmat_usuario,
            num_tel=num_tel,
            email=self.normalize_email(email),
        )
        # Se ingresa la contraseña y se guarda
        usuario.set_password(password)
        usuario.save()
        # Se retorna el usuario creado
        return usuario

    # Función para crear SuperUsuario
    def create_superuser(self, nombres_usuario, appat_usuario, apmat_usuario, num_tel, email, password):
        # Creación de SuperUsuario
        usuario = self.create_user(
            nombres_usuario=nombres_usuario,
            appat_usuario=appat_usuario,
            apmat_usuario=apmat_usuario,
            num_tel=num_tel,
            email=email,
            password=password,
        )
        # Asignación de valor para SuperUsuario
        usuario.usuario_administrador = True
        usuario.save()
        # Se retorma el SuperUsuario creado
        return usuario

# Modelo Usuario


class Usuario(AbstractBaseUser):
    nombres_usuario = models.CharField('Nombre(s)', max_length=200)
    appat_usuario = models.CharField('Apellido paterno', max_length=50)
    apmat_usuario = models.CharField('Apellido materno', max_length=50)
    num_tel = models.BigIntegerField('Número telefónico')
    email = models.EmailField('Correo electrónico',
                              unique=True, max_length=254)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres_usuario', 'appat_usuario',
                       'apmat_usuario', 'num_tel']

    # String para Usuario
    def __str__(self):
        return f'Usuario: {self.nombres_usuario} {self.appat_usuario} {self.apmat_usuario}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador


# Modelo Factura
class Factura(models.Model):
    almacen = models.CharField(_("Almacen"), max_length=50)
    factura = models.CharField(_("Factura"), max_length=50)
    serie = models.CharField(_("Serie"), max_length=1)
    rfc = models.CharField(_("RFC"), max_length=14)
    UUID = models.TextField(_("UUID"))
    fecha_timbrado = models.CharField(_("Fecha de timbrado"), max_length=500)
    ruta_produccion = models.TextField(_("Ruta producción"))
    ruta_app_fact = models.TextField(_("Ruta app"))

    # String para Factura
    def __str__(self) -> str:
        return self.factura + '_' + self.serie
