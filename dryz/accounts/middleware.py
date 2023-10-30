
from threading import local

request_local = local()

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the request object to the thread-local variable
        request_local.request = request

        response = self.get_response(request)

        return response
