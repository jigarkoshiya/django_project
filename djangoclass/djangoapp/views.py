from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Products
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

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
    return render(request, 'product.html', context=context)




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

        existing_email = User.objects.filter(email=email).first()

        if existing_user:
            message = 'this user already exists'
        elif existing_email:
            message = 'this email already exists'
        elif password != confirm_password:
            message = 'password doesnt exists'
        else:
            # user = User(username=username, email=email, password=password)
            user = User.objects.create_user(username=username, email=email, password=password)
            # products = Products.objects.create()
            user.save()
            return redirect("user_login")
        context = {"message": message}
    return render(request, 'user_reg.html', context)


def user_login(request):
    message = ""
    if request.method == "POST":
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        email = request.POST.get('email')
        password = request.POST.get('password')

        username = User.objects.filter(email=email).first()
        print(username, type(username))
        is_authenticated = authenticate(request, username=username, password=password)
        # if not username:
        #     message = "Your email is not registered with us"
        if not is_authenticated:
            message = "Password or email doesnt matches. Email maybe not registered with us"
        elif username:            
            login(request, user=username)
            print(username.username, type(username.username), "username.username")
            return redirect('products')
    context = {"message": message}
    return render(request=request, template_name='user_login.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('products')


def update_product(request, product_id):
    product_object = Products.objects.filter(id=product_id).first()
    if not product_object:
        return redirect('products')
        
    context = {"product_object": product_object}
    return render(request=request, template_name='update_product.html', context=context)