from django.http import HttpResponse
from django.shortcuts import render
from .models import Products
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


def products(request):
    products=Products.objects.all()
    print(products)
    return HttpResponse(products)




def products(request):
    products = Products.objects.all()
    context = { 
        "products": products, 
        "product_count": len(products)
    }
    return render(request, 'products.html', context=context)




@csrf_exempt
def user_reg(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('repass')

        if password != confirm_password:
            message = "Incorrect password"
        else:
            message = "Correct password"
        
        existing_user = User.objects.filter(username=username).first()
        print(existing_user)
        if existing_user:
            message = 'this user already exists'
        else:
            # user = User(username=username, email=email, password=password)
            user = User.objects.create_user(username=username, email=email, password=password)
            # products = Products.objects.create()
            user.save()
            print(username, email, password, confirm_password)
        context = {"message": message}
    return render(request, 'user_reg.html', context)


def user_login(request):
    pass