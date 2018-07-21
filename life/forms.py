from django.forms import ModelForm
from life.models import *

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'cost', 'quantity']