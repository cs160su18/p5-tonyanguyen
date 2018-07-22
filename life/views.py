from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import requires_csrf_token
from life.models import Item, Cart
from life.forms import ItemForm
import json


def index(request):
    items_list = Item.objects.all()
    return render(request, 'life/index.html', {'items': items_list})
  
# User foreign key in cart to refer the item
# Once we have the item, subtract the quantity from the database
# Save, remove everything from the cart
    
def cart(request):
    items_list = Cart.objects.all()
    return render(request, 'life/cart.html', {'items': items_list})  

  
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
 
def admin(request):
    items_list = Item.objects.all()
    return render(request, 'life/admin.html', {'items': items_list})

def editcart(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        try:
            item = Item.objects.get(pk=data['id'])
        except:
            item = None
            
        print(item)

        if data['type'] == 'add':
            addtocart(data['id'])
            return JsonResponse({'status': 'success', 'data': newentry})
        elif data['type'] == 'remove':
            removefromcart(data['id'])
        elif data['type'] == 'swap':
            addtocart(data['id'])
            return JsonResponse({'status': 'success', 'incart': True})
        elif data['type'] == 'setquantity':
            pass
        elif data['type'] == 'increment':
            pass
        elif data['type'] == 'decrement':
            pass
        else:
            print('unknown data type posted to editcart: ' + data['type'])
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'success'})

def addtocart(pk):
    newentry = Cart(item_id=pk, quantity=1)
    newentry.save()

def removefromcart(item):
    Cart.objects.get(item=item).delete()

def edititems(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        if data['type'] == 'add':
            pass
        elif data['type'] == 'remove':
            Item.objects.get(pk=data['id']).delete()
        elif data['type'] == 'setquantity':
            Item.objects.get(pk=data['id'])
        elif data['type'] == 'increment':
            pass
        elif data['type'] == 'decrement':
            pass
        else:
            print('unknown data type posted to edititems: ' + data['type'])
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'success'})