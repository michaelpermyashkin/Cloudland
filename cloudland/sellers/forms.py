from django import forms
from store.models import Product, Seller

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'price', 'shipping_cost', 'description_short', 'description_full', 'product_image', 'quantity']

        # def clean_image(self):
        #     image = self.cleaned_data.get('image', False)
        #     if image:
        #         if image._height > 1920 or image._width > 1080:
        #             self.add_error('product_image', "Image must have a 2")
        #         return image
        #     else:
        #         raise ValidationError("No image found")

class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'price', 'shipping_cost', 'description_short', 'description_full', 'product_image', 'quantity', 'seller']

class SellerBioEditForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['seller_full_name', 'seller_listing_name', 'profile_picture', 'bio_description', 'email']