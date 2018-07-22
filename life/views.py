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
        resp = {
            'status': 'success',
            'method': data['type']
        }

        try:
            inv_item = Item.objects.get(pk=data['inventory_id'])
        except:
            inv_item = None            
            
        try:
            cart_item = Cart.objects.get(pk=data['cart_id'])
        except:
            try:
                cart_item = Cart.objects.get(item__id=data['inventory_id'])
            except:
                cart_item = None
                
        if cart_item:
            resp['cart_id'] = cart_item.id

        if data['type'] == 'add':
            if not cart_item and inv_item:
                cart_item = Cart(item_id=inv_item.id, quantity=1)
                cart_item.save()
                resp['cart_id'] = cart_item.id
                resp['info'] = 'added new cart item (none prior existing)'
                return JsonResponse(resp)
            elif cart_item:
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
                resp['quantity'] = cart_item.quantity
                resp['info'] = 'increased cart item quantity' 
                return JsonResponse(resp)
            else:
                resp['status'] = 'error'
                resp['reason'] = 'no matching cart or inventory item found' 
                return JsonResponse(resp)
        elif data['type'] == 'remove':
            if cart_item:
                cart_item.delete()
                resp['info'] = 'deleted item from cart'
                return JsonResponse(resp)
            else:
                resp['status'] = 'error'
                resp['reason'] = 'no matching cart item found'
                return JsonResponse(resp)
        elif data['type'] == 'setquantity':
            if cart_item:
                if data['quantity'] > 1:
                    cart_item.quantity = data['quantity']
                    cart_item.save()
                    resp['quantity'] = cart_item.quantity
                    return JsonResponse(resp)
                else:
                    cart_item.delete()
                    resp['info'] = 'deleted item from cart'
                    resp['method'] = 'remove'
                    return JsonResponse(resp)
            else:
                resp['status'] = 'error'
                resp['reason'] = 'no matching cart item found'
                return JsonResponse(resp)
        elif data['type'] == 'inc':            
            if cart_item:
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
                resp['quantity'] = cart_item.quantity
                return JsonResponse(resp)
            else:
                resp['status'] = 'error'
                resp['reason'] = 'no matching cart item found'
                return JsonResponse(resp)
        elif data['type'] == 'dec':
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity = cart_item.quantity - 1
                    cart_item.save()
                    resp['quantity'] = cart_item.quantity
                    return JsonResponse(resp)
                else:
                    cart_item.delete()
                    resp['info'] = 'deleted item from cart'                    
                    return JsonResponse(resp)
            else:
                resp['status'] = 'error'
                resp['reason'] = 'no matching cart item found'
                return JsonResponse(resp)
        else:
            print('unknown data type posted to editcart: ' + data['type'])            
            resp['status'] = 'error'
            resp['reason'] = 'unknown data type'
            return JsonResponse(resp)

    return JsonResponse({'status': 'unknown', 'method': data['type']})

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