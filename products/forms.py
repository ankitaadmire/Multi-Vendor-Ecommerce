from django import forms
from .models import ProductRequest


class ProductRequestForm(forms.ModelForm):

    class Meta:
        model = ProductRequest

        fields = [
            'product_name',
            'description',
            'price',
            'stock',
            'category',
            'image',
        ]

        widgets = {

            'category': forms.Select(attrs={
                'class': 'form-select'
            })

        }