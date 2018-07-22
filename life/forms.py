from django.forms import ModelForm
from life.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'cost', 'quantity']
        
    # https://stackoverflow.com/a/31627454 & https://stackoverflow.com/a/32986885
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})