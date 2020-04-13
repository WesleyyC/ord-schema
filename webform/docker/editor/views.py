from django.http import HttpResponse
from django.template import loader


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    template = loader.get_template('editor/webform.html')
    context = {}
    return HttpResponse(template.render(context, request))

def small(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    template = loader.get_template('editor/small.html')
    context = {}
    return HttpResponse(template.render(context, request))