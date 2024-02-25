from django.urls import path
from .views import products,user_reg, user_login, user_logout, update_product


urlpatterns = [
    # path('index/',index, name="index"),
    path('products/',products,name="products"),
    path('user_reg/',user_reg,name="user_reg"),
    path('user_login/',user_login,name="user_login"),
    path('user_logout/', user_logout, name="user_logout"),
    path('update_product/<str:product_id>/', update_product, name="update_product"),

]
