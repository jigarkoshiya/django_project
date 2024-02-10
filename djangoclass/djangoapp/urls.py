from django.urls import path
from .views import products


urlpatterns = [
    # path('index/',index, name="index"),
    path('prodycts',products,name="products"),
]
