import datetime
import json
import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Products, UserAddress, UserCartModel, UserOrders
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# def products(request):
#     products=Products.objects.all()
#     print(products)
#     return HttpResponse(products)




# def products(request):
#     products = Products.objects.all()
#     context = { 
#         "products": products, 
#         "product_count": len(products)
#     }   
def products(request):
    products = Products.objects.all().order_by('-updated_at')
    context = { 
        "products": products, 
        "product_count": len(products)
    }     
    # return redirect("user_login")
    # if request.user.is_authenticated:
    return render(request, 'product.html', context=context)
    # else:
    #     return redirect("user_login")



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
            message1 = 'this user already exists'
        elif existing_email:
            message1 = 'this email already exists'
        # elif password != confirm_password:
        #     message = 'password doesnt exists'
        else:
            # user = User(username=username, email=email, password=password)
            jigar = User.objects.create_user(username=username, email=email, password=password)
            # products = Products.objects.create()
            jigar.save()
            return redirect("user_login")
        context = {"message": message,
                   "message1":message1}
    return render(request, 'user_reg.html', context)


def user_login(request):
    message = ""
    if request.method == "POST":
        # csrf_token = request.POST.get('csrfmiddlewaretoken')
        email = request.POST.get('email')
        password = request.POST.get('password')

        username = User.objects.filter(email=email).first()
        # print(username, type(username))
        is_authenticated = authenticate(request, username=username, password=password)
        # if not username:
        #     message = "Your email is not registered with us"
        if not is_authenticated:
            message = "Password or email doesn't matches. Email maybe not registered with us"
        elif username:            
            login(request, user=username)
            # print(username.username, type(username.username), "username.username")
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
    
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_price = request.POST.get('product_price')
        product_rating = request.POST.get('product_rating')
        product_quantity = request.POST.get('product_quantity')
        print(product_name, product_description, product_price, product_rating, product_quantity)

        product_obj = Products.objects.filter(id=product_id).first()
        product_obj.product_name = product_name
        product_obj.product_desc = product_description      
        product_obj.price = product_price      
        product_obj.rating = product_rating      
        product_obj.available_quantity = product_quantity      
        product_obj.updated_at = datetime.datetime.now()
        product_obj.save()
        return redirect("products")
        
    context = {"product_object": product_object}
    return render(request=request, template_name='update_product.html', context=context)





def add_product(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            product_description = request.POST.get('product_description')
            product_price = request.POST.get('product_price')
            product_rating = request.POST.get('product_rating')
            available_quantity = request.POST.get('available_quantity')
            product_image = request.FILES.get('product_image')

            product_obj = Products.objects.create(
                product_name=product_name,
                product_desc=product_description,
                price=product_price,
                rating=product_rating,
                available_quantity=available_quantity,
                product_image=product_image
                )
            product_obj.save()
            return redirect('products')

        return render(request,'add_product.html')
    else:
        return redirect('user_login')
    



def delete_product(request, product_id):
    Products.objects.filter(id=product_id).delete()
    return redirect('products')



def add_to_cart(request,product_id):
    product_obj = Products.objects.filter(id=product_id).first()
    user_obj = User.objects.filter(username=request.user.username).first()

    if request.method == 'POST':
        cart_value = request.POST.get('cart_value')
        already_added_obj = UserCartModel.objects.filter(product_id=product_id).first()

        if already_added_obj:
            already_added_obj.quantity += int(cart_value)
            already_added_obj.save()
        else:
            cart_obj = UserCartModel.objects.create(
                    product_id = product_obj,
                    user_id = user_obj,
                    quantity = cart_value
            )
            cart_obj.save()
        print(cart_value, "cart_value")
    return redirect('display_cart')



def display_cart(request):
    user_obj = User.objects.filter(username=request.user.username).first()
    cart_obj = UserCartModel.objects.filter(user_id_id=user_obj.id)

    user_address = UserAddress.objects.filter(user_id=user_obj.id).first()
    context = {"user_obj": user_obj, "cart_obj": cart_obj, "user_address": user_address}
    return render(request, 'display_cart.html', context)



def delete_cart_item(request, product_id):
    user_obj = User.objects.filter(username=request.user.username).first()
    user_id = user_obj.id
    print("#########", user_id)
    product_to_delete = UserCartModel.objects.filter(id=product_id).filter(user_id=user_id).delete()
    return redirect('display_cart')



def user_address(request):
    if request.method == 'POST':
        line1 = request.POST.get('line1')
        line2 = request.POST.get('line2')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        state = request.POST.get('state')
        country = request.POST.get('country')

        if request.user.username and request.user.is_authenticated:
            logged_in_user = User.objects.filter(username=request.user.username).first()
        
        address_obj = UserAddress.objects.create(
            line1=line1,
            line2=line2,
            city=city,
            zip_code=zip_code,
            state=state,
            country=country,
            user_id=logged_in_user
        )
        address_obj.save()
        return redirect('display_cart')
    return render(request,'user_address.html')




@csrf_exempt
def order_placed(request):
    if request.method == "POST":
        
        if request.user.username and request.user.is_authenticated:
            logged_in_user = User.objects.filter(username=request.user.username).first()
            
            is_address_exists = UserAddress.objects.filter(user_id=logged_in_user.id).first()
            if not is_address_exists:
                return JsonResponse({'address_exists':False})
            else:    
                order_placed_list = request.POST.getlist('product_placed[]')
                print(order_placed_list)
                for orders in order_placed_list:
                    cart_item = UserCartModel.objects.filter(user_id=logged_in_user.id).filter(id=orders).first()
                    orders_placed_obj = UserOrders.objects.create(
                        order_id=str(uuid.uuid4()),
                        address_id=is_address_exists,
                        order_placed_at=datetime.datetime.now(),
                        user_id = logged_in_user,
                        payment_type="CASH_ON_DELIVERY",
                        product_total_quantity = cart_item.quantity if cart_item.quantity else 1,
                        product_name= cart_item.product_id.product_name,
                        product_image=cart_item.product_id.product_image,
                        product_quantity= cart_item.quantity if cart_item.quantity else 1,
                        total_amount=float(cart_item.quantity)*cart_item.product_id.price
                    )
                    orders_placed_obj.save()
                    cart_item.delete()
                return HttpResponse("success")

        else:
            pass

def user_orders(request):
    user_order_placed = UserOrders.objects.filter(user_id=request.user.id)

    context = {"user_order_placed": user_order_placed}
    return render(request, 'user_orders.html', context)













