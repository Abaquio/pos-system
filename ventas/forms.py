from django import forms
from .models import Producto, Venta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto','cantidad']