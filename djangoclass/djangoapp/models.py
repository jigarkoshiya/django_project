from django.db import models

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    product_dec=models.TextField()
    price=models.FloatField(default=10,null=True,blank=True)
    prouct_image=models.ImageField(null=True,blank=True)
    rating=models.FloatField(null=True,blank=True)
    active=models.BooleanField(default=True,null=True,blank=True)
    available_quantity=models.IntegerField(null=True,blank=True)
    

    class Meta:
        verbose_name_plural="products"

    def __str__(self):
        return f"Name :{self.product_name}, Discription: {self.product_dec}, price: {self.price}, Image: {self.prouct_image}, Rating: {self.rating}, Active: {self.active}, Available_quantity: {self.available_quantity}"
    

# Create your models here.
