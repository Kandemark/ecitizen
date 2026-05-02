from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['success'] = False
        if 'detail' not in response.data and hasattr(exc, 'detail'):
            response.data['detail'] = str(exc.detail)
    return response
