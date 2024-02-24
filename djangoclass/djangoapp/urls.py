from django.urls import path
from .views import products,user_reg


urlpatterns = [
    # path('index/',index, name="index"),
    path('products/',products,name="products"),
    path('user_reg/',user_reg,name="user_reg"),
    # path('user_login/',user_login,name="user_login"),
]
