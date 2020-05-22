from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse
from datetime import datetime
from store.models import Product, Seller, Category
import random # to shuffle product order for display

categories = Category.objects.order_by('name')
sellers = Seller.objects.order_by('seller_listing_name') 

active_filters = {
    'category': 'category_All',
    'seller': '',
    'price': '',
    'min_price': '',
    'max_price': '',
    'order_by': '?',
}
active = []

def resetDefaultFilters():
    global active_filters
    active_filters = {
        'seller': '',
        'category': 'category_All',
        'min_price': '',
        'max_price': '',
        'order_by': '?',
    }
    getActiveList()

def getActiveList():
    active.clear()
    for key in active_filters:
        if active_filters[key] != '':
            active.append(active_filters[key])
    print(active)


def getProductsWithActiveFilters():
    products = Product.objects.order_by('?')
    getActiveList()
    if active_filters['min_price'] != '' and active_filters['max_price'] != '':
        products = products.filter(price__gte=active_filters['min_price'], price__lte=active_filters['max_price'])
    if active_filters['min_price'] != '' and active_filters['max_price'] == '':
        products = products.filter(price__gte=active_filters['min_price'])
    if active_filters['seller'] != '':
        products = products.filter(seller__slug = active_filters['seller'])
    if active_filters['category'] != 'category_All' and active_filters['category'] != '':
        products = products.filter(category__slug = active_filters['category'])
    if active_filters['order_by'] != '':
        products = products.order_by(active_filters['order_by'])
    return products


# Products page to view all items
def products_page_all(request):
    resetDefaultFilters()
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected seller
def products_by_seller(request, slug):
    active_filters['seller'] = slug
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected category
def products_by_category(request, slug):
    print(slug)
    active_filters['category'] = slug
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# Products page to view all items
def products_order_by(request, order_by):
    active_filters['order_by'] = order_by
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)


# Filter products by selected category
def products_by_price(request, min_price, max_price):
    active_filters['price'] = 'price_'+str(min_price)+'-'+str(max_price)
    active_filters['min_price'] = min_price
    active_filters['max_price'] = max_price
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# Filter products by price where only lower bound is defined
def products_by_price_min(request, min_price):
    active_filters['price'] = 'price_'+str(min_price)
    active_filters['min_price'] = min_price
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# View when an item is selected to display item detail
def view_item(request, id):
    product = Product.objects.filter(product_id=id)
    args = {
        'product': product,
    }
    return render(request, 'store/view-item.html', args)

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