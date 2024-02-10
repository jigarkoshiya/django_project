from django.db import models

class Products(models.Model):
    product_name = models.CharField(max_length=100)
    product_dec=models.TextField()
    price=models.FloatField(default=10,null=True,blank=True)
    prouct_image=models.ImageField(null=True,blank=True)
    rating=models.FloatField(null=True,blank=True)
    active=models.BooleanField(default=True,null=True,blank=True)
    available_quantity=models.ImageField(null=True,blank=True)
    

    class Meta:
        verbose_name_plural="products"

    def __str__(self):
        return self.product_name

# Create your models here.
