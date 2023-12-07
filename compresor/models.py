from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, nombres_usuario, appat_usuario, apmat_usuario, num_tel, email, password=None):

        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            nombres_usuario=nombres_usuario,
            appat_usuario=appat_usuario,
            apmat_usuario=apmat_usuario,            
            num_tel=num_tel,
            email=self.normalize_email(email),
        )

        usuario.set_password(password)
        usuario.save()

        return usuario

    def create_superuser(self, nombres_usuario, appat_usuario, apmat_usuario, num_tel, email, password):

        usuario = self.create_user(
            nombres_usuario=nombres_usuario,
            appat_usuario=appat_usuario,
            apmat_usuario=apmat_usuario,            
            num_tel=num_tel,
            email=email,
            password=password,
        )

        usuario.usuario_administrador = True
        usuario.save()

        return usuario


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

    def __str__(self):
        return f'Usuario: {self.nombres_usuario} {self.appat_usuario} {self.apmat_usuario}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador


class Facturas(models.Model):
    almacen = models.CharField(_("Almacen"), max_length=50)
    factura = models.CharField(_("Factura"), max_length=50)
    serie = models.CharField(_("Serie"), max_length=1)
    rfc = models.CharField(_("RFC"), max_length=14)
    UUID = models.TextField(_("UUID"))
    FechaDeTimbrado = models.CharField(_("Fecha de timbrado"), max_length=500)
    RutaProduccion = models.CharField(_("Ruta Producción"), max_length=500)
    RutaAppFact = models.CharField(_("RutaAppFact"), max_length=500)

    def __str__(self) -> str:
        return self.factura + '_' + self.serie
