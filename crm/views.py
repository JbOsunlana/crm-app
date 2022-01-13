from django.contrib.auth.signals import user_logged_in
from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, RegisterForm #it will replace the UserCreationForm in the register view
from django.forms import inlineformset_factory #to make multiple forms in a form. form will turn to formset
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm #this i sthe first import for the form
# Create your views here.
from django.contrib import messages # this is for the pop up message that comes up after signing up or logging in
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
       form = RegisterForm(request.POST)
       if form.is_valid():
           form.save()
           user = form.cleaned_data.get('username') #this is the way to get the username
           messages.success(request, 'Account was created for ' + user)
           
           return redirect('login')
 

    context = {'form':form}
    return render(request, 'crm/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username OR Password is incorrect')
            
    context = {}
    return render(request, 'crm/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')
 
@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending} 
    
    return render(request, 'crm/dashboard.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()

    return render(request, 'crm/products.html', {'products': products})


@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders) #this isfor searching
    orders = myFilter.qs

    context ={'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'crm/customer.html', context)


@login_required(login_url='login')
def CreateOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5) #extra is to set the number of times you want the orer form to show in a form
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'crm/order_create.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'crm/order_create.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'crm/delete.html', context)


