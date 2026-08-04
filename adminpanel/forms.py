from django import forms
from accounts.models import CustomUser


class SellerForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:
        model = CustomUser

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
        })
            
    def save(self, commit=True):

        seller = super().save(commit=False)

        seller.role = "seller"

        if self.cleaned_data.get("password"):
            seller.set_password(self.cleaned_data["password"])

        if commit:
            seller.save()

        return seller
            
class EditSellerForm(forms.ModelForm):

    class Meta:
        model = CustomUser

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

class EditCustomerForm(forms.ModelForm):

    class Meta:

        model = CustomUser

        fields = [

            "first_name",

            "last_name",

            "username",

            "email",

            "phone",

            "city",

            "state",

            "address",

        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                "class": "form-control"

            })


from products.models import Product

class EditProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [

            "product_name",

            "description",

            "category",

            "price",

            "stock",

            "image",

        ]

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                "class":"form-control"

            })