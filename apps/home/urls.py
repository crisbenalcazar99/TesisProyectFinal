# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import registrar_datos
from apps.home.views import get_temperature_data

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('registerData/', views.registrar_datos, name='registrar_datos'),
    path('registerImage/', views.registrar_imagen, name='registrar_imagen'),
    path('get-temperature-data/', views.get_temperature_data, name='get_temperature_data'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]