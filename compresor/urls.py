from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_files, name='list_files'),
    path('compress/', views.compress_files, name='compress_files'),
]
