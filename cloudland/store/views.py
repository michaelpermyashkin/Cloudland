import random # to shuffle product order for display
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse
from store.models import Product, Seller, Category
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required

categories = Category.objects.order_by('name') # list of all categories 
sellers = Seller.objects.all().filter(is_active=True).order_by('seller_listing_name') # list of all sellers 
filterPath = ''
# list of all currently active filters
active_filters = {
    'category': 'category_All',
    'seller': 'seller_All',
    'price': 'price_default',
    'min_price': '',
    'max_price': '',
    'order_by': '?',
}
active = [] # array of active filter id's passed into template 

# sets all default filters 
def resetDefaultFilters():
    global active_filters
    active_filters = {
        'seller': 'seller_All',
        'category': 'category_All',
        'price': 'price_default',
        'min_price': '',
        'max_price': '',
        'order_by': '?',
    }
    getActiveList()

# builds array of all currently set filters
def getActiveList():
    active.clear()
    for key in active_filters:
        if active_filters[key] != '':
            active.append(active_filters[key])

# Builds string to display the active filters in template
def buildFilterPath():
    path = ''
    category = active_filters['category']
    if 'All' in category: 
        category = 'All Categories'

    seller = active_filters['seller']
    if 'All' in seller: 
        seller = 'All Sellers'
    else:
        seller_odj = sellers.get(slug=seller)
        seller = seller_odj.seller_listing_name

    price = active_filters['price']
    if 'default' in price:
        price = 'Default $'
    else:
        num_str = price.split("_",1)[1]
        numbers = num_str.split('-')
        numbers = [int(i) for i in numbers] 
        if len(numbers) == 2:
            price = '$'+str(min(numbers))+'.00-$'+str(max(numbers))+'.00'
        if len(numbers) == 1:
            price = '$'+str(numbers[0])+'+'

    order = active_filters['order_by']
    orders = {
        '?': 'Order Default', 
        '-date_listed': 'Latest',
        'price': 'Low to High',
        '-price': 'High to Low'
    }
    for key, value in orders.items(): 
        if key == order:
            order = value

    global filterPath
    filterPath = category.title() + ' / ' + seller.title() + ' / ' + price.title() + ' / ' + order.title()

# Gets all products that match the current filters settings
def getProductsWithActiveFilters():
    # products = Product.objects.filter(quantity__gte=1).order_by('?')
    products = Product.objects.filter(seller__is_active=True).order_by('?')
    getActiveList()
    # Min and Max Price
    if active_filters['min_price'] != '' and active_filters['max_price'] != '':
        products = products.filter(price__gte=active_filters['min_price'], price__lte=active_filters['max_price'])
    # Min Price
    if active_filters['min_price'] != '' and active_filters['max_price'] == '':
        products = products.filter(price__gte=active_filters['min_price'])
    # Max Price
    if active_filters['min_price'] == '' and active_filters['max_price'] != '':
        products = products.filter(price__lte=active_filters['min_price'])
    # Seller
    if active_filters['seller'] != 'seller_All' and active_filters['seller'] != '':
        products = products.filter(seller__slug = active_filters['seller'])
    # Category
    if active_filters['category'] != 'category_All' and active_filters['category'] != '':
        products = products.filter(category__slug = active_filters['category'])
    # Order by
    if active_filters['order_by'] != '':
        products = products.order_by(active_filters['order_by'])
    
    buildFilterPath()
    return products


# Products page to view all items
def products_page_all(request):
    resetDefaultFilters()
    getParamResolver(request)
    products = getProductsWithActiveFilters()

    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
        'filterPath': filterPath
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected seller
def products_by_seller(request, slug):
    getParamResolver(request)
    if slug == 'All':
        active_filters['seller'] = 'seller_All'
    else:
        active_filters['seller'] = slug
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
        'filterPath': filterPath
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected category
def products_by_category(request, slug):
    getParamResolver(request)
    if slug == 'All':
        active_filters['category'] = 'category_All'
    else:
        active_filters['category'] = slug
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
        'filterPath': filterPath
    }
    return render(request, 'store/products-page.html', args)


def getParamResolver(request):
    global active_filters
    # Price GET params
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    price_default = request.GET.get('price')
    if price_default:
        active_filters['price'] = 'price_default'
    else:
        if min_price and not max_price:
            if min_price.isnumeric():
                active_filters['price'] = 'price_'+str(min_price)
                active_filters['min_price'] = min_price
        elif min_price and max_price:
            if min_price.isnumeric() and max_price.isnumeric():
                active_filters['price'] = 'price_'+str(min_price)+'-'+str(max_price)
                active_filters['min_price'] = min_price
                active_filters['max_price'] = max_price
            else:
                pass

    # order_by GET param
    valid_orders = ['?', '-date_listed', 'price', '-price']
    order_by = request.GET.get('order_by')
    if order_by in valid_orders:
        active_filters['order_by'] = order_by

    return

# View when an item is selected to display item detail
def view_item(request, id):
    product = Product.objects.get(product_id=id)
    qaunt_available = range(1, product.quantity+1)
    args = {
        'product': product,
        'qaunt_available': qaunt_available,
    }
    return render(request, 'store/view-item.html', args)

# About page
def about(request):
    return render(request, 'store/about.html', {'sellers': sellers})

# Contact page
@login_required
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['your_email']
            subject = "Message from: " + from_email + " re: " + form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'store/contact-success.html')
    return render(request, 'store/contact.html', {'form': form})


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