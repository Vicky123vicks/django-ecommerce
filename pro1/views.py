from django.http import HttpResponse

def login_view(request):
    return HttpResponse("Hello, welcome to your Django e-commerce site!")
