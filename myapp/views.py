from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('Welcome!')

def create(request):
    return HttpResponse('create!')

def read(request, id):
    return HttpResponse('read!' + id)


    
