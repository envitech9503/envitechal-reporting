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
        # Customize this function to handle the exception as needed
        context = {
            'error': str(exception),
        }
        return render(request, 'error.html', context, status=500)
