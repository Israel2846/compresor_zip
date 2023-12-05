from django.db import models
from django.utils.translation import gettext as _


class Facturas(models.Model):
    almacen = models.CharField(_("Almacen"), max_length=50)
    factura = models.CharField(_("Factura"), max_length=50)
    serie = models.CharField(_("Serie"), max_length=1)
    rfc = models.CharField(_("RFC"), max_length=14)
    UUID = models.TextField(_("UUID"))
    FechaDeTimbrado = models.CharField(_("Fecha de timbrado"), max_length=500)
    RutaProduccion = models.CharField(_("Ruta Producción"), max_length=500)
    RutaAppFact = models.CharField(_("RutaAppFact"), max_length=500)

