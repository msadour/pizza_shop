"""
Views.
"""
import os
import json
import platform

from django.shortcuts import render
from .models import Customer, Pizza, Order
from .forms import AuthenticationForm, CreateCustomerForm, PizzaForm, FilterOrderForm

context = {}

def init_database(request):
    """
    Init the database if empty.
    :param request:
    :return:
    """
    Customer.objects.all().delete()
    Pizza.objects.all().delete()
    Order.objects.all().delete()
    if platform.system() in ['Linux', 'Darwin']:
        slash = '/'
    else:
        slash = '\\'

    path_pizzas_files = os.getcwd() + slash + "webapp" + slash + "pizzas.json"
    pizzas = json.load(open(path_pizzas_files))['pizzas']
    for pizza in pizzas:
        new_pizza = Pizza(**pizza)
        new_pizza.save()
    usertest = Customer(**json.load(open(path_pizzas_files))['usertest'])
    usertest.save()

def welcome(request, errors=None):
    """
    Go to the authentication page.
    :param request:
    :param errors:
    :return:
    """
    if len(Pizza.objects.all()) == 0:
        init_database(request)
    context['errors'] = errors
    context['form_username'] = AuthenticationForm()
    context['form_create_customer'] = CreateCustomerForm()
    if "current_user" not in context.keys():
        return render(request, 'webapp/welcome.html', context)
    return list_pizza(request)

def get_or_create_customer(request, action=""):
    """
    Get or create an user according to which form has been used.
    :param request:
    :param action:
    :return:
    """
    if request.method == "POST":
        if action == 'create':
            form = CreateCustomerForm(request.POST)
            if form.is_valid():
                if Customer.objects.filter(username=form.cleaned_data['username']).exists():
                    return welcome(request, ["This username is already used."])
                new_customer = Customer(**form.cleaned_data)
                new_customer.save()
                context['current_user'] = new_customer
        else:
            form = AuthenticationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                if Customer.objects.filter(username=username).exists():
                    context['current_user'] = Customer.objects.get(username=username)
                else:
                    return welcome(request, ["Username doesn\'t exist"])
    return list_pizza(request)

def list_pizza(request):
    """
    Go the the pizzas pages.
    :param request:
    :return:
    """
    context['pizza_forms'] = [PizzaForm(pizza) for pizza in Pizza.objects.all()]
    return render(request, 'webapp/pizzas.html', context)

def order_pizza(request):
    """
    Order a selected pizza.
    :param request:
    :return:
    """
    if request.method == "POST":
        form = PizzaForm(None, request.POST)
        if form.is_valid():
            context['current_user'].order_pizza(**form.cleaned_data)
        return orders(request, 'mine')
    return list_pizza(request)

def orders(request, mine=None, filter_orders=None):
    """
    Go to the page of orders (all of them or order's user)
    :param request:
    :param mine:
    :param filter_orders:
    :return:
    """
    context['mine'] = mine
    context['form_filter'] = FilterOrderForm()
    context['orders'] = context['current_user'].get_orders(mine, filter_orders)

    return render(request, 'webapp/orders.html', context)

def filter_orders(request):
    """
    Filter the orders.
    :param request:
    :return:
    """
    if request.method == "POST":
        form = FilterOrderForm(request.POST)
        if form.is_valid():
            return orders(request, False, form.cleaned_data)
    return orders(request)
