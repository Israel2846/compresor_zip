from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('list_files', views.list_files, name='list_files'),
    path('compress', views.compress_files, name='compress_files'),
]
