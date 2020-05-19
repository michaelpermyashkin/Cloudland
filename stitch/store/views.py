from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse
from datetime import datetime
from store.models import Product, Seller, Category
import random # to shuffle product order for display

# Products page to view all items
def products_page_all(request):
    products = Product.objects.order_by('?')
    categories = getCategoryList()
    sellers = getSellerList()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': 'category_All',
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected category
def products_by_category(request):
    if request.method == 'POST':
        for key in request.POST.keys():
            if key.startswith('category_'):
                selectedCategory = str(key[9:])
        products = getProductsByCategory(selectedCategory)
        categories = getCategoryList()
        sellers = getSellerList()
        args = {
            'products': products,
            'sellers': sellers,
            'categories': categories,
            'active': 'category_' + selectedCategory,
        }
        return render(request, 'store/products-page.html', args)
    return HttpResponseRedirect(reverse('store-products-page-all-home'))

# Filter products by selected category
def products_by_price(request):
    if request.method == 'POST':
        for key in request.POST.keys():
            if key.startswith('price_'):
                selectedPriceRange = str(key[6:])
                lower = selectedPriceRange.split('-')[0]
                upper = selectedPriceRange.split('-')[1]
        products = getProductsByPrice(lower, upper)
        categories = getCategoryList()
        sellers = getSellerList()
        args = {
            'products': products,
            'sellers': sellers,
            'categories': categories,
            'active': 'price_' + selectedPriceRange,
        }
        return render(request, 'store/products-page.html', args)
    return HttpResponseRedirect(reverse('store-products-page-all-home'))

# Filter products by selected seller
def products_by_seller(request):
    if request.method == 'POST':
        for key in request.POST.keys():
            if key.startswith('seller_'):
                selectedSeller = str(key[7:])
        products = getProductsBySeller(selectedSeller)
        categories = getCategoryList()
        sellers = getSellerList()
        args = {
            'products': products,
            'sellers': sellers,
            'categories': categories,
            'active': 'seller_'+selectedSeller,
        }
        return render(request, 'store/products-page.html', args)
    return HttpResponseRedirect(reverse('store-products-page-all-home'))


def getProductsByCategory(filterCategory):
    filterCategory = filterCategory.lower()
    if filterCategory == 'all':
        products = Product.objects.order_by('?')
    else:
        category_list = Category.objects.values_list('name', flat=True) 
        for category in category_list:
            if category.lower() == filterCategory:
                products = Product.objects.filter(category__name=category).order_by('?')
    return products


def getProductsBySeller(filterSeller):
    filterSeller = filterSeller.lower()
    if filterSeller == 'all':
        products = Product.objects.order_by('?')
    else:
        seller_list = Seller.objects.values_list('seller_listing_name', flat=True) 
        for seller in seller_list:
            if seller.lower() == filterSeller:
                products = Product.objects.filter(seller__seller_listing_name=seller).order_by('?')
    return products

def getProductsByPrice(lower, upper):
    lower = float(lower)
    upper = float(upper)
    products = Product.objects.filter(price__gte=lower, price__lte=upper).order_by('?')
    return products


def getCategoryList():
    categories = Category.objects.values_list('name', flat=True).order_by('name')
    return categories


def getSellerList():
    sellers = Seller.objects.values_list('seller_listing_name', flat=True).order_by('seller_listing_name') 
    return sellers

# View when an item is selected to display item detail
def view_item(request):
    selectedProductID = None
    if request.method == 'POST':
        for key in request.POST.keys():
            if key.startswith('get-prod-info'):
                selectedProductID = int(key[13:])

    # we successfully found product
    if selectedProductID != None:
        product = Product.objects.filter(product_id=selectedProductID)
        args = {
            'product': product,
        }
        return render(request, 'store/view-item.html', args)
    #  maybe add an oops page instead of going back to same page
    else :
        return render(request, 'store/products-page.html')


# Contact page
def contact(request):
    return render(request, 'store/contact.html')

# products = [
#     {
#         'product_id': 100002,
#         'product_name': 'Item name',
#         'price': 7.98,
#         'seller': Seller.objects.get(pk=1),
#         'category': Category.objects.get(pk=1),
#         'description_short': 'Brief description...',
#         'description_full': 'Full product description...',
#         'product_image': 'img.jpg',
#         'is_featured': False,
#         'date_listed': datetime.now(),
#         'quantity': 10,
#     }, 
# ]

# for product in products:
#     Product.objects.create(**product)