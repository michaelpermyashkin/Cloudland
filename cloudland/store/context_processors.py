from .models import Product, Seller, Category

categories = Category.objects.order_by('name') # list of all categories 
sellers = Seller.objects.order_by('seller_listing_name') # list of all sellers 

def add_variables_to_context(request):
    return {
        'sellers': sellers,
        'categories': categories,
    }