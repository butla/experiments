from django.http import HttpResponse


def index(request):
    return HttpResponse('no siema. Polls tutaj, z tutoriala')
