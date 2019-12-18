from django.db import models
from django.utils import timezone


class Customer(models.Model):
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)

    def orders(self):
        return self.order_set.all()

class Pizza(models.Model):
    type = models.CharField(max_length=200)

class Order(models.Model):
    date = models.DateField(default=timezone.now)
    pizza = models.ForeignKey(Pizza, related_name='order_pizza', blank=False, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='order_customer', blank=False, on_delete=models.CASCADE)
    size = models.CharField(max_length=200)