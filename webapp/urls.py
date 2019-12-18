from django.urls import path
from .views import welcome, list_pizza, order_pizza, my_orders, all_orders, get_or_create_customer


urlpatterns = [
    path('', welcome, name="welcome"),
    path('get_or_create_customer/<str:action>', get_or_create_customer, name="get_or_create_customer"),
    path('pizzas', list_pizza, name="list_pizza"),
    path('order_pizza', order_pizza, name="order_pizza"),
    path('my_orders', my_orders, name="my_orders"),
    path('all_orders', all_orders, name="all_orders"),
]