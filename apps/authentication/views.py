# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64

from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
""""
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_type, auth_string = auth_header.split(' ')
                if auth_type.lower() == 'basic':
                    auth_decoded = base64.b64decode(auth_string).decode('utf-8')
                    username, password = auth_decoded.split(':')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return JsonResponse({'message': 'Inicio de sesión exitoso', 'username': username}, status=200)
                    else:
                        return JsonResponse({'error': 'Nombre de usuario o contraseña no válidos'}, status=400)
                else:
                    return JsonResponse({'error': 'Unsupported authentication method'}, status=400)
            except (ValueError, TypeError, base64.binascii.Error):
                return JsonResponse({'error': 'Invalid Authorization header'}, status=400)
        return JsonResponse({'error': 'Authorization header missing'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
    
"""