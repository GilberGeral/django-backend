from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib import admin
from mascotas.views import vista_home 
from django.shortcuts import render

def vista_home(request):
    return render(request, 'mascotas/index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista_home, name='home'),
    path('api/v1/', include('mascotas.urls')),

]