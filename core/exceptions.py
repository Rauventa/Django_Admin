from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if settings.DEBUG:
        return response

    if response is not None:
        data = response.data
        response.data = {}
        errors = []
        for field, value in data.items():
            if not isinstance(value, str):
                value = ", ".join(value)
            errors.append({field: value})

        response.data['errors'] = errors
    else:
        request = context.get('request')
        try:
            if request and hasattr(request, 'stream') and request.stream.path.startswith('/api/v1/'):
                if isinstance(exc, Exception):
                    return Response({'base_errors': [str(exc)]}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            pass

    return response
