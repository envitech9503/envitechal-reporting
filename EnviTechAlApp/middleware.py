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


class GlobalLoginRequiredMiddleware:
    """Require authentication for every request except an explicit public allowlist."""
    PUBLIC_PREFIXES = ('/login', '/logout', '/static/', '/media/', '/admin/login', '/admin/logout', '/favicon')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        u = getattr(request, 'user', None)
        if u is None or not u.is_authenticated:
            path = request.path
            if not any(path.startswith(p) for p in self.PUBLIC_PREFIXES):
                from django.shortcuts import redirect
                return redirect('/login/?next=' + request.path)
        return self.get_response(request)
