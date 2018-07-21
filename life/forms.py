from django.forms import ModelForm
from life.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'cost', 'quantity']