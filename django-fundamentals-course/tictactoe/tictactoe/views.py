from django.http import HttpResponse

def welcome(request):
    return HttpResponse("Welcome to the site!")



# Create your views here.
