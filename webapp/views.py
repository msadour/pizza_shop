import os
import json
import platform

from django.shortcuts import render
from .models import Customer, Pizza, Order
from .forms import AuthenticationForm, CreateCustomerForm, PizzaForm

context = {}
#
# def check_login(method):
#     def wrapper(request, *args, **kwargs):
#         if "current_user" not in context.keys():
#             return welcome(request)
#         return method(request, *args, **kwargs)
#     return wrapper

def init_database():
    if platform.system() in ['Linux', 'Darwin']:
        slash = '/'
    else:
        slash = '\\'

    path_pizzas_files = os.getcwd() + slash + "webapp" + slash + "pizzas.json"
    pizzas = json.load(open(path_pizzas_files))['pizzas']
    for pizza in pizzas:
        new_pizza = Pizza(**pizza)
        new_pizza.save()

def welcome(request, errors=[]):
    if len(Pizza.objects.all()) == 0:
        init_database()
    context['errors'] = errors
    context['form_username'] = AuthenticationForm()
    context['form_create_customer'] = CreateCustomerForm()
    if "current_user" not in context.keys():
        return render(request, 'webapp/welcome.html', context)
    else:
        return list_pizza(request)

def get_or_create_customer(request, action=""):
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
    context['pizza_forms'] = [PizzaForm(pizza) for pizza in Pizza.objects.all()]
    return render(request, 'webapp/pizzas.html', context)

def order_pizza(request):
    if request.method == "POST":
        form = PizzaForm(None, request.POST)
        if form.is_valid():
            pizza = Pizza.objects.get(type=form.cleaned_data['type'])
            size = form.cleaned_data['size']
            # import pdb; pdb.set_trace()
            new_order = Order(pizza=pizza, size=size, customer=context['current_user'])
            new_order.save()
        return orders(request, 'mine')

def orders(request, mine=None):
    if mine:
        context['orders'] = context['current_user'].order_customer.all().order_by('date')
    else:
        context['orders'] = Order.objects.all()
    return render(request, 'webapp/my_orders.html', context)



