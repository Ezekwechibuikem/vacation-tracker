from django.shortcuts import redirect
from django.urls import reverse

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('login') and request.GET.get('next') == '/':
            return redirect(reverse('index'))  # Redirect to a different URL
        return self.get_response(request)
