from django import forms
from store.models import Product, Seller

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'price', 'shipping_cost', 'description_short', 'description_full', 'product_image', 'quantity']

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'price', 'shipping_cost', 'description_short', 'description_full', 'product_image', 'quantity', 'seller']

class SellerBioEditForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['seller_full_name', 'seller_listing_name', 'profile_picture', 'bio_description', 'email']