# forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = '__all__'
    # name = forms.CharField(max_length=255)
    # barcode = forms.CharField(max_length=14)
    # description = forms.CharField(widget=forms.Textarea)
    # date_added = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

  def __init__(self, *args, **kwargs):
    super(ProductForm, self).__init__(*args, **kwargs)



class BarcodeSearchForm(forms.Form):
  barcode = forms.CharField(max_length=14)

