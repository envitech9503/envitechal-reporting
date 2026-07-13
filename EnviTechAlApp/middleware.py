from django.http import HttpResponseServerError
from django.shortcuts import render

class CustomExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # Handle the exception and redirect to a custom error view
            return self.handle_exception(request, e)

        return response

    def handle_exception(self, request, exception):
        # Log full detail server-side; show users a generic message + reference id
        import logging, uuid
        ref = uuid.uuid4().hex[:8]
        logging.getLogger('etal.errors').error('ref=%s path=%s: %s', ref, getattr(request, 'path', '?'), exception, exc_info=True)
        context = {
            'error': 'An unexpected error occurred. Please try again or contact the lab administrator. Reference: %s' % ref,
        }
        return render(request, 'error.html', context, status=500)
