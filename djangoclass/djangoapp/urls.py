from django.urls import path
from .views import products,user_reg, user_login, user_logout, update_product,add_product,delete_product,add_to_cart,display_cart,delete_cart_item,user_address,user_orders,order_placed


urlpatterns = [
    # path('index/',index, name="index"),
    path('products/',products,name="products"),
    path('user_reg/',user_reg,name="user_reg"),
    path('user_login/',user_login,name="user_login"),
    path('user_logout/', user_logout, name="user_logout"),
    path('update_product/<str:product_id>/', update_product, name="update_product"),
    path('add_product/', add_product, name="add_product"),
    path('delete_product/<str:product_id>', delete_product, name="delete_product"),
    # path('delete/<str:product_id>', delete, name="delete"),
    path('add_to_cart/<str:product_id>', add_to_cart, name="add_to_cart"),
    path('display_cart/',display_cart, name="display_cart"),
    path('delete_cart_item/<str:product_id>', delete_cart_item, name="delete_cart_item"),
    path('user_address/', user_address, name="user_address"),
    path('user_orders/', user_orders, name="user_orders"),
    path('order_placed/', order_placed, name="order_placed")



]
