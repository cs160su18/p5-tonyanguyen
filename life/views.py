from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from life.models import Item, Cart
from life.forms import ItemForm

def index(request):
    items_list = Item.objects.all()
    return render(request, 'life/index.html', {'items': items_list})
  
def cart(request):
    return HttpResponse("User had added items to their cart!")
  
def update(request):
    query = request.GET.get('id', 0)
    print(query)
    
    try:
        item = Item.objects.get(pk=query)
    except:
        item = None
    
    if request.method == 'POST':    
        if item:
            form = ItemForm(request.POST, instance=item)   
            form.save()
        else:
            form = ItemForm(request.POST)   
            form.save()
        # do some sort of redirect or something
    else:        
        if item:
            form = ItemForm(instance=item)
        else:
            form = ItemForm
            
    return render(request, 'life/update.html', {'id': query, 'item': item, 'form': form}) 

def login(request):
    form = AuthenticationForm()
    return render(request, 'life/login.html', {'form': form})  

def register(request):
    form = UserCreationForm()
    return render(request, 'life/register.html', {'form': form})