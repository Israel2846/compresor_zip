from django.urls import path
from . import views

urlpatterns = [
    path('tiempo', views.index, name='Index'),
    path('', views.lista, name='Lista'),
]
