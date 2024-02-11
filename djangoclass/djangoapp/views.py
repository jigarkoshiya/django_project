from django.http import HttpResponse
from django.shortcuts import render
from .models import Products

def products(request):
    products=Products.objects.all()
    print(products)
    return HttpResponse(products)
# Create your views here.


from django.shortcuts import render
def products(request):
    products=Products.objects.all()
    return render(request,'product.html', context={'products':products})
