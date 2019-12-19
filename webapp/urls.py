"""
Urls.
"""
from django.urls import path
from .views import welcome, list_pizza, order_pizza, orders, \
    get_or_create_customer, filter_orders, init_database, logout


urlpatterns = [
    path('', welcome, name="welcome"),
    path('init_database', init_database, name="init_database"),
    path('get_or_create_customer/<str:action>', get_or_create_customer,
         name="get_or_create_customer"),
    path('pizzas', list_pizza, name="list_pizza"),
    path('order_pizza', order_pizza, name="order_pizza"),
    path('orders/<str:mine>', orders, name="orders"),
    path('orders', orders, name="orders"),
    path('filter_orders', filter_orders, name="filter_orders"),
    path('logout', logout, name="logout"),
]
