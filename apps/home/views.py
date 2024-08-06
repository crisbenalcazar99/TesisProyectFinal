# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64
import json
import os
import time
from datetime import datetime
from PIL import Image
from io import BytesIO

from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from IA_Bees.IA_Bees_Detector import FunctionRecognize
from apps.home.decorators import basic_auth_required
from apps.home.models import RegistroTemperatura, RegistroImagen



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@csrf_exempt
@basic_auth_required
def registrar_datos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperatura = data.get('temperatura')
            humedad = data.get('humedad')

            registro = RegistroTemperatura.objects.create(
                temperatura=temperatura,
                humedad=humedad
            )
            return JsonResponse({'message': 'Datos registrados correctamente', 'id': registro.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
@basic_auth_required
def registrar_imagen(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            imagen_base_64 = data.get('imagen_base_64')

            if imagen_base_64:
                # Decodificar la imagen base64
                imagen_data = base64.b64decode(imagen_base_64)

                # Crea un objeto BytesIO a partir de los datos decodificados
                image_stream = BytesIO(imagen_data)

                # Abre la imagen con PIL
                image = Image.open(image_stream)

                # Crear un nombre de archivo único basado en la fecha y hora actual
                fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")  # Formato: YYYYMMDD_HHMMSS
                filename = f"imagen_{fecha_actual}.png"

                # Definir la ruta donde se guardará la imagen
                images_dir = os.path.join(settings.MEDIA_ROOT, 'Images')
                if not os.path.exists(images_dir):
                    os.makedirs(images_dir)

                filepath = os.path.join(images_dir, filename)
                image.save(filepath, format='PNG')

                registro = RegistroImagen.objects.create(
                    url=filepath,
                    contiene_varroa=False
                )

                functionRecognize = FunctionRecognize(image)
                functionRecognize.bee_detection()

                return JsonResponse({'message': 'Imagen guardada con éxito.', 'filename': filename}, status=200)
            else:
                return JsonResponse({'error': 'No se proporcionó una imagen.'}, status=400)

        except Exception as e:
            return JsonResponse({'errorException': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
@basic_auth_required
def registrar_ubicacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitud = data.get('latitud')
            longitud = data.get('longitud')

            registro = RegistroTemperatura.objects.create(
                latitud=latitud,
                longitud=longitud
            )
            return JsonResponse({'message': 'Datos Ubicacion registrados correctamente', 'id': registro.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


#@csrf_exempt
#@basic_auth_required
def get_temperature_data(request):
    if request.method == 'GET':
        try:
            hoy = timezone.now().date()
            data = RegistroTemperatura.objects.filter(fecha_registro__date=hoy).order_by('fecha_registro')

            labels = [entry.fecha_registro.strftime("%H:%M") for entry in data]
            temperatures = [entry.temperatura for entry in data]
            humidities = [entry.humedad for entry in data]

            return JsonResponse({
                'labels': labels,
                'temperatures': temperatures,
                'humidities': humidities,
            }, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
