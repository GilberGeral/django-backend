from .models import Mascota

def crear_mascota(data):
    mascota = Mascota.objects.create(
        nombre=data['nombre'],
        edad_meses=data['edadMeses'],
        tipo=data['tipo']
    )
    return mascota