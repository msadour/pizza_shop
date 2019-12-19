"""
Models.
"""
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    """
    Class Customer.
    """
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)

    def get_orders(self, mine=False, filter_orders=None):
        """
        Get orders.
        :param mine:
        :param filter_orders:
        :return:
        """
        if mine:
            return self.order_customer.all()

        if filter_orders:
            if filter_orders['criteria'] == 'name':
                return Order.objects.filter(customer__name=filter_orders['key_word'])
            return Order.objects.filter(customer__email=filter_orders['key_word'])
        return Order.objects.all()

    def order_pizza(self, **kwargs):
        """
        Order a pizza.
        :param kwargs:
        :return:
        """
        pizza = Pizza.objects.get(type=kwargs.get('type'))
        size = kwargs.get('size')
        new_order = Order(pizza=pizza, size=size, customer=self)
        new_order.save()
        return new_order

    def clean_orders(self):
        """
        Delete all orders.
        :return:
        """
        self.order_customer.all().delete()


class Pizza(models.Model):
    """
    Class Pizza.
    """
    type = models.CharField(max_length=200)

class Order(models.Model):
    """
    Class order.
    """
    date = models.DateField(default=timezone.now)
    pizza = models.ForeignKey(Pizza, related_name='order_pizza', blank=False,
                              on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='order_customer', blank=False,
                                 on_delete=models.CASCADE)
    size = models.CharField(max_length=200)
