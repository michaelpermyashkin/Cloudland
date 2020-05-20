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

# Products page to view all items
def products_order_by(request, order_by):
    products = Product.objects.order_by(order_by)
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
def products_by_category(request, slug):
    products = getProductsByCategory(slug)
    categories = getCategoryList()
    sellers = getSellerList()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': 'category_' + slug,
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected category
def products_by_price(request, min_price, max_price):
    products = getProductsByPrice(min_price, max_price)
    categories = getCategoryList()
    sellers = getSellerList()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': 'price_' + str(min_price) + '_' + str(max_price),
    }
    return render(request, 'store/products-page.html', args)

# Filter products by price where only lower bound is defined
def products_by_price_min(request, min_price):
    products = getProductsByPrice_min(min_price)
    categories = getCategoryList()
    sellers = getSellerList()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': 'price_' + str(min_price) + '_',
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected seller
def products_by_seller(request, slug):
    products = getProductsBySeller(slug)
    categories = getCategoryList()
    sellers = getSellerList()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': 'seller_'+slug,
    }
    return render(request, 'store/products-page.html', args)


def getProductsByCategory(slug):
    products = Product.objects.filter(category__slug=slug).order_by('?')
    return products


def getProductsBySeller(slug):
    products = Product.objects.filter(seller__slug=slug).order_by('?')
    return products

def getProductsByPrice(min_price, max_price):
    lower = float(min_price)
    upper = float(max_price)
    products = Product.objects.filter(price__gte=min_price, price__lte=max_price).order_by('?')
    return products

def getProductsByPrice_min(min_price):
    lower = float(min_price)
    products = Product.objects.filter(price__gte=min_price).order_by('?')
    return products

def getCategoryList():
    categories = Category.objects.order_by('name')
    return categories


def getSellerList():
    sellers = Seller.objects.order_by('seller_listing_name') 
    return sellers

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