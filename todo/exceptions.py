from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    
    response = exception_handler(exc, context)

    if response is not None:
        result = {}
        status = {}
        error = response.data
        status['success'] = False
        status['error'] = error
        result['status'] = status
        response.data = result

    return response
