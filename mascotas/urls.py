from django.urls import path
from . import views

urlpatterns = [    
    path('create', views.mascota_create, name='crear_mascota'),
    path('list_all', views.mascota_list_all, name='mascota_list_all'),
    path('delete/<int:id>/', views.mascota_delete, name='mascota_delete'),
    path('update/<int:id>/', views.mascota_update, name='mascota_update'),
]