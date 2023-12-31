# models.py
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=14, unique=True)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    quantity_available = models.PositiveIntegerField(default=0)


    def __str__(self):
      return self.name


class Cart(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  products = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)

