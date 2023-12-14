from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('create_user', views.create_user, name='create_user'),
    path('list_files', views.list_files, name='list_files'),
    path('compress', views.compress_files, name='compress_files'),
    path('get_data_production', views.get_data_production, name='get_data_production'),
]
