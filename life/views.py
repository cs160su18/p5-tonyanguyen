from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from life.models import *
from life.forms import ItemForm

def index(request):
    items_list = Item.objects.all()
    return render(request, 'life/index.html', {'items': items_list})
  
def cart(request):
    return render(request, 'life/cart.html', {'items': items_list})  
  
def update(request):    
    id = 0 # change to get primary key from url query string
    item = Item.objects.get()
    form = ItemForm()
    return render(request, 'life/update.html', {'items': items_list}) 

def login(request):
    form = AuthenticationForm()
    return render(request, 'life/login.html', {'form': form})  

def register(request):
    form = UserCreationForm()
    return render(request, 'life/register.html', {'form': form})