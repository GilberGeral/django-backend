from django.shortcuts import render
from .models import Mascota

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import crear_mascota
from .models import TipoMascota

def vista_home(request):
    return render(request, 'mascotas/index.html')

@api_view(['POST'])
def mascota_create(request):
    # Aqui validaciones de datos
    data = request.data

    errores = {}

    if not data.get('nombre') or data['nombre'].strip() == '':
        errores['nombre'] = 'El nombre es requerido.'

    try:
        edad = int(data.get('edadMeses', -1))
        if edad < 0:
            errores['edadMeses'] = 'Edad debe ser un número positivo.'
    except (ValueError, TypeError):
        errores['edadMeses'] = 'Edad debe ser un número válido.'

    tipos_validos = {1,2,3,4}
    if not isinstance(data.get('tipo'), int) or data.get('tipo') not in tipos_validos:
        errores['tipo'] = 'Tipo de mascota inválido.'

    if errores:
        return Response({'errores': errores}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        mascota = crear_mascota(request.data)
        return Response({'id': mascota.id, 'mensaje': 'Mascota creada'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
# 'tipo': m.tipo.id,
@api_view(['GET'])
def mascota_list_all(request):
    mascotas = Mascota.objects.all()
    tipos = TipoMascota.objects.all().values('id', 'nombre')
    tipos_dict = {t['id']: t['nombre'] for t in tipos}
    resultado = []

    for m in mascotas:
        resultado.append({
            'id': m.id,
            'nombre': m.nombre,
            'edadMeses': m.edad_meses,
            'tipo': tipos_dict.get(m.tipo, 'Desconocido'),
            'tipoId': m.tipo
        })

    return Response(resultado, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def mascota_delete(request, id):
    if not isinstance(id, int) or id <= 0:
      return Response({'error': 'ID inválido. Debe ser un entero positivo.'}, status=status.HTTP_400_BAD_REQUEST)
    # return Response({'error': 'ID inválido. Debe ser un entero positivo.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        mascota = Mascota.objects.get(id=id)
        mascota.delete()
        return Response({'mensaje': f'Mascota con id {id} eliminada correctamente.'}, status=status.HTTP_200_OK)
    except Mascota.DoesNotExist:
        return Response({'error': 'Mascota no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def mascota_update(request, id):
    data = request.data
    errores = {}

    if not data.get('nombre') or data['nombre'].strip() == '':
        errores['nombre'] = 'El nombre es requerido.'

    try:
        edad = int(data.get('edadMeses', -1))
        if edad < 0:
            errores['edadMeses'] = 'Edad debe ser un número positivo.'
    except (ValueError, TypeError):
        errores['edadMeses'] = 'Edad debe ser un número válido.'

    if not data.get('tipoId'):
      errores['tipo'] = 'Tipo es necesario'

    tipos_validos = {1,2,3,4}
    if data.get('tipoId') not in tipos_validos:
      errores['tipo'] = 'Tipo de mascota inválido.'
        

    if errores:
        return Response({'errores': errores}, status=status.HTTP_400_BAD_REQUEST)

    try:
        mascota = Mascota.objects.get(id=id)
        mascota.nombre = data['nombre']
        mascota.edad_meses = edad
        mascota.tipo = data['tipoId']
        mascota.save()
        return Response({'mensaje': f'Mascota con id {id} actualizada correctamente.'}, status=status.HTTP_200_OK)
    except Mascota.DoesNotExist:
        return Response({'error': 'Mascota no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
