from functools import wraps
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import base64


def basic_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_type, auth_string = auth_header.split(' ')
                if auth_type.lower() == 'basic':
                    auth_decoded = base64.b64decode(auth_string).decode('utf-8')
                    username, password = auth_decoded.split(':')
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if not request.user.is_authenticated:
                            login(request, user)
                        return view_func(request, *args, **kwargs)
                    else:
                        return JsonResponse({'error': 'Nombre de usuario o contraseña no válidos'}, status=401)
                else:
                    return JsonResponse({'error': 'Unsupported authentication method'}, status=401)
            except (ValueError, TypeError, base64.binascii.Error):
                return JsonResponse({'error': 'Invalid Authorization header'}, status=400)
        return JsonResponse({'error': 'Authorization header missing'}, status=401)

    return _wrapped_view
