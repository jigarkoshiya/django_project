from django.http import HttpResponse
from django.shortcuts import render
from .models import Products

def products(request):
    products=Products.objects.all()
    print(products)
    return HttpResponse(products)
# Create your views here.
