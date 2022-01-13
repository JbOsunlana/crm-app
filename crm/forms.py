from django import forms
from django.forms import ModelForm
from .models import Order
from django.contrib.auth.forms import UserCreationForm #first to import for creating a new form
from django import forms #second to import
from  django.contrib.auth.models import User #third to import

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']