from django import forms
from .models import Product,Category,Order

class categoryForm(forms.ModelForm):
    # Include category fields
    category_name = forms.CharField(max_length=100, required=True, label="Category Name")
    category_image = forms.ImageField(required=False, label="Category Image")
    
    class Meta:
        model = Category  # Specify the model the form is based on
        fields = ['category_name', 'category_image']  # Specify the fields to include
        labels = {
            'category_name': 'Category Name',
            'category_image': 'Category Image'
        }

class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_ID', 'product_name', 'product_description', 'price', 'quantity_in_stock', 'category', 'product_image']
        labels = {
            'product_ID': 'Product Code',
            'product_name': 'Name',
            'product_description': 'Description',
            'price': 'Price',
            'quantity_in_stock': 'Quantity in Stock',
            'category': 'Category',
            'product_image': 'Product Image'
        }
        widgets = {
            'product_ID': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # Ensure dropdown is styled properly
        }

    def __init__(self, *args, **kwargs):
        super(productForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # If editing, disable product_ID field
            self.fields['product_ID'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        # Save the product instance
        product = super(productForm, self).save(commit=False)

        if commit:
            product.save()

        return product



class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = Order  # Reference the correct model here
        fields = ['shipping_address']  # Use the correct field names
